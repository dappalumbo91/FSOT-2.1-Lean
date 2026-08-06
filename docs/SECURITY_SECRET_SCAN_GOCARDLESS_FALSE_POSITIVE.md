# Secret scanning: GoCardless “Live Access Token” — false positive

**Alert (GitHub):** GoCardless Live Access Token  
**Flagged string (exact):** `` `live_ingest_spine_labband_gap_eVmp-1023922` ``  
**Validity reported by GitHub:** Unknown  

## Classification: **not a GoCardless API token**

This is **scientific inventory text**, not a payments credential.

| Segment | Meaning |
|---------|---------|
| `live_ingest_spine` | FSOT extension panel / domain id (`Live_Ingest_Spine`) |
| `labband_gap_eV` | lab band-gap observable (electron-volts) |
| `mp-1023922` | Materials Project–style **public** material id |

GitHub’s detector matches a loose `live_…` pattern used by some **GoCardless live** API keys.  
Our string is a **concatenated domain + property + open-science material id**, which collides with that pattern.

**There is no GoCardless integration in this repository.** No payment webhooks, no GC API clients, no merchant tokens.

## Is it “fixed”?

| Layer | Status |
|-------|--------|
| Real GoCardless secret in repo? | **No** — never was |
| Need to rotate a GC live token? | **Only if you have a real GC account key** (unrelated to this string) |
| Contiguous string still in git history / `data/fsot_atlas.sqlite`? | **Yes** — open-science atlas may embed scientific row keys |
| Safe to close alert as false positive? | **Yes** — cite this document |

Do **not** blindly “revoke a GoCardless token” for this id unless you independently confirm a real GC credential was committed (this pattern is scientific, not a payment key).

## What to do in the GitHub Security UI

1. Open the alert → mark **False positive** (or “used in tests / not a secret”).  
2. Comment: *FSOT scientific key: domain `live_ingest_spine` + band-gap eV + Materials Project id `mp-1023922`; no GoCardless product in repo. See `docs/SECURITY_SECRET_SCAN_GOCARDLESS_FALSE_POSITIVE.md`.*  
3. Skip GC token rotation unless you have a real GC live key elsewhere.

## Optional future hardening (atlas generators)

When generating atlas row keys, avoid gluing `live_` + freeform text into one token, e.g. prefer structured fields:

- `domain=live_ingest_spine`
- `property=band_gap_eV`
- `material_id=mp-1023922`

instead of one concatenated scanner-bait string.

## Related

- Panel: `data/live_ingest_spine_benchmark.json`  
- Atlas: `data/fsot_atlas.sqlite`  
- Open-science policy: `docs/OPEN_SCIENCE_ONLY_POLICY.md`
