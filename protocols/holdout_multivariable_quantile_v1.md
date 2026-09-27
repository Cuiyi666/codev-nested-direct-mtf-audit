# Hold-out multivariable and quantile amendment v1

## Purpose

This amendment tests whether the nested decision effect survives when two perturbation variables are changed together and when the robust score is defined by a mean or lower quantile rather than only by a single worst case.

## Frozen scope

- Engine: CODE V 11.5, `CodeV.Application` COM interface.
- Systems: `tessar`, `petzval`, and `wideang`, the three hold-out systems that passed finite-variable and native-analysis screening.
- Excluded hold-outs: `eyepiece` and `microscp` remain failed because `RDY S1` read back as the infinite-radius sentinel (`1e18`). They are not replaced in this amendment.
- Candidate variable: `RDY S1`, offsets `[-0.02,-0.01,+0.01,+0.02]` relative to the registered baseline.
- Perturbation variables: `THI S1` and `RDY S2`, each perturbed independently by the fixed relative pairs below.
- Frequency: 50 cycles/mm.
- Candidate nominal repetitions: five complete nominal bundles per candidate.
- Multivariable perturbations: 20 complete bundles per candidate, fixed before execution.

## Frozen perturbation pairs

Each pair is `(THI S1 relative offset, RDY S2 relative offset)`:

```text
(-0.018, +0.013), (+0.006, -0.017), (-0.011, -0.004), (+0.017, +0.009),
(-0.003, +0.019), (+0.014, -0.012), (-0.019, -0.008), (+0.002, +0.004),
(+0.009, -0.019), (-0.007, +0.015), (+0.018, -0.002), (-0.014, +0.007),
(+0.005, +0.011), (-0.009, -0.016), (+0.012, -0.006), (-0.001, +0.018),
(+0.016, +0.001), (-0.017, -0.013), (+0.008, -0.009), (-0.005, +0.003)
```

## Frozen scoring rules

For every candidate, the 20 valid multivariable MTF scores are summarized by:

1. mean score;
2. empirical 5th percentile using the nearest-rank rule (`ceil(0.05*n)` with `n=20`);
3. minimum score.

The selected candidates are the argmax under each rule. No score-dependent sample removal or replacement is allowed. Any COM error, invalid trace, non-finite MTF, parser failure, or failed restoration is retained as a failed record and prevents that system from being called complete.

## Equal-budget interpretation

All four decision rules use the same 20 multivariable bundles per candidate. The amendment compares ranking rules, not total project cost. The nominal-only rule is reported as a reference based on the five nominal bundles and is not treated as a lower-cost implementation of the 20-sample multivariable audit.

## Stop gates

- Stop a system after the first invalid baseline readback.
- Stop a candidate after any perturbation fails to restore the registered baseline.
- Stop the amendment if the frozen pair list, candidate list, or score parser changes after the first result.

