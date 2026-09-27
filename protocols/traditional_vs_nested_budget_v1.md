# CODE V traditional-vs-nested budget contract v1

**Status:** frozen before the formal comparison.  
**Systems:** the eight-system set in `usable_codev_system_set_v1.md`.  
**Engine:** CODE V 11.5, `CodeV.Application` COM.

## Unit of cost

One evaluation is exactly one execution bundle:

```text
pma;tgr 32;go
fie;go
mtf;mfr 50;ifr 10;plo fre n;go
```

The bundle count includes invalid, rejected, and failed evaluations. COM startup, copying, parsing, and file I/O are reported separately and are not substituted for optical evaluations.

## Fixed variables and candidate grid

For every included system, `RDY S1` is the candidate design/compensator variable and `THI S1` is the perturbation variable. Both must be finite and successfully readable before formal execution. No additional variable may be introduced after the first comparison call.

Candidate design states are the four deterministic `RDY S1` offsets `{-2%, -1%, +1%, +2%}` from the registered nominal value. Perturbation states are the five deterministic `THI S1` offsets `{-2%, -1%, 0%, +1%, +2%}` from the registered nominal value. If an offset produces a non-finite or unrecoverable state, it is a counted failure and the system stops under the existing restoration gate.

## Equal budgets per system

- Traditional path: 20 evaluations = 4 candidate states × 5 fixed repeat/field-condition records. It selects the candidate using nominal direct-MTF only; no inner perturbation loop is allowed.
- Nested path: 20 evaluations = 4 candidate states × 5 perturbation states. It selects the candidate using the prespecified worst-case (minimum over the five perturbation states) direct-MTF score.
- One baseline evaluation and one final restore check are control operations outside the 20-evaluation comparison budget and are reported separately for both paths.
- Total comparison budget: 40 evaluations per system, 320 evaluations for eight systems, plus 16 baseline control evaluations.

The traditional five records are repeated nominal analyses with independent raw-output records; they are not treated as five independent optical systems. They exist only to consume the same 20-call budget as the nested path while preserving a nominal-only decision rule.

## Decision endpoint

The primary endpoint is the selected `RDY S1` candidate under each path and the associated minimum 50 cycles/mm MTF across the native fields present in the raw CODE V report. The decision disagreement indicator is `traditional_choice != nested_choice`. No acceptance-rate or manufacturing-yield claim is allowed.

## Failure and stopping

Every mutation requires readback. Any COM error, parser error, non-finite value, failed restoration, or `Error:` text is preserved and counted; the affected system stops. No post-outcome replacement is allowed within this amendment. The final prescription must restore to nominal within `1e-9*max(1,|x|)`.

## Reporting

Report all 8 systems, all 2 excluded library candidates, the exact evaluation denominator, failures, selected candidates, raw native text, JSONL ledger, and SHA-256 manifest. CODE V results remain independent from the Zemax study.
