# Validation notes: oas-flight-policy (paid wave 3 validation, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w3_2026-11-25/oas-flight-policy@w3/`, arm
`full`, DeepSeek V4 Flash (Nebius fp8), temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin
head dd0002a. Line numbers are lines of `src/plugin/data/policy.txt`.

## Results

20/24 valid (83.3%), mean field score 0.917, **easy 5/5**. By category: boundary 5/6, distractor 2/2, easy 5/5,
flag 0/3, hidden 2/2, multi 4/4, refusal 2/2. $0.00149 billed per run, 3.9 calls per run, no run over the hosted
65,536 cap. Every run submitted.

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| kapok-strand | boundary_twin | Saturday Avianca D76V-PSNE ($581), PERSONAL_COST_PAID_BY_TRAVELER; key Monday Avianca ($380), ALTERNATE_ROUTE_TOO_EXPENSIVE, PERSONAL_CHANGE_NOT_ALLOWED or PERSONAL_TRAVEL_NOT_COVERED | model slip | It read the Director's PERSONAL_DAYS sign-off and line 573-575 ("may be combined if prior authorization is obtained") as settling it: "leaving Saturday IS allowed (Director approved personal days)". It never searched Monday, so it never applied lines 585-588 (date changes allowed "provided that these changes do not increase the fare cost beyond the comparable options"; $581 is $201 over Monday's $380, beyond "not higher than $200", lines 166-167). The traveller paying the difference does not lift that test. The twin jacaranda-cove ($580) passed. |
| vicuna-marsh | flag | BOOK connection B3KD-WUXC, ALTERNATE_ROUTE_WITHIN_MARGIN; key FLAG either offer | model slip (borderline: a weak flag) | "Savings of $200 or more. ... So the alternative (connecting) is required." It quoted only the second sentence of line 166-169 and never weighed the first ("comparable as long as ... not higher than $200"), which at exactly $200 lets the traveller's nonstop stand. The audit judged the two inclusive tests a real conflict and both offers are held. The connection is arguably the stronger reading; if a re-run books it again, consider a BOOK under a new id. Twins fern-canyon ($509) and guava-ledge ($511) passed. |
| wren-caldera | flag | BOOK LATAM business 2PAL-FSKC (the held offer), PREMIUM_FARE_AUTHORIZED, CHIEF_OF_STAFF; key FLAG for SECRETARY_GENERAL, APPROVAL_REQUIRED | model slip | "the Chief of Staff signed the Premium Fare Authorization Form ... So business class is authorized." It cited CABIN_EXCEPTIONS (6.3) without reading it: "a filled Premium Fare Authorization Form must be approved by the Secretary General" (lines 351-352; also 334-335). The Chief of Staff appears in lines 48, 85 and 96 only as a signer of travel authorizations ("is only allowed to provide travel authorizations", line 85). The record states plainly who signed; a fair reader holds. The flag twin dahlia-mesa (form signed by the Secretary General) passed. |
| yucca-strait | flag | BOOK Aeromexico KZHQ-J2ES (the held offer), LOWEST_FARE; key FLAG for DIRECTOR or SECRETARY, ADVANCE_PURCHASE_TOO_LATE or APPROVAL_REQUIRED | model slip | It never considered timing: "The trip has director sign-off for travel authorization ... Book the lowest fare." Authorized and booked on December 15 for January 4 travel is 20 days, inside "three (3) weeks prior to the travel date" (lines 280-281), so "Fares purchased late ... require additional written approval" (283-284), and none is on file. Twins egret-shoal (21 days, easy) and mango-quarry (late approval on file) passed. |

## Fixes

None. All four failures are slips; no accept set was widened and no record changed.

## Q2

The always-cheapest agent passes **9/24 (37.5%)**, unchanged (`MAX_PASS_ALWAYS_LOWEST = 9`).

## Re-score at this head

Stored answers re-scored against the current verifier: 20/24, easy 5/5 (unchanged).

## Re-run

Required: none. Optional (variance only): vicuna-marsh (weak flag; if it books the connection again, consider a
BOOK under a new id).

## Checks

`uv run pytest -q` (196 passed, 3 skipped), `uv run ruff check .`, `uv lock --check`, `check_shared.py`,
`tools/stock_verify.py` (24 scenarios, 0 failures), stock `nanoagent plugin inspect .` (exit 0).
