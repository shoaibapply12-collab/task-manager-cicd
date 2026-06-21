# Reflection

The lint stage protects against inconsistent formatting and obvious style/code
issues making it into the codebase, catching things a human reviewer might
miss or get tired of flagging by hand. The test stage protects against actual
functional regressions — it verifies that the API's behavior (status codes,
response bodies, error handling) still works the way it's supposed to after a
change, rather than relying on someone remembering to test manually. The
deploy stage protects production itself: by gating it on `needs: test`, a
broken or unformatted change is physically prevented from going live.

Order matters because each stage is more expensive/risky to fail at than the
one before it. If `deploy` ran before `test`, a broken commit could reach
production before anyone — human or pipeline — ever discovered it was broken;
you'd be debugging in production instead of in CI, and users could be exposed
to the failure in the meantime. Running cheap, fast checks (lint, then test)
before the expensive/irreversible step (deploy) means failures get caught at
the earliest, cheapest point.

One thing I'd add to make this closer to a real production setup is a staging
environment/job that deploys first and runs smoke tests against it, with the
production deploy gated on that staging job succeeding — plus storing secrets
(API keys, deploy tokens) in GitHub Secrets rather than the workflow file
itself.
