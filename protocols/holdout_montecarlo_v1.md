# Held-out Monte Carlo robustness amendment (v1)

**Status:** frozen before execution.

## Cohort

The three systems that passed the held-out qualification are `tessar`, `petzval`, and `wideang`. The two screening failures are not reintroduced.

## Frozen variables and distribution

- Candidate variable: `RDY S1` offsets `[-0.02, -0.01, +0.01, +0.02]`.
- Perturbation variables: `THI S1` and `RDY S2`.
- Each perturbation component is sampled independently from `Uniform[-0.02,+0.02]` as a relative offset from the nominal readback.
- Pseudorandom generator: Python `random.Random(20260927)`; draws are generated once in system/candidate/sample order and stored before optical calls.
- Samples per candidate: 50; nominal control repeats per candidate: 5.
- Score: minimum finite native MTF at 50 cycles/mm over the parsed field rows.
- Candidate summaries: nominal minimum, Monte Carlo mean, nearest-rank empirical 5th percentile, and Monte Carlo minimum.

## Failure and stopping rules

Every bundle is retained. Invalid readback, `Error:` output, non-finite score, missing MTF row, or failed restore stops the affected system and is recorded as a failure. No random draw or system may be removed after seeing its score. Source prescriptions are opened read-only; all state changes occur in the existing staged CODE V session and are restored before the next state.

## Interpretation

This is a computational Monte Carlo extension of the CODE V study. It is not a physical manufacturing-yield measurement. The output will be reported separately from the fixed-grid quantile audit and used to test whether the held-out candidate ordering is sensitive to the sampled perturbation distribution.
