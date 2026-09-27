# Cross-software sorting audit v1

## Scope and limitation

This is an external software audit, not a claim of identical-prescription replication. The CODE V hold-out systems `tessar` and `petzval` are compared with corresponding OpticStudio sample lens families. The native sample prescriptions are not assumed to be numerically identical; therefore this audit can test whether the decision-rule implementation behaves consistently on representative lens families, but it cannot establish cross-engine equivalence of the CODE V results.

## Frozen settings

- Zemax OpticStudio 2024 R1 bridge, standalone ZOS-API connection.
- Sequential FFT MTF, primary wavelength, all fields, 256 sampling, 100 cycles/mm maximum.
- Decision frequency: 50 cycles/mm, using the nearest returned frequency sample.
- Candidate variable: radius of surface 1, offsets `[-0.02,-0.01,+0.01,+0.02]` relative to each Zemax sample baseline.
- Perturbation variables: thickness of surface 1 and thickness of surface 2.
- Perturbation pairs `(surface-1 thickness, surface-2 thickness)`:
  `(-0.02,+0.01), (-0.01,-0.02), (0,0), (+0.01,+0.02), (+0.02,-0.01)`.
- Score: minimum MTF across non-diffraction-limit field series and sagittal/tangential components at the nearest returned frequency to 50 cycles/mm.
- Each state is saved to a new `.zmx` copy. Source files are never overwritten.

## Evidence and stop rules

The archive retains inspect output, baseline analysis, edit JSON, modified lens copy, bridge summary, native MTF text, raw MTF CSV, and command logs. Stop if a source lens fails to load, an edit targets an inactive/read-only cell, an analysis has no finite MTF series, or the nearest frequency is not within 1 cycles/mm of 50.

