# OAS Travel Policy Flight Booking

**Source of the handbook:** https://www.oas.org/legal/english/admmem/admmen122.pdf. The agent reads it verbatim (bundled at `src/plugin/data/policy.txt`); flights, fares and trips are synthetic.

**No affiliation with the Organization of American States.** The handbook is the *Travel Policy of the General
Secretariat of the Organization of American States* (Administrative Memorandum 122, Appendix A; undated, cites
AG/RES. 2437 of 2008), a public administrative memorandum posted on the OAS legal site
(https://www.oas.org/legal/english/admmem/admmen122.pdf), bundled verbatim for research. Confirm with the course
staff that the verbatim text may be redistributed before publishing this plugin.

A `nanoagent.plugin/v0001` plugin. An agent handles one traveller's flight request under the General Secretariat's
real travel policy: it reads the trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or
**FLAG_FOR_APPROVAL** with the offer, cabin, reason, approver and policy section. A deterministic Python verifier,
with no LLM, rebuilds the offers and the policy's answer itself and checks every field. Built from the
original-handbook template (`handbook_plugins/_template`).

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 8,215 words, 741 lines, 53,710 bytes, sha256 `a8d9c29a...7370f2`, equal
to `pilot_work/originals/oas/frozen/SHA256SUMS`) is never paraphrased, and the task text restates no rule. Under
stock NanoAgent the agent does not see it: the plugin then runs as the `off` baseline. The `harness.policy` switch
of the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it to the system prompt:
`harness.policy: full` adds all of it, and the selection methods add parts of it. These plugins are meant to run
with `query: instructions+input`, so a selector sees the traveller's request. Line 167 prints "$2002": that is
"$200" followed by the marker of footnote 2 (lines 185-186, "The amount of US$200"); the rules read it as $200.

**Size.** At about 0.2 DeepSeek tokens a character of handbook plus 1,800 for the rest of the first prompt (the
Thornton and NJC paid calibration), the first call under `full` is about 12,500 input tokens, the second about
13,300 (plus the trip record) and the third 14,300 to 15,300 (plus 2 to 5 offers). A 3-call run (`get_trip`,
`search_flights`, `submit`) is about 40,000 to 41,000 input tokens, and the final message after `submit` starts near
16,000, so the run ends near 57,000 with output: under the hosted cap of 65,536 with about 8,000 to spare. The two
personal-days cases (`jacaranda-cove`, `kapok-strand`) need a second search (the working day), which adds about
15,000 and takes those runs over the hosted cap; run them where the cap is higher.

## Task

- **Input:** `TaskInput`: `scenario` (one of 24 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on the trip's route and date (and on the working day when the record
  gives a different one), then `submit`.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when refusing),
  `reason_code`, `approver` and `clause`, each from a closed list. The reason list is the template's shared list
  (codes for rules this policy lacks) plus nine codes of this policy and ten decoy codes from other handbooks'
  rules. Fares are in cents of US dollars.
- **Success:** every field is one the answer key accepts; the cabin is graded as the chosen offer's own. Score =
  fields right / 6.
- **Approvers** (template rule 4'): every trip record holds the written travel authorization of the area's highest
  authority (lines 47-49); a booking accepts that role and `NONE`, plus the Secretary General where his Premium
  Fare form or his standing exception for IACHR Commissioners is relied on; refusals accept `NONE` (and the unused
  authorization's role); holds accept only the awaited role(s).
- **Reasons on a declined request.** The task instructions say that when the booking is not what the traveller asked
  for, the reason code gives why the request is declined. A refused business or first cabin accepts
  `ECONOMY_CLASS_REQUIRED`/`UPGRADE_NOT_ELIGIBLE` (or `PREMIUM_FARE_AUTHORIZED` beside it in `ocelot-spire`), not
  `LOWEST_FARE`; a refused personal date (`kapok-strand`) accepts the personal-change codes. A nonstop declined because
  the cheaper connection passes the $200 / four-hour test (`guava-ledge`, `heron-pampa`) accepts `LOWEST_FARE` beside
  the specific codes (lead's decision, the same in every plugin).
- **No hidden facts:** no scenario has `answer_key_inputs`; background offers are off (`background_offers: 0`).

| Scenario | Category | Expected decision (offer; cabin) | Reason | Approver | Clause (frozen lines of must_keep) |
|---|---|---|---|---|---|
| `agave-ridge` | easy | BOOK (united-economy; ECONOMY) | LOWEST_FARE | NONE or SECRETARY_GENERAL | CLASS_OF_SERVICE or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or OWN_APPROVAL or TRAVEL_CLASS (145-148, 324-335, 363-366, 294-296) |
| `basalt-vine` | easy | BOOK (latam-business; BUSINESS) | PREMIUM_FARE_AUTHORIZED or SENIOR_ROLE_ENTITLEMENT | CHIEF_OF_STAFF or NONE or SECRETARY_GENERAL | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or PREMIUM_TRAVEL or TRAVEL_CLASS (145-148, 324-335, 351-353, 47-49) |
| `condor-flats` | easy | BOOK (united-economy; ECONOMY) | ECONOMY_CLASS_REQUIRED or UPGRADE_NOT_ELIGIBLE | NONE or SECRETARY | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or PREMIUM_TRAVEL or TRAVEL_CLASS (145-148, 324-335, 149-151, 351-353, 47-49) |
| `dahlia-mesa` | easy | BOOK (latam-business; BUSINESS) | PREMIUM_FARE_AUTHORIZED | DIRECTOR or NONE or SECRETARY_GENERAL | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or PREMIUM_TRAVEL or TRAVEL_CLASS (149-151, 351-353, 324-335, 47-49) |
| `egret-shoal` | easy | BOOK (aeromexico-economy; ECONOMY) | LOWEST_FARE | DIRECTOR or NONE | ADVANCE_TIMELINESS or CLASS_OF_SERVICE or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or TRAVEL_CLASS (145-148, 324-335, 363-366, 47-49, 278-284) |
| `fern-canyon` | boundary_twin | BOOK (nonstop-economy or dallas-economy; ECONOMY) | ALTERNATE_ROUTE_WITHIN_MARGIN or COMPARABLE_FARE_OPTION or COST_SAVINGS or LOWEST_FARE | NONE or SECRETARY | COMPARABLE_OPTIONS or CONNECTIONS or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or PERSONAL_PREFERENCE or PERSONAL_PREFERENCE_DEFINITION (166-173, 387-396, 185-186, 47-49) |
| `guava-ledge` | boundary_twin | BOOK (dallas-economy; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or COST_SAVINGS or LOWEST_FARE | NONE or SECRETARY | COMPARABLE_OPTIONS or CONNECTIONS or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or PERSONAL_PREFERENCE or PERSONAL_PREFERENCE_DEFINITION (166-173, 387-396, 370-372, 185-186, 47-49) |
| `heron-pampa` | boundary_twin | BOOK (miami-economy; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or COST_SAVINGS or LOWEST_FARE | DIRECTOR or NONE | COMPARABLE_OPTIONS or CONNECTIONS or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or PERSONAL_PREFERENCE or PERSONAL_PREFERENCE_DEFINITION (166-173, 387-396, 370-372, 47-49) |
| `ibis-knoll` | boundary_twin | BOOK (miami-economy or nonstop-economy; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or CONNECTION_TOO_LONG or COST_SAVINGS or LOWEST_FARE | DIRECTOR or NONE | COMPARABLE_OPTIONS or CONNECTIONS or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or PERSONAL_PREFERENCE or PERSONAL_PREFERENCE_DEFINITION (166-173, 387-396, 370-372, 47-49) |
| `jacaranda-cove` | boundary_twin | BOOK (saturday-avianca; ECONOMY) | ALTERNATE_ROUTE_WITHIN_MARGIN or COMPARABLE_FARE_OPTION or LOWEST_FARE or PERSONAL_COST_PAID_BY_TRAVELER | DIRECTOR or NONE | COMPARABLE_OPTIONS or OFFICIAL_WITH_PERSONAL or PERMISSIBLE_CHANGES or PERSONAL_COSTS (573-583, 585-592, 593-597, 166-173, 47-49) |
| `kapok-strand` | boundary_twin | BOOK (monday-avianca; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or PERSONAL_CHANGE_NOT_ALLOWED or PERSONAL_TRAVEL_NOT_COVERED | DIRECTOR or NONE | COMPARABLE_OPTIONS or OFFICIAL_WITH_PERSONAL or PERMISSIBLE_CHANGES or PERSONAL_COSTS (573-583, 585-592, 166-173, 47-49) |
| `llama-terrace` | multi_rule | BOOK (united-business; BUSINESS) | PREMIUM_FARE_AUTHORIZED or SENIOR_ROLE_ENTITLEMENT | ASSISTANT_SECRETARY_GENERAL or NONE or SECRETARY_GENERAL | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or OWN_APPROVAL or PREMIUM_TRAVEL or TRAVEL_CLASS (145-148, 324-335, 351-353, 294-296) |
| `mango-quarry` | multi_rule | BOOK (aeromexico-economy; ECONOMY) | LATE_PURCHASE_APPROVED or LOWEST_FARE | DIRECTOR or NONE | ADVANCE_TIMELINESS or CLASS_OF_SERVICE or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or TRAVEL_CLASS (145-148, 324-335, 363-366, 47-49, 278-284) |
| `nopal-harbor` | multi_rule | BOOK (united-economy or american-economy; ECONOMY) | ALTERNATE_ROUTE_WITHIN_MARGIN or COMPARABLE_FARE_OPTION or LOWEST_FARE or LOYALTY_PROGRAM_PREFERENCE | DIRECTOR or NONE | CLASS_OF_SERVICE or COMPARABLE_OPTIONS or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or PERSONAL_PREFERENCE or PERSONAL_PREFERENCE_DEFINITION or SELECTION_OF_CARRIER or TRAVEL_CLASS (398-401, 166-173, 387-396, 159-162, 363-366, 47-49) |
| `ocelot-spire` | multi_rule | BOOK (united-business; BUSINESS) | PREMIUM_FARE_AUTHORIZED or UPGRADE_NOT_ELIGIBLE | DIRECTOR or NONE or SECRETARY_GENERAL | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or PREMIUM_TRAVEL or TRAVEL_CLASS (149-151, 351-353, 324-335, 47-49) |
| `puma-lagoon` | hidden_clause | BOOK (avianca-flexible; ECONOMY) | FULL_ECONOMY_FARE_AUTHORIZED or SENIOR_ROLE_ENTITLEMENT | NONE or SECRETARY or SECRETARY_GENERAL | HUMAN_RIGHTS_COMMISSIONERS (638-642, 47-49) |
| `quetzal-bank` | hidden_clause | BOOK (delta-economy; ECONOMY) | ECONOMY_CLASS_REQUIRED or UPGRADE_NOT_ELIGIBLE | DIRECTOR or NONE | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or OAS_TRAVELER or PAYMENT_RESTRICTED_INSTITUTIONS or PREMIUM_TRAVEL or TRAVEL_CLASS (79-80, 644-649, 324-335, 149-151, 47-49) |
| `rhea-dune` | distractor | BOOK (jetblue-economy; ECONOMY) | ANCILLARY_FEES_EXCLUDED or LOWEST_FARE | CHIEF_OF_STAFF or NONE | ANCILLARY_FEES or CLASS_OF_SERVICE or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or TRAVEL_CLASS (425-430, 363-366, 145-148, 324-335) |
| `sisal-crest` | distractor | BOOK (avianca-economy; ECONOMY) | ECONOMY_CLASS_REQUIRED or UPGRADE_NOT_ELIGIBLE | DIRECTOR or NONE | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or PREMIUM_TRAVEL or TRAVEL_CLASS (145-148, 324-335, 149-151, 351-353, 47-49) |
| `tapir-hollow` | refusal | REFUSE (none; NONE) | OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED | NONE | PERSONAL_VACATION (719-727) |
| `urchin-bay` | refusal | REFUSE (none; NONE) | OUTSIDE_POLICY_SCOPE or THIRD_PARTY_TICKET_COVERS_TRIP | DIRECTOR or NONE | THIRD_PARTY_DEVIATIONS (602-606, 47-49) |
| `vicuna-marsh` | flag | FLAG_FOR_APPROVAL (dallas-economy or nonstop-economy; ECONOMY) | APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT | DIRECTOR or NOT_NAMED or PROCUREMENT_DEPARTMENT or SECRETARY | COMPARABLE_OPTIONS or CONNECTIONS or LOWEST_LOGICAL_FARE or LOWEST_LOGICAL_FARE_DEFINITION or PERSONAL_PREFERENCE or PERSONAL_PREFERENCE_DEFINITION (166-173, 387-396, 185-186, 47-49) |
| `wren-caldera` | flag | FLAG_FOR_APPROVAL (latam-business; BUSINESS) | APPROVAL_REQUIRED | SECRETARY_GENERAL | CABIN_EXCEPTIONS or CLASS_OF_SERVICE or PREMIUM_TRAVEL or TRAVEL_CLASS (351-353, 149-151, 324-335) |
| `yucca-strait` | flag | FLAG_FOR_APPROVAL (aeromexico-economy; ECONOMY) | ADVANCE_PURCHASE_TOO_LATE or APPROVAL_REQUIRED | DIRECTOR or SECRETARY | ADVANCE_TIMELINESS or TRAVEL_ARRANGEMENTS (278-284, 84-85, 47-49) |

Mix (EDGE_CASES.md 5.2, 24 row): 5 easy, 6 boundary twins, 4 multi-rule, 2 hidden clause, 2 distractor, 2 refusal,
3 flags (12.5%; the 15% cap is 3). Decisions: 19 BOOK (4 business, 15 economy), 2 REFUSE, 3 FLAG. The one unclear
phrase is "savings of $200 or more" (`vicuna-marsh`: at exactly $200 the nonstop is comparable and the connection is
required; twins `fern-canyon` $199 and `guava-ledge` $201). `wren-caldera` (form signed by the Chief of Staff, not
the Secretary General) and `yucca-strait` (authorized 20 days before travel, no late-purchase approval) are
approval-required holds, never "no compliant offer". Degenerate agents: always-cheapest (cheapest seat, `LOWEST_FARE`,
`NONE`) passes 9 of 24; always-flag passes 1.

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller, route, dates, purpose, requested cabin, routing, airline and fare, bag fees, sign-offs, a ticket already bought by others | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date (one way, or round trip with `return_date`): the pinned scenario offers plus seeded background offers on those searches only; a search the case does not pin lists nothing and says so | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-oas-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this handbook's scenario ids, approvers, sections and trip record.
- `src/plugin/`: `world.py` (the simulated world: real airports and airline hubs, distance-based times
  and fares, hash-seeded background offers and opaque offer ids), `scenarios.py`, `guide.py`,
  `answer.py`, `tools.py`, `rules.py` (this handbook's rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of `world.py`, `scenarios.py`, `guide.py`, `answer.py` and
  `rules.py`, plus `booking.py` (`verify_task`) and `tools.py` (`verify_input`, `verify_output`).
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this handbook's settings,
  `tests/build_scenarios.py` writes the scenario files, and `tests/BUILD_NOTES.md` records the build.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
# from a NanoAgent checkout:
nanoagent plugin inspect <this folder>
```

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`).
