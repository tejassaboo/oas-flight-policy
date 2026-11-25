# Build notes: oas-flight-policy (wave 3, 2026-11-24)

Built to `pilot_work/tier_plan/build/WAVE3_BUILD_BRIEF.md` from the frozen handbook
`pilot_work/originals/oas/frozen/oas_policy.txt` (Travel Policy of the General Secretariat of the OAS, Administrative
Memorandum 122, Appendix A; 8,215 words, 741 lines, 53,710 bytes, sha256 a8d9c29a...7370f2; under 10,000 words, so
24 scenarios). Made with `_template/instantiate.py oas-flight-policy --slug oas --task-id book-oas-flight
--currency USD --background 0 --scenarios 24`. The user was asleep; every choice below is the recommended one, taken
without asking.

## Flight rules the handbook supports (frozen line numbers)

| Clause | Lines | Operator / kind | Used by |
|---|---|---|---|
| Written advance authorization by the area's highest authority (Director or Secretary, Chief of Staff, Secretary General) | 47-49, 84-85, 94-96 | mandatory | every trip record holds it |
| Economy at the lowest logical fare, except the Secretary General, the Assistant Secretary General and the Chair of the Permanent Council | 145-148, 324-335 (footnote 3) | mandatory ("must comply", "be purchased in Economy Class") | agave-ridge, basalt-vine, condor-flats, llama-terrace, quetzal-bank, rhea-dune, sisal-crest |
| Premium travel is an exception; Premium Fare Authorization Form approved by the Secretary General | 149-151, 334-335, 351-353 | mandatory approver | dahlia-mesa, ocelot-spire, wren-caldera |
| Lowest logical fare: any reasonable itinerary, may need a stop; lowest available fares whenever possible | 159-162, 363-368 | default | every economy case |
| Comparable options: not higher than $200 above the LLF ("$2002" = $200 + footnote 2, lines 185-186) | 166-167, 389-391 | inclusive | fern-canyon, nopal-harbor, jacaranda-cove/kapok-strand, vicuna-marsh |
| Connections required when they save $200 or more without adding more than four hours; stops added for the LLF should not add more than 4 hours | 167-169, 370-372, 391-393 | both inclusive | guava-ledge, heron-pampa/ibis-knoll, vicuna-marsh |
| Beyond the allowance, travellers may use their judgment; reported, may need additional justification | 171-173, 394-396 | permission with reporting | every preference request (see decision 2) |
| Carrier requests follow the personal preference criteria | 398-401 | criteria | nopal-harbor |
| Ancillary fees (baggage) are not counted in the LLF | 425-430 | mandatory ("should not be included") | rhea-dune |
| Only the SG, ASG and Chair may approve their own travel request | 294-296 | prohibition with exception | agave-ridge, llama-terrace |
| Travel plans approved no later than three weeks before travel; late purchases need additional written approval from the duly authorized official in the requesting area | 278-284 | inclusive ("no later than"); "would therefore require" | egret-shoal, mango-quarry, yucca-strait |
| Official travel combined with personal days: prior authorization by Director or Secretary; date changes allowed if the fare does not rise beyond the comparable options; traveller pays differences | 573-597 | mandatory | jacaranda-cove, kapok-strand |
| Third-party paid plans: the GS/OAS covers only the cost of deviating | 602-606 | "should only cover" / "In no case" | urchin-bay |
| SG exception: elected IACHR Commissioner may buy full economy fares | 638-642 | standing exception | puma-lagoon |
| Guests are OAS travellers; institutions that cannot receive payments: GS/OAS buys the fare | 79-80, 644-649 | definition / procedure | quetzal-bank |
| Personal/vacation travel at the traveller's expense, not booked by the corporate agents | 719-727 | mandatory | tapir-hollow |

Not tested, and why: the TMC mandate and the ban on airline-direct purchases (lines 229-244) and the price-match
guarantee (355-361) concern who books and at what matched price, which the simulated world cannot express; rail and
Acela (174-176, 337-344) are not flights; mileage allowance (177-181, 468-473) is driving; statutory travel (27-31,
75-78) is paid by the GS/OAS under the Staff Rules, so a REFUSE ("the organisation buys no ticket at all") would be
wrong and a BOOK would be outside this policy, and it was left out; employees flying together (630-636) names no
number ("please contact DP"), so the handbook has no checkable multi-traveller rule and `OVERLAY_MINIMUMS` has no
`multi_traveller` entry; group travel (86-89, 708-717) is negotiated by DP; there is no flight-duration rule at all
(`DURATION_RULES = ()`, `over()` raises, `DURATION_CASES = []`, three duration tests skip on empty parameters), and
no overnight-stop rule, so no overnight overlay. The 6.10 upgrade rule (413-423) was considered for a "full coach
fare for upgrade purposes" case and dropped: it bars such fares only "when reasonable non-penalty lower fares are
available", and every non-refundable fare carries a penalty, so the case could not be made clear.

## Decisions taken (recommended choices)

1. **"$2002" at line 167** is "$200" with footnote marker 2 (the frozen README says so; line 390 repeats "$200"; the
   footnote at 185-186 reads "The amount of US$200"). Every test uses 20,000 cents.
2. **The traveller's judgment clause** (171-173, 394-396) lets a traveller keep a dearer option beyond the allowance,
   reported and possibly with additional justification. That would make every preference case two-answer. So every
   preference request says, in the same words, "if the policy lets me have it without any extra justification; if
   not, book what the policy calls for". Within the allowance the preference is booked (it is only reported as
   personal preference, 163-165); beyond it the policy's choice is booked. No threshold or rule wording is in the
   request.
3. **The two $200 tests collide at exactly $200.** "not higher than $200" (comparable) and "savings of $200 or more"
   (connection required) are both inclusive, so at exactly $200 the nonstop is comparable and the connection is
   required. That is the plugin's unclear-text flag (`vicuna-marsh`, phrase "savings of $200 or more"), with twins at
   $199 (`fern-canyon`, nonstop only) and $201 (`guava-ledge`, connection only).
4. **Four hours** is measured as the extension of elapsed time over the fastest nonstop (and as the arrival
   difference; every pair leaves at the same time so they agree, and the rules raise otherwise). Exactly 240 minutes
   is not "more than four (4) hours": the connection is required (`heron-pampa`). At 241 (`ibis-knoll`) the
   connection is not required and, read with 370-372, is not a stop the LLF may add, so the nonstop is the LLF; a
   reader who still counts the connection as the LLF ("any reasonable itineraries") books it, so both offers are
   accepted. Measuring flying time only (65 minutes longer) would give "required" in both twins; the 241 accept set
   covers that reading too.
5. **The three exempt officials** may fly the cabin they ask for at its cheapest fare with no Premium Fare form: the
   sentence "Any requests for advance purchase ... of a different class of service must be approved ... by the
   Secretary General" follows the exception and is read as applying to everyone else (2.21 calls premium travel an
   exception, and the three are not under the rule). This is the least certain key (see "Unsure").
6. **Late purchase** (278-284): the trip authorization's `signed_on` against `travel_date`; 21 days is "no later than
   three (3) weeks", 20 is late. In every case the authorization is signed on or a few days before the booking date, so
   the approval date and the purchase date are on the same side. A late trip without the additional approval is a hold
   for the "duly authorized official in the requesting area": DIRECTOR or SECRETARY (84-85). Because every FLAG must be
   a `flag`-category scenario (`tests/test_scenarios.py`), the three-week rule has no boundary-twin pair of its own: its
   boundary is covered by the flag `yucca-strait` (20 days) and its flag twins `egret-shoal` (21 days, BOOK) and
   `mango-quarry` (14 days with the approval on file, BOOK). Every other scenario is authorized 30 or more days ahead.
7. **Premium Fare form signed by someone other than the SG** (`wren-caldera`): hold the cheapest fare in the cabin
   asked for, approver SECRETARY_GENERAL only. A form for business when first is asked (`ocelot-spire`, with a
   fallback) books the cheapest business fare.
8. **Personal days** (`jacaranda-cove`, `kapok-strand`): the ticket is the traveller's own day (Saturday); its lowest
   fare is compared with the lowest fare on the working day (Monday, the record's `business_travel_date`, a pinned
   second search). $200 above is allowed (traveller pays), $201 is not, and the request's fallback books Monday.
9. **Third-party ticket** (`urchin-bay`): the IDB round trip already takes the traveller to Santiago and home around the
   workshop, so the GS/OAS portion ("additional expenses paid to deviate") is nothing: REFUSE. The trip record states
   it in `ticket_from_others` and `ticket_from_others_suffices`.
10. **Approvers** follow SYNC_NOTES 4': BOOKs accept the trip authorizer and NONE, plus SECRETARY_GENERAL where his form
    (dahlia-mesa, ocelot-spire) or his standing exception (puma-lagoon) is relied on, and the late-purchase signer;
    the third-party refusal accepts NONE and DIRECTOR (4(b)); the vacation refusal has no sign-off (NONE). Holds:
    SECRETARY_GENERAL (wren-caldera); DIRECTOR or SECRETARY (yucca-strait); NOT_NAMED, PROCUREMENT_DEPARTMENT,
    DIRECTOR or SECRETARY for the unclear hold (vicuna-marsh; DP receives the personal-preference reports, 395).
11. **Reason codes.** Handbook codes: ECONOMY_CLASS_REQUIRED, PREMIUM_FARE_AUTHORIZED, FULL_ECONOMY_FARE_AUTHORIZED,
    COMPARABLE_FARE_OPTION, LATE_PURCHASE_APPROVED, ANCILLARY_FEES_EXCLUDED, PERSONAL_COST_PAID_BY_TRAVELER,
    PERSONAL_CHANGE_NOT_ALLOWED, THIRD_PARTY_TICKET_COVERS_TRIP. Decoys (subjects grepped in the frozen text, none
    present): NEXT_OF_KIN_TRAVEL, FLY_AMERICA_US_CARRIER_REQUIRED, OPEN_SKIES_AGREEMENT, CREATIVE_TICKETING,
    EXTENDED_TRAVEL_SAVINGS, DENIED_BOARDING_NOT_ALLOWED, CHANCELLOR_WRITTEN_AUTHORIZATION, DOUBLE_BOOKING_PROHIBITED,
    PRIVATE_AIRCRAFT_NOT_APPROVED, TRAVEL_PACKAGE_NOT_ITEMIZED. Dropped: WEEKEND_TRAVEL_HOME and WEEKEND_TRIP_NOT_EARNED
    (a personal weekend appears in two cases), CANDIDATE_TRIP_NOT_COVERED (recruitment travel is named at line 75).
    Declined requests (brief lesson 12): a refused business or first cabin accepts ECONOMY_CLASS_REQUIRED and
    UPGRADE_NOT_ELIGIBLE (ocelot-spire also PREMIUM_FARE_AUTHORIZED), never LOWEST_FARE; the refused Saturday
    (kapok-strand) accepts PERSONAL_CHANGE_NOT_ALLOWED, PERSONAL_TRAVEL_NOT_COVERED, ALTERNATE_ROUTE_TOO_EXPENSIVE;
    nonstops declined by the $200/4-hour test (guava-ledge, heron-pampa) accept LOWEST_FARE beside COST_SAVINGS and
    ALTERNATE_ROUTE_TOO_EXPENSIVE; rhea-dune keeps LOWEST_FARE beside ANCILLARY_FEES_EXCLUDED (the traveller asked
    for the lowest fare, and 6.11 is part of finding it).
12. **Arrival deadlines** (lesson 4): the record has `work_starts`; every listed offer lands before it (the rules raise
    otherwise), and twins carry identical requests.
13. **One ticket, no background** (SYNC_NOTES 5): every case is one way, `return_date` is empty everywhere, and every
    search has `background: 0`, so the agent sees only the pinned offers and no unpinned search lists anything.
14. **Degenerate baselines.** Always-cheapest (cheapest seat, LOWEST_FARE, NONE) passes 7 of 24 (29%: agave-ridge,
    egret-shoal, guava-ledge, heron-pampa, ibis-knoll, mango-quarry, rhea-dune). Always-flag passes 1 (vicuna-marsh).
    `MAX_PASS_ALWAYS_LOWEST = 7`, `MAX_PASS_ALWAYS_FLAG = 1`. Decisions: 19 BOOK (4 business, 15 economy; the
    always-cheapest agent fails 12 of the 19), 2 REFUSE, 3 FLAG.

## Hosted-cap estimate

Policy 53,710 characters; at 0.2 tokens a character plus 1,800 (Thornton/NJC paid calibration): call 1 about 12,500
input tokens, call 2 about 13,300, call 3 about 14,300 to 15,300 (2 to 5 offers). A 3-call run is about 40,000 to
41,000 input tokens and ends near 57,000 with the final message and output: under the 65,536 cap with about 8,000 to
spare. **The two personal-days cases need a second search** (the working day), about 15,000 more, which takes them to
about 71,000: over the hosted cap. One extra tool call on any other case also reaches the cap.

## Blind read (non-flag scenarios), from the handbook text and the tool outputs only

I dumped `get_trip` and `search_flights` (every listed offer, on the travel date and, for the personal cases, the
working day) and re-derived each answer from the frozen text, without `rules.py`.

| Scenario | My reading | Agrees |
|---|---|---|
| agave-ridge | SG, exempt (145-146) but asks the lowest economy fare: UA nonstop $289; self-authorized, allowed (294-296) | yes |
| basalt-vine | Chair of the Permanent Council, exempt (324-328): business asked, cheapest business LATAM $3,620 | yes |
| condor-flats | Director, business asked, no Premium Fare form: economy (324-328), lowest UA $985; fallback given | yes |
| dahlia-mesa | SG-approved form for business (351-353): cheapest business LATAM $3,860 | yes |
| egret-shoal | authorized Dec 14 for Jan 4 = 21 days, not late (280-281): lowest AM $412 | yes |
| fern-canyon | nonstop $509 vs Dallas connection $310 (+150 min): $199 more, comparable; saving under $200, not required: nonstop | yes |
| guava-ledge | $201 more: connection required (saves $200 or more, within 4 h); nonstop needs justification, declined: AA $310 | yes |
| heron-pampa | connection saves $300, lands 240 min later: not more than four hours, required: AA via MIA $940 | yes |
| ibis-knoll | 241 min later: not required; nonstop is the LLF under 370-372, or the connection under 159-161: either | yes |
| jacaranda-cove | Saturday AV $580 vs Monday AV $380: +$200, not beyond comparable (585-588); traveller pays: Saturday AV | yes |
| kapok-strand | Saturday $581: +$201, beyond comparable; fallback: Monday AV $380 | yes |
| llama-terrace | ASG self-approved (294-296), exempt, business: cheapest business UA nonstop $1,150 | yes |
| mango-quarry | 14 days, late, additional approval by the Director on file: lowest AM $412 | yes |
| nopal-harbor | United $338 vs AA $198: +$140, comparable (398-401, 389-391): United | yes |
| ocelot-spire | SG form covers business only; first not covered; fallback: cheapest business UA $980 | yes |
| puma-lagoon | IACHR Commissioner, SG's exception for full economy fares (638-640): cheapest refundable economy AV $890 | yes |
| quetzal-bank | guest on GS/OAS funds is an OAS traveller (79-80); economy (324-328), no form: DL $520 | yes |
| rhea-dune | Chair asks the lowest fare; bag fees excluded from the LLF (427-428): JetBlue $139 | yes |
| sisal-crest | adviser to the Chair is not the Chair (324-328): economy AV $395 | yes |
| tapir-hollow | family vacation, not official travel (719-727): REFUSE | yes |
| urchin-bay | IDB ticket already covers the trip; GS/OAS pays only deviation costs (602-606), none: REFUSE | yes |

All 21 non-flag scenarios agree. The three holds were read too: vicuna-marsh (exactly $200, the two inclusive tests
disagree), wren-caldera (form signed by the Chief of Staff, 351-352 needs the SG), yucca-strait (20 days, no
additional approval, 283-284).

During the read I widened four accept sets where a correct answer could fairly use another value (lesson 5):
ALTERNATE_ROUTE_WITHIN_MARGIN on nopal-harbor and jacaranda-cove, SENIOR_ROLE_ENTITLEMENT on puma-lagoon (an
exception granted to a role), and SECRETARY beside DIRECTOR on vicuna-marsh (the LAX trip is authorized by a
Secretary). I also made tapir-hollow's `work_starts` empty (a vacation has no work).

## Unsure (two-reader risks)

- **basalt-vine, llama-terrace (exempt officials in business).** A cautious reader could hold the business fare for
  the Secretary General's written approval (328-335: "Any requests for advance purchase by GS/OAS of a different class
  of service must be approved in advance and in writing by the Secretary General"). I read the sentence as covering
  the non-exempt; the three officials' tickets are excepted from the economy rule in the same sentence.
- **fern-canyon (nonstop $199 above).** A strict reader of "Lowest available fares must be used whenever possible"
  (161, 365) could book the connection. The comparable-options and personal-preference clauses exist to allow the
  choice, and the traveller asks for it, so only the nonstop is accepted.
- **urchin-bay.** "should only cover" is soft-sounding, but "In no case ... should exceed" and the IDB ticket covering
  every day make nothing to buy.
- **egret-shoal / yucca-strait.** 5.2 speaks of "travel plans" and "Fares purchased late"; I tie lateness to the trip
  authorization's date, which here is also the purchase date. 15 days before the quarter (282) is not modelled.
- **Hosted cap** for the two personal-days cases (above).

## Template change requests

None blocking. Two observations:

1. `tests/test_scenarios.py` requires every FLAG to be in the `flag` category, so a numeric rule whose one side is an
   approval hold (OAS's three-week rule) cannot have a boundary-twin pair; the flag and its flag twins have to stand
   in for it. A "boundary_twin may be a hold" allowance would let such rules have a proper pair.
2. As FedEx noted, the duration hook models only absolute limits; OAS's only time limit is relative (four hours more
   than the nonstop), coded as a constant and tested through its twins.

## Acceptance outputs (final)

```
$ uv run pytest -q
196 passed, 3 skipped in 2.47s
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 10ms
$ python3 ../_template/check_shared.py .
: ok
$ nanoagent plugin inspect .  (stock checkout)
exit 0
$ nanoagent plugin pack . <scratch>/oas-flight-policy.tar.gz  (stock checkout)
packed . into <scratch>/oas-flight-policy.tar.gz (186285 bytes)
$ python ../_template/tools/stock_verify.py .  (stock checkout Python)
agave-ridge          right=True score=1.00 identical=True wrong-decision-rejected=True
basalt-vine          right=True score=1.00 identical=True wrong-decision-rejected=True
condor-flats         right=True score=1.00 identical=True wrong-decision-rejected=True
dahlia-mesa          right=True score=1.00 identical=True wrong-decision-rejected=True
egret-shoal          right=True score=1.00 identical=True wrong-decision-rejected=True
fern-canyon          right=True score=1.00 identical=True wrong-decision-rejected=True
guava-ledge          right=True score=1.00 identical=True wrong-decision-rejected=True
heron-pampa          right=True score=1.00 identical=True wrong-decision-rejected=True
ibis-knoll           right=True score=1.00 identical=True wrong-decision-rejected=True
jacaranda-cove       right=True score=1.00 identical=True wrong-decision-rejected=True
kapok-strand         right=True score=1.00 identical=True wrong-decision-rejected=True
llama-terrace        right=True score=1.00 identical=True wrong-decision-rejected=True
mango-quarry         right=True score=1.00 identical=True wrong-decision-rejected=True
nopal-harbor         right=True score=1.00 identical=True wrong-decision-rejected=True
ocelot-spire         right=True score=1.00 identical=True wrong-decision-rejected=True
puma-lagoon          right=True score=1.00 identical=True wrong-decision-rejected=True
quetzal-bank         right=True score=1.00 identical=True wrong-decision-rejected=True
rhea-dune            right=True score=1.00 identical=True wrong-decision-rejected=True
sisal-crest          right=True score=1.00 identical=True wrong-decision-rejected=True
tapir-hollow         right=True score=1.00 identical=True wrong-decision-rejected=True
urchin-bay           right=True score=1.00 identical=True wrong-decision-rejected=True
vicuna-marsh         right=True score=1.00 identical=True wrong-decision-rejected=True
wren-caldera         right=True score=1.00 identical=True wrong-decision-rejected=True
yucca-strait         right=True score=1.00 identical=True wrong-decision-rejected=True
24 scenarios, 0 failures
```
