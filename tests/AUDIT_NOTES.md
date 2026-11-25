# Independent audit: oas-flight-policy (2026-11-25)

Audited build 729c418 against `pilot_work/tier_plan/build/WAVE3_AUDIT_BRIEF.md`, the wave 3 build brief's 12 lessons,
MASTER_PLAN section 4 and EDGE_CASES sections 1-3 and 5. I read the frozen handbook in full (`src/plugin/data/policy.txt`,
8,215 words). Then I dumped `get_trip`, every pinned `search_flights` output (including the working-day search of the two
personal-days cases) and every answer key. I re-derived each answer from the handbook and those outputs only, before I
read `rules.py`. "$2002" at line 167 means $200 with footnote marker 2 (lines 185-186, and line 390 repeats "$200").

**Verdict: pass after fixes.** The keyed bookings satisfy every constraint the handbook states, in all 24 scenarios. The
defects were false-failure risks: two senior-official cases that a cautious reader could hold, and two preference cases
whose strict lowest-fare reading was not accepted. The worlds stay the same except for one added sign-off in each of
two trip records. No ids or categories changed.

## Defects found and fixed

| Scenario | Problem | Fix |
|---|---|---|
| basalt-vine (Chair, business), llama-terrace (ASG, business) | Lines 324-335 exempt the three officials from economy, then say "Any requests for advance purchase by GS/OAS of a different class of service must be approved in advance and in writing by the Secretary General". 2.21 (149-151) calls any non-economy travel "an exception under this policy", and 6.3 (351-353) needs the SG's Premium Fare form, without carving out the three. A careful reader can hold the business fare for the SG's approval. That is a second defensible decision, and the schema accepts only one decision per case. | Put the approval on file: each record now carries a `PREMIUM_FARE_FORM` from the Secretary General for business (basalt 2027-01-15, llama 2027-03-05), and each request says so in one clause ("The Secretary General approved business class for this trip in writing"). Both readings now BOOK the cheapest business fare (unchanged offers). Accept sets add PREMIUM_FARE_AUTHORIZED, SECRETARY_GENERAL (4': two sign-offs relied on, plus NONE), PREMIUM_TRAVEL and CABIN_EXCEPTIONS. `rules.exempt` now raises on a senior official's premium request without that approval, so a future case cannot reopen the ambiguity. llama-terrace still tests own approval (5.4, lines 294-296): the ASG signed his own travel request. |
| fern-canyon (nonstop $199 above the connection) | Only the nonstop was accepted. "Lowest available fares must be used whenever possible" (lines 161, 365) is the handbook's only mandatory wording on fares. The comparable-options and personal-preference text (166-167, 387-391) says how a non-LLF choice "will be reported", and does not say outright that the traveller is entitled to it. An agent that holds to the lowest fare, reads "if not, book what the policy calls for" and books the $310 connection is defensible. | Accept both offers. Reasons add LOWEST_FARE (the ground is the lowest-fare rule itself, so lesson 12 allows it) and COST_SAVINGS. The $200 boundary still bites: guava-ledge ($201) accepts only the connection, and vicuna-marsh ($200) is the flag. |
| nopal-harbor (United $140 above American) | The same mechanism: a carrier request is "subject to the Personal Preference criteria" (398-401), so the strict lowest-fare reading books American at $198. Accepting it in fern-canyon but not here would be inconsistent. | Accept both offers. Reasons add LOWEST_FARE, and clauses add the lowest-fare sections (TRAVEL_CLASS, CLASS_OF_SERVICE, LOWEST_LOGICAL_FARE, LOWEST_LOGICAL_FARE_DEFINITION). |

Always-cheapest baseline (`MAX_PASS_ALWAYS_LOWEST`): **7 -> 9 of 24** (37.5%, within the ~40% target). The two
additions are fern-canyon and nopal-harbor. The always-flag baseline stays at 1.

## Builder's open items, settled

- **basalt-vine / llama-terrace:** the hold under 6.1 is defensible (see above). Fixed by putting the approval on
  file rather than by keying a hold, because the exemption reading is also strong: the rail rule 6.1.1 (lines
  337-344) exempts the same three and requires the SG's written authorization only from others, and "reported to the
  Permanent Council" echoes the reporting of non-compliance (148, footnote 3). The cost is that no case now tests the
  exemption on a premium cabin alone. agave-ridge and rhea-dune still test it on economy.
- **fern-canyon:** the connection is defensible. Accepted (see above).
- **urchin-bay:** REFUSE is right and is the only sane answer. "should only cover any additional expenses paid to
  deviate" sets a ceiling on what the GS/OAS pays, and "In no case ... should exceed the cost(s) of what the GS/OAS
  would pay if the initial travel plans did not exist" is absolute. The IDB round trip (out March 1, back March 6)
  already spans the March 5 workshop, so no deviation exists. BOOK would double-ticket the traveller, and a hold has
  nothing to wait for. Left as built.
- **Uniform request wording** ("if the policy lets me have it without any extra justification; if not, book what the
  policy calls for"): it is a little formal, but it is natural for a staff member who knows there is a justification
  step. It gives no threshold and no section. It only echoes that justification exists, which the agent cannot use
  without the handbook's $200 and four-hour tests. It does its job: it turns the traveller-judgment clause (171-173,
  394-396) into one answer on each side of the allowance. Left as built.
- **egret-shoal / yucca-strait (5.2):** I checked the second deadline too, "approved no later than fifteen (15) days
  before the beginning of the following quarter", which falls on December 17 for a January 4 trip. egret-shoal
  (December 14) and yucca-strait (December 15) both meet it, and mango-quarry (December 21) misses it but has the
  late-purchase approval on file. So it changes no answer. Left as built.

## Checked and left as built

- Every other key matches my blind derivation: agave-ridge, condor-flats, dahlia-mesa, egret-shoal, guava-ledge,
  heron-pampa (exactly 240 minutes is "not more than four hours"; the flying-time measure gives the same answer),
  ibis-knoll (241: both offers, correct), jacaranda-cove, kapok-strand, mango-quarry, ocelot-spire, puma-lagoon,
  quetzal-bank, rhea-dune, sisal-crest, tapir-hollow, urchin-bay, vicuna-marsh, wren-caldera and yucca-strait.
  Every keyed offer lands before `work_starts`.
- **Flag** vicuna-marsh: genuinely unclear. The two inclusive $200 tests in one paragraph give different tickets at
  exactly $200, and both offers are held. wren-caldera and yucca-strait are approval holds, and their approvers are
  only the awaited roles (4').
- **Twins** differ in one fact: fern/vicuna/guava (nonstop $509/$510/$511), heron/ibis (layover 175/176),
  jacaranda/kapok (Saturday $580/$581), and egret/yucca/mango (signing date, and the late approval).
- **jacaranda-cove**, exactly $200 on a personal date change: 8.1.1 cites only "the comparable options" ("not higher
  than $200"). The "$200 or more" connection test concerns routings, not the traveller's own dates. So the case is not
  a second instance of the vicuna-marsh flag. Residual risk: low.
- **Leaks:** no rule wording or threshold in any request (`test_lint` passes). The ocelot-spire "about $300 more"
  is a fact about the offers. The decline-reason sentence is the last line of the book task's instructions.
- **Hosted cap:** the builder's note stands. The two personal-days cases need a second search and run about 71k
  tokens, over the 65,536 hosted cap.

## Acceptance outputs (after fixes)

```
uv run pytest -q                        196 passed, 3 skipped
uv run ruff check .                     All checks passed!
uv lock --check                         Resolved 42 packages
python3 ../_template/check_shared.py .  : ok
stock_verify.py . (stock Python)        24 scenarios, 0 failures
nanoagent plugin inspect . (stock)      exit 0
```

Both `rules.py` copies are byte-identical, and the scenario JSON was regenerated with `tests/build_scenarios.py`.
README rows for the four changed scenarios and the baseline sentence are updated.
