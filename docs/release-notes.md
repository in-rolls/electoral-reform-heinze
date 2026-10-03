# Presidential, in Principle: v0.1.0 candidate

This first audit release reproduces Heinze's deposited results and examines what the
headline measures establish about presidential authority, shared tenure and elite
capture. The README leads with the comparison-group levels and the institutional
meaning of the variables, then separates those questions from analytical sensitivity.

The release includes the unchanged Dataverse v1.0 archive and its manifest, preserved
paper and supplementary sources, executable author and independent audit pipelines,
generated results, and a claim-to-evidence record. All 17 survey outcomes are retained
in the recent-cohort diagnostics, including findings that support the paper.

## Findings and scope

- Authority measures imply a weak indirect presidency, but the released variables do
  not reveal the full distribution across discussion participants.
- Shared tenure combines past and planned rotation and changes sharply between early
  and later indirect cohorts. Restricting election cohorts materially changes some
  headline contrasts.
- Unopposed selection, landowner reports and repeated categories from citizen questions
  require institutional and measurement qualifications before interpretation as capture.
- Officeholder composition, selected process evidence and vignette expectations do not
  directly establish sample-wide persistence of elite control.
- Missing dates, original response categories and geographic identifiers prevent some
  proposed checks. These remain unresolved rather than being reported as null results.

The release also retains the associations that survive, the author's relevant defenses,
rejected criticisms, a minor descriptive-standard-error correction, and exact numerical
reproduction boundaries. It makes no finding of fabrication or author misconduct.

## Verification

The candidate is prepared with `make all`, which executes the full R pipeline and the
independent Python arithmetic tests. `make ci-python` verifies retained outputs against
source data and checks Python formatting and generated README tables. GitHub Actions
runs that tier and R linting; it does not rerun the full R estimation. Software versions,
source hashes and analysis logs are retained in the repository.

Release artifacts are standard Git source archives with a SHA-256 sidecar. Extract the
archive and run `make test` to verify the preserved sources and independently reconstruct
the tested statistics. Run `make deps` and `make all` for complete re-estimation.

Publication status and candidate-specific review/CI evidence belong in the GitHub release
description. This file describes the candidate's scope and does not claim that a release
has been published or that pending gates have passed.
