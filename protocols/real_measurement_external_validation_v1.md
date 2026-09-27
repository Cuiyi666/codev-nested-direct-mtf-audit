# Real-system external validation protocol (v1)

**Status:** frozen template; not executed because no measured/as-built dataset was supplied.

## Purpose

The Optics Express-strengthening validation must test whether the decision ordering survives a physical or as-built measurement, rather than treating a library prescription as a manufactured system. This protocol is deliberately separate from the CODE V comparison and will not be populated with simulated values.

## Required inputs

1. As-built prescription or a signed tolerance/as-built record identifying all changed radii, thicknesses, glasses, and spacings.
2. Measured MTF data in a machine-readable table with frequency, field coordinate, tangential/sagittal component, wavelength, detector/pupil sampling, and units.
3. Measurement metadata: instrument/model, calibration date, aperture and focus procedure, environmental conditions, and uncertainty or repeatability estimate.
4. A mapping file linking the measured system to one registered candidate and the frozen perturbation variables.
5. Raw export plus a checksum; processed CSVs are derived artifacts only.

## Frozen analysis

The pre-registered score is the minimum finite measured MTF at the registered frequency over the declared field/component rows. If a measurement is unavailable, non-finite, out of calibration, or cannot be mapped to the candidate, the system is marked `not evaluable`; it is not removed or replaced. No simulated MTF may substitute for a missing measurement.

The comparison will report (i) nominal CODE V ranking, (ii) as-built measured ranking, (iii) absolute and relative score differences, and (iv) whether the nested decision is retained. Measurement uncertainty will be propagated as an interval or bootstrap only after the raw-data lock; it will not be tuned to favor either workflow.

## Stop gates

Stop before scoring if the prescription/measurement identity is ambiguous, the metadata omit calibration or sampling information, the MTF frequency cannot be matched within 1 cycle/mm, or the raw file checksum changes after lock. Report the blocker and preserve the incomplete record.

## Current status

No physical measurement files were present in the study directory at the time of this run. Consequently, no real-system result is claimed in the manuscript. The first suitable measured/as-built system can be added as amendment `real_measurement_v2` without changing the existing CODE V denominators.

Acquisition alternatives and the minimum data package are specified in `REAL_VALIDATION_ACTION_PLAN.md`. Route A (two measured candidate variants) is the strongest validation; Route B (one as-built system with independent MTF) is the minimum credible calibration check; Route C is an honest computational-only submission with bounded claims.
