from pathlib import Path
import argparse, json, math


def parse_args():
    parser = argparse.ArgumentParser(
        description="Audit parsed MTF scores against raw per-run records."
    )
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=None,
        help="Private evidence root containing the run directories; alternatively set CODEV_EVIDENCE_ROOT.",
    )
    return parser.parse_args()


args = parse_args()
ROOT = args.evidence_root or Path.cwd()
RUNS=[ROOT/'runs'/'budget_comparison_replacement_v1',ROOT/'runs'/'frequency30_robustness_v1',ROOT/'runs'/'frequency40_robustness_v1',ROOT/'runs'/'frequency60_robustness_v1',ROOT/'runs'/'frequency70_robustness_v1',ROOT/'runs'/'amplitude05_robustness_v1',ROOT/'runs'/'amplitude20_robustness_v1',ROOT/'runs'/'random_perturbation_repro_v1']

def independent_score(text, target):
    values=[]
    for line in text.splitlines():
        tokens=line.replace('\t',' ').split()
        if not tokens or tokens[0] != str(target): continue
        for token in tokens[1:]:
            try: values.append(float(token))
            except ValueError: pass
    return min(values) if values else None

checks=[]
for run in RUNS:
    target=50
    for f in (30,40,50,60,70):
        if f'frequency{f}' in run.name: target=f
    for rec_path in run.glob('*/record.json'):
        rec=json.loads(rec_path.read_text(encoding='utf-8')); d=rec_path.parent
        expected={}
        if rec.get('baseline',{}).get('score') is not None: expected['baseline']=rec['baseline']['score']
        for group in ('traditional','nested'):
            for item in rec.get(group,[]):
                if group=='traditional':
                    for i,score in enumerate(item.get('scores',[]),1): expected[f'trad_c{item["candidate"]}_r{i}']=score
                else:
                    for i,score in enumerate(item.get('scores',[]),1): expected[f'nest_c{item["candidate"]}_p{i}']=score
        for tag, exp in expected.items():
            p=d/f'{tag}_mtf.txt'; alt=independent_score(p.read_text(encoding='utf-8',errors='replace'),target) if p.exists() else None
            ok=(exp is None and alt is None) or (exp is not None and alt is not None and math.isclose(float(exp),float(alt),rel_tol=0,abs_tol=1e-12))
            checks.append({'run':run.name,'lens':rec.get('lens'),'tag':tag,'expected':exp,'independent':alt,'match':ok})
bad=[x for x in checks if not x['match']]
out={'status':'pass' if not bad else 'fail','checked':len(checks),'mismatches':len(bad),'records':checks}
(ROOT/'runs'/'mtf_parser_audit_v1.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'status':out['status'],'checked':out['checked'],'mismatches':out['mismatches']},indent=2))
