"""The answer key's rules for the Travel Policy of the General Secretariat of the Organization of American States
(Administrative Memorandum 122, Appendix A), as exact integer code. Byte-identical in src/plugin/rules.py and
verifier/rules.py; it imports only modules a verifier may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. Where the text leaves an answer
open, the rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each unclear phrase
at most once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a new scenario cannot
fall silently into untested logic.

The duration hook. The handbook has no absolute flight-duration threshold: no cabin, fare or approval depends on
how long a flight is. Its one time limit is relative, the four hours that a cheaper routing may add to the one-way
air travel time (lines 166-169, 370-372 and 391-393), and it is coded below as EXTRA_MINUTES, measured as the
elapsed time from first departure to last arrival against the fastest nonstop, and checked against the arrival
difference as well (every scenario leaves at the same time, so the two agree; rules raise if they ever differ).
So DURATION_RULES is empty and over() raises.

Money. Line 167 prints "$2002": the amount $200 with the marker of footnote 2 (lines 185-186, "The amount of
US$200"). Line 390 repeats it as "$200". Two tests use it:
- comparable options (lines 166-167, 389-391): an alternative is comparable when its cost is "not higher than
  $200" above the lowest logical fare (inclusive: $200.00 is still comparable);
- connections required (lines 167-169, 391-393): a cheaper routing is required when it saves "$200 or more"
  (inclusive) without adding more than four hours (inclusive: exactly 240 minutes still counts).
The two tests overlap at exactly $200: the dearer nonstop is then comparable and the cheaper connection is
required. That is a flag (UNCLEAR_PHRASE). Below $200 only the comparable test speaks; above it only the
requirement does.

The traveller's choice. Lines 171-173 and 394-396 let travellers "use their judgment" beyond the allowance, but
"Those cases will be reported and may require additional justification". Every request with a preference in this
plugin says the traveller wants the preferred option only if it needs no extra justification and otherwise wants
what the policy calls for, so a preference within the allowance is booked and one beyond it is declined.

Approvers. Lines 47-49 (and 94-96): every trip is authorized in advance and in writing by the area's highest
authority (Director or Secretary, the Chief of Staff or the Secretary General); line 294-296 lets only the
Secretary General, the Assistant Secretary General and the Chair of the Permanent Council approve their own.
Under the template's rule 4' (SYNC_NOTES.md), a booking whose sign-offs are already on file accepts each of those
roles and NONE; a refusal does not use the trip authorization, so it accepts NONE and that role (rule 4(b)); a
hold accepts only the role(s) it awaits (NOT_NAMED where the handbook names none).
"""

from contract import (
    Approver,
    Cabin,
    Clause,
    Decision,
    Position,
    Purpose,
    ReasonCode,
    Routing,
    SignOffSubject,
)

from .world import days_between, utc_minute

HANDBOOK = "Travel Policy of the General Secretariat of the Organization of American States (AM 122, Appendix A)"

# Each closed-list section and the heading line it names in the frozen text (tests check every heading is there).
CLAUSE_HEADINGS = {
    Clause.INTRODUCTION: "Introduction:",
    Clause.POLICY_SUMMARY: "1. Travel Policy Summary",
    Clause.DEFINITIONS: "2. Definitions",
    Clause.OAS_TRAVELER: "2.3 OAS Traveler: includes Staff Members, Time Based Natural CPRs, SOCs, guests and every person",
    Clause.AUTHORIZED_APPROVER: "2.5 Authorized Approver: under this travel policy, the corresponding area's highest "
                                "authority (Director",
    Clause.TRAVEL_CLASS: "2.20 Travel Class: With the exception of the Secretary General, the Assistant Secretary "
                         "General, and the",
    Clause.PREMIUM_TRAVEL: "2.21 Premium Travel: travel completed by any means in a Travel Class other than Economy; "
                           "this is",
    Clause.LOWEST_LOGICAL_FARE_DEFINITION: "2.24 Lowest Logical Fare (LLF): lowest logical fares include any "
                                           "reasonable itineraries from the",
    Clause.PERSONAL_PREFERENCE_DEFINITION: "2.25 Personal preference: within this policy, if LLF as presented by the "
                                           "designated TMC is not selected",
    Clause.COMPARABLE_OPTIONS: "2.26 Comparable Options: options will be comparable as long as the total cost for "
                               "alternative fares are",
    Clause.RAIL_TRAVEL: "2.27 Rail/Train Travel: with the exception of the Secretary General, Assistant Secretary "
                        "General and the",
    Clause.MANDATORY_TRAVEL_AGENCY: "4. Mandatory use of the designated Travel Management Company (TMC)",
    Clause.TRAVEL_ARRANGEMENTS: "5. Travel Arrangements",
    Clause.ADVANCE_TIMELINESS: "5.2. Advance Authorization - Timeliness: under normal circumstances and as required "
                               "by other",
    Clause.AUTHORIZING: "5.3. Authorizing: all OAS Official Quarterly Travel Plans must be approved by the traveler's "
                        "supervisor",
    Clause.OWN_APPROVAL: "5.4. With the exception of the Secretary General, the Assistant Secretary General and the "
                         "Chair of the",
    Clause.TRANSPORTATION: "6. Transportation Accommodations (Air, Rail, Ground or Sea)",
    Clause.CLASS_OF_SERVICE: "6.1. Class of Service: all travelers must comply with the requirement -- established by "
                             "the OAS",
    Clause.FARES: "6.2. Fares: all airfares for all approved GS/OAS must be purchased in accordance to this travel "
                  "policy,",
    Clause.CABIN_EXCEPTIONS: "6.3. Class of Service Exceptions: to process a request for exception, a "
                                        "filled Premium Fare",
    Clause.PRICE_MATCH: "6.4. Price Match Guarantee: the Department of Procurement will negotiate a price match "
                        "guarantee",
    Clause.LOWEST_LOGICAL_FARE: "6.5. Lowest Logical Fare (LLF): lowest logical fares include any reasonable "
                                "itineraries that are available",
    Clause.CONNECTIONS: "6.6. Connections: for the purpose of finding the LLF, the TMC may add one or more stops where",
    Clause.PERSONAL_PREFERENCE: "6.7. Personal preference: within this policy, if LLF as presented by the designated "
                                "TMC is not selected",
    Clause.SELECTION_OF_CARRIER: "6.8. Selection of Carrier: the selection of the LLF should be independent of the "
                                 "carrier. Unless it is",
    Clause.ALTERNATE_AIRPORTS: "6.9. Use of Alternate Airports or Departure Locations: the selection of the LLF should "
                               "be independent",
    Clause.AIRLINE_UPGRADES: "6.10. Airline Upgrades: upgrades to other than Economy Class using personal funds, "
                             "points, miles and",
    Clause.ANCILLARY_FEES: "6.11. Airline Ancillary Services Fees: although ancillary fees are a fairly new component, "
                           "most major",
    Clause.FREQUENT_FLIER: "7.1. Frequent Flier Miles: GS/OAS permits travelers to retain their frequent flyer mileage "
                           "points",
    Clause.SPECIAL_CIRCUMSTANCES: "8. Special Circumstances and Other Considerations",
    Clause.OFFICIAL_WITH_PERSONAL: "8.1. Official Travel Combined with Personal Trip: at times a traveler/passenger may "
                                   "wish to combine",
    Clause.PERMISSIBLE_CHANGES: "8.1.1. Permissible changes: personal changes will only be allowed if the official "
                                "itinerary remains",
    Clause.PERSONAL_COSTS: "8.1.2. Per diem will not be paid if the traveler is not on official duty the day or "
                           "applicable night",
    Clause.THIRD_PARTY_DEVIATIONS: "8.2. Deviations from Travel Plans paid by Third Parties: if passenger is travelling "
                                   "or has already",
    Clause.FLYING_TOGETHER: "8.5. Employees Flying Together: there are specific restrictions related to insurance and "
                            "risk regarding",
    Clause.HUMAN_RIGHTS_COMMISSIONERS: "8.6. Human Rights Commissioners: According to request GS/CIDH/10/09 and until "
                                       "further notice, the",
    Clause.PAYMENT_RESTRICTED_INSTITUTIONS: "8.7. Staff of Institutions unable to receive payments in their name: from "
                                            "time to time, the GS/OAS may",
    Clause.GROUPS_AND_MEETINGS: "11. General Assembly, Groups and Meetings",
    Clause.PERSONAL_VACATION: "12. Personal/Vacation Travel",
    Clause.PERSONAL_ACCOUNTABILITY: "13. Personal Accountability",
}

# No absolute flight-duration threshold in this handbook (see the module docstring).
DURATION_RULES = ()

# Handbook-specific conventions shown by booking_requirements, beyond the template's (none here).
CONVENTIONS = ()

# Lines 166-167 and 389-391 ("not higher than $200", footnote 2: US$200): the comparable-options allowance.
ALLOWANCE_CENTS = 20_000
# Lines 167-169 and 391-393: a cheaper routing is required when it saves "$200 or more" without extending the total
# one-way air travel time "by more than four (4) hours"; lines 370-372: stops added for the LLF "should not increase
# the travelling or layover time by more than 4-hours each way".
SAVINGS_CENTS = 20_000
EXTRA_MINUTES = 240
# Lines 280-284: travel plans "should be approved no later than three (3) weeks prior to the travel date"; fares
# purchased late "would therefore require additional written approval from the duly authorized official in the
# requesting area".
LEAD_DAYS = 21
# Lines 145-146, 324-328, 294-296: the three officials outside the economy rule, who may also approve their own trip.
EXEMPT = {
    Position.SECRETARY_GENERAL: Approver.SECRETARY_GENERAL,
    Position.ASSISTANT_SECRETARY_GENERAL: Approver.ASSISTANT_SECRETARY_GENERAL,
    Position.PERMANENT_COUNCIL_CHAIR: Approver.PERMANENT_COUNCIL_CHAIR,
}
# Lines 47-49, 84-85, 94-96: the area's highest authority (Director or Secretary, Chief of Staff or Secretary General).
AUTHORIZERS = (Approver.DIRECTOR, Approver.SECRETARY, Approver.CHIEF_OF_STAFF, Approver.SECRETARY_GENERAL)
# Lines 283-284: "the duly authorized official in the requesting area" (lines 84-85: Director or Secretary).
AREA_OFFICIALS = [Approver.DIRECTOR, Approver.SECRETARY]
# Lines 576-577: personal days need "prior authorization ... from either the Director or the Secretary".
PERSONAL_AUTHORIZERS = (Approver.DIRECTOR, Approver.SECRETARY)
CABIN_RANK = {Cabin.ECONOMY: 1, Cabin.PREMIUM_ECONOMY: 2, Cabin.BUSINESS: 3, Cabin.FIRST: 4}

UNCLEAR_REASONS = [ReasonCode.UNCLEAR_POLICY_TEXT, ReasonCode.APPROVAL_REQUIRED]
UNCLEAR_PHRASE = "savings of $200 or more"

LOWEST_CLAUSES = [Clause.TRAVEL_CLASS, Clause.CLASS_OF_SERVICE, Clause.LOWEST_LOGICAL_FARE,
                  Clause.LOWEST_LOGICAL_FARE_DEFINITION]
CLASS_CLAUSES = [Clause.TRAVEL_CLASS, Clause.CLASS_OF_SERVICE, Clause.PREMIUM_TRAVEL, Clause.CABIN_EXCEPTIONS]
PREFERENCE_CLAUSES = [Clause.COMPARABLE_OPTIONS, Clause.PERSONAL_PREFERENCE, Clause.PERSONAL_PREFERENCE_DEFINITION]
PERSONAL_CLAUSES = [Clause.OFFICIAL_WITH_PERSONAL, Clause.PERMISSIBLE_CHANGES]


def over(rule, offer):
    """The duration hook: this handbook has no duration threshold, so every rule name is unknown."""
    raise ValueError(f"this handbook has no duration rule {rule!r}")


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted(offer.offer_id for offer in offers),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(clauses),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def one(offers, what):
    if len(offers) != 1:
        raise ValueError(f"{what}: {len(offers)} offers tie or none is listed; not modelled")
    return offers[0]


def signed(trip, subject):
    return [record for record in trip.sign_offs if record.subject == subject]


def on_route(trip, offers, date):
    return [offer for offer in offers if offer.segments[0].origin == trip.origin.code
            and offer.segments[-1].destination == trip.destination.code and offer.segments[0].depart_local[:10] == date]


def arrival(offer):
    return offer.segments[-1].arrive_local


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers on its searches: the decision, and every accepted offer id, cabin,
    reason, approver and section. ``hidden`` (the scenario's answer_key_inputs) is unused by this handbook."""
    if hidden:
        raise ValueError("this handbook's scenarios carry no answer_key_inputs")
    if trip.return_date:
        raise ValueError("a round-trip ticket is not modelled")
    if trip.purpose_kind == Purpose.VACATION:
        if trip.sign_offs:
            raise ValueError("a vacation with sign-offs on file is not modelled")
        return answer(Decision.REFUSE, [], [ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE],
                      [Approver.NONE], [Clause.PERSONAL_VACATION],
                      "Lines 721-727: personal travel not associated with an official trip is made through the "
                      "leisure section of the travel agency, the corporate travel agents should not book it, and all "
                      "its costs are the traveller's and non-reimbursable. The GS/OAS buys no ticket.")
    if trip.purpose_kind == Purpose.HOME_LEAVE:
        raise ValueError("statutory travel (lines 27-31, 75-78) is not modelled")
    authorizations = signed(trip, SignOffSubject.TRAVEL_AUTHORIZATION)
    if len(authorizations) != 1:
        raise ValueError("every official trip holds one written travel authorization (lines 47-49)")
    authorization = authorizations[0]
    if authorization.name == trip.traveller_name:
        if EXEMPT.get(trip.position) != authorization.role:
            raise ValueError("a traveller approving their own trip outside lines 294-296 is not modelled")
    elif authorization.role not in AUTHORIZERS:
        raise ValueError("a travel authorization by someone other than the area's highest authority is not modelled")
    if days_between(authorization.signed_on, trip.booking_date) < 0:
        raise ValueError("a sign-off dated after today")
    # Rule 4': a booking accepts NONE beside every sign-off on file that it relies on; rule 4(b) for a refusal.
    roles = [Approver.NONE, authorization.role]
    if trip.ticket_from_others:
        if not trip.ticket_from_others_suffices:
            raise ValueError("a third-party ticket that leaves a deviation to pay is not modelled")
        return answer(Decision.REFUSE, [], [ReasonCode.THIRD_PARTY_TICKET_COVERS_TRIP, ReasonCode.OUTSIDE_POLICY_SCOPE],
                      roles, [Clause.THIRD_PARTY_DEVIATIONS],
                      "Lines 602-606: when the traveller already has travel paid by someone else, the GS/OAS portion "
                      "covers only the additional expenses of deviating from those plans; the ticket on file already "
                      "takes the traveller to the work and home on the days needed, so there is nothing to buy.")
    travel = [offer for offer in on_route(trip, offers, trip.travel_date) if offer.seats_available]
    if trip.business_travel_date != trip.travel_date:
        work = [offer for offer in on_route(trip, offers, trip.business_travel_date) if offer.seats_available]
    else:
        work = travel
    if any(arrival(offer) >= trip.work_starts for offer in work):
        raise ValueError("an offer that lands after the work starts is not modelled")
    result = booking(trip, travel, offers, roles)
    return timeliness(trip, authorization, result)


def timeliness(trip, authorization, result):
    """Lines 278-284: travel plans approved no later than three weeks before the travel date; a late purchase needs
    additional written approval from the duly authorized official in the requesting area."""
    lead = days_between(authorization.signed_on, trip.travel_date)
    late = signed(trip, SignOffSubject.LATE_PURCHASE_APPROVAL)
    if lead >= LEAD_DAYS:
        if late:
            raise ValueError("a late-purchase approval on a timely trip is not modelled")
        if lead < LEAD_DAYS + 7:
            # Close to the line, the section that sets it is an accepted citation as well.
            result["clauses"] = by_value([*result["clauses"], Clause.ADVANCE_TIMELINESS])
        return result
    if result["decision"] != Decision.BOOK or trip.position in EXEMPT:
        raise ValueError("a late trip that is not a plain booking is not modelled")
    if late:
        signers = [record.role for record in late]
        if any(role not in AREA_OFFICIALS for role in signers):
            raise ValueError("a late-purchase approval by someone outside the requesting area is not modelled")
        result["reason_codes"] = by_value([*result["reason_codes"], ReasonCode.LATE_PURCHASE_APPROVED])
        result["approvers"] = by_value([*result["approvers"], *signers])
        result["clauses"] = by_value([*result["clauses"], Clause.ADVANCE_TIMELINESS])
        result["explanation"] += (f" Lines 280-284: the trip was authorized {lead} days before the travel date, under "
                                  "three weeks, and the additional written approval for the late purchase is on file.")
        return result
    if len(result["offer_ids"]) != 1:
        raise ValueError("a late hold with more than one accepted offer is not modelled")
    return {
        "decision": Decision.FLAG_FOR_APPROVAL,
        "offer_ids": result["offer_ids"],
        "cabins": result["cabins"],
        "reason_codes": by_value([ReasonCode.APPROVAL_REQUIRED, ReasonCode.ADVANCE_PURCHASE_TOO_LATE]),
        "approvers": by_value(AREA_OFFICIALS),
        "clauses": by_value([Clause.ADVANCE_TIMELINESS, Clause.TRAVEL_ARRANGEMENTS]),
        "unclear_phrase": "",
        "explanation": (f"Lines 280-284: the trip was authorized {lead} days before the travel date, later than three "
                        "weeks before it, so the purchase is late and needs additional written approval from the duly "
                        "authorized official in the requesting area (the Director or Secretary, lines 84-85); none is "
                        "on file. Hold the fare that would otherwise be bought: " + result["explanation"]),
    }


def booking(trip, travel, offers, roles):
    economy = [offer for offer in travel if offer.cabin == Cabin.ECONOMY]
    if trip.business_travel_date != trip.travel_date:
        return personal(trip, offers, economy, roles)
    if trip.traveller_pays_difference:
        raise ValueError("a traveller paying a difference outside personal days is not modelled")
    if trip.position in EXEMPT:
        return exempt(trip, travel, economy, roles)
    if trip.requested_cabin != Cabin.ECONOMY:
        return premium_request(trip, travel, economy, roles)
    if trip.requested_refundable:
        return full_fare(trip, economy, roles)
    return economy_request(trip, economy, roles)


def plain(trip):
    return (trip.requested_routing == Routing.ANY and not trip.requested_airline and not trip.requested_refundable
            and not trip.checked_bag_fees)


def lowest(economy):
    """The lowest logical fare (lines 159-162, 363-366, 370-372): the cheapest economy offer among the reasonable
    itineraries, a connection counting only when it adds no more than four hours to the fastest nonstop."""
    nonstops = [offer for offer in economy if offer.stops == 0]
    if not nonstops:
        raise ValueError("a route with no economy nonstop is not modelled")
    fastest = min(offer.elapsed_minutes for offer in nonstops)
    logical = [offer for offer in economy if offer.stops == 0 or offer.elapsed_minutes - fastest <= EXTRA_MINUTES]
    return one(cheapest(logical), "lowest logical fare")


def extra_minutes(connection, nonstop):
    """Lines 168-169: how much the connection extends the total one-way air travel time, measured both as elapsed
    time and as the arrival difference; both must agree on which side of four hours it falls."""
    measures = {connection.elapsed_minutes - nonstop.elapsed_minutes,
                utc_minute(connection.segments[-1].arrive_utc) - utc_minute(nonstop.segments[-1].arrive_utc)}
    if len({value <= EXTRA_MINUTES for value in measures}) != 1:
        raise ValueError("an extension within four hours on one measure and over on another is not modelled")
    return max(measures)


def exempt(trip, travel, economy, roles):
    """Lines 145-146 and 324-328: the Secretary General, the Assistant Secretary General and the Chair of the
    Permanent Council are outside the economy rule; lines 294-296: they may approve their own trip."""
    if trip.requested_routing != Routing.ANY or trip.requested_airline or trip.requested_refundable:
        raise ValueError("a senior official's routing, airline or fare request is not modelled")
    clauses = [Clause.TRAVEL_CLASS, Clause.CLASS_OF_SERVICE]
    if roles[-1] == EXEMPT[trip.position]:
        clauses.append(Clause.OWN_APPROVAL)
    if trip.requested_cabin == Cabin.ECONOMY:
        chosen = lowest(economy)
        reasons, notes = [ReasonCode.LOWEST_FARE], "the traveller asks for the lowest economy fare"
        clauses += [Clause.LOWEST_LOGICAL_FARE, Clause.LOWEST_LOGICAL_FARE_DEFINITION]
        if trip.checked_bag_fees:
            reasons.append(ReasonCode.ANCILLARY_FEES_EXCLUDED)
            clauses.append(Clause.ANCILLARY_FEES)
            notes += ("; lines 427-430: ancillary fees, baggage included, are left out when the lowest fare is found "
                      "and are reimbursed separately, so the bag fees do not change which fare is lowest")
        return answer(Decision.BOOK, [chosen], reasons, roles, clauses,
                      f"Lines 145-146 and 324-328: the traveller is one of the three officials outside the economy "
                      f"rule; {notes}: {chosen.carrier} at {chosen.fare_cents} cents.")
    if trip.checked_bag_fees:
        raise ValueError("bag fees on a premium request are not modelled")
    wanted = [offer for offer in travel if offer.cabin == trip.requested_cabin]
    chosen = one(cheapest(wanted), "cheapest fare in the requested cabin")
    return answer(Decision.BOOK, [chosen], [ReasonCode.SENIOR_ROLE_ENTITLEMENT], roles, clauses,
                  "Lines 145-146 and 324-328: tickets for the Secretary General, the Assistant Secretary General and "
                  "the Chair of the Permanent Council are not held to economy class, so the cabin asked for is booked "
                  "at its cheapest fare; lines 294-296 let these three approve their own travel.")


def premium_request(trip, travel, economy, roles):
    """Lines 149-151, 324-335 and 351-353: any class other than economy is an exception that needs a Premium Fare
    Authorization Form approved by the Secretary General."""
    if not plain(trip):
        raise ValueError("a premium request with another preference is not modelled")
    forms = signed(trip, SignOffSubject.PREMIUM_FARE_FORM)
    if not forms:
        chosen = lowest(economy)
        clauses = list(CLASS_CLAUSES)
        why = ("Lines 145-148 and 324-328: tickets paid for with the Organization's funds are bought in economy at the "
               "lowest logical fare; another class is an exception that needs a Premium Fare Authorization Form "
               "approved by the Secretary General (lines 149-151, 351-353), and none is on file")
        if trip.position in (Position.INVITED_EXPERT, Position.CONSULTANT):
            clauses += [Clause.OAS_TRAVELER, Clause.PAYMENT_RESTRICTED_INSTITUTIONS]
            why += ("; lines 79-80: a guest travelling with GS/OAS funds is an OAS traveller, and lines 648-649: the "
                    "GS/OAS buys the fare")
        return answer(Decision.BOOK, [chosen], [ReasonCode.ECONOMY_CLASS_REQUIRED, ReasonCode.UPGRADE_NOT_ELIGIBLE],
                      roles, clauses, f"{why}: the lowest economy fare, {chosen.carrier} at {chosen.fare_cents} cents.")
    form = one(forms, "premium fare form")
    wanted = [offer for offer in travel if offer.cabin == trip.requested_cabin]
    if form.role != Approver.SECRETARY_GENERAL:
        if form.cabin != trip.requested_cabin:
            raise ValueError("an unsigned form for another cabin is not modelled")
        held = one(cheapest(wanted), "cheapest fare in the requested cabin")
        return answer(Decision.FLAG_FOR_APPROVAL, [held], [ReasonCode.APPROVAL_REQUIRED], [Approver.SECRETARY_GENERAL],
                      CLASS_CLAUSES,
                      "Lines 351-352: the Premium Fare Authorization Form 'must be approved by the Secretary General' "
                      "(also lines 328-335); it was signed by someone else. Hold the cheapest fare in the cabin asked "
                      "for until the Secretary General approves it.")
    approvers = [*roles, Approver.SECRETARY_GENERAL]
    if CABIN_RANK[trip.requested_cabin] < CABIN_RANK[form.cabin]:
        raise ValueError("a request below the approved cabin is not modelled")
    covered = [offer for offer in travel if offer.cabin == form.cabin]
    chosen = one(cheapest(covered), "cheapest fare in the approved cabin")
    if trip.requested_cabin == form.cabin:
        return answer(Decision.BOOK, [chosen], [ReasonCode.PREMIUM_FARE_AUTHORIZED], approvers, CLASS_CLAUSES,
                      "Lines 149-151 and 351-353: the Premium Fare Authorization Form for this cabin is approved by the "
                      "Secretary General; the cheapest fare in that cabin.")
    return answer(Decision.BOOK, [chosen], [ReasonCode.UPGRADE_NOT_ELIGIBLE, ReasonCode.PREMIUM_FARE_AUTHORIZED],
                  approvers, CLASS_CLAUSES,
                  "Lines 149-151 and 351-353: the form the Secretary General approved names a lower cabin than the one "
                  "asked for; any other class needs its own approved form, so the cheapest fare in the approved cabin.")


def full_fare(trip, economy, roles):
    """Lines 638-642: the Secretary General authorized the elected IACHR Commissioners to buy full economy fares."""
    if trip.position != Position.IACHR_COMMISSIONER or trip.requested_routing != Routing.ANY or trip.requested_airline:
        raise ValueError("a refundable-fare request outside lines 638-642 is not modelled")
    full = one(cheapest([offer for offer in economy if offer.refundable]), "cheapest full economy fare")
    return answer(Decision.BOOK, [full], [ReasonCode.FULL_ECONOMY_FARE_AUTHORIZED, ReasonCode.SENIOR_ROLE_ENTITLEMENT],
                  [*roles, Approver.SECRETARY_GENERAL], [Clause.HUMAN_RIGHTS_COMMISSIONERS],
                  "Lines 638-640: the Secretary General authorized an exception allowing the elected IACHR Commissioner "
                  "to purchase full economy fares, and the commissioner asks for one; the cheapest refundable economy "
                  "fare.")


def economy_request(trip, economy, roles):
    """Lines 159-173, 363-396 and 398-401: the lowest logical fare, a preference within the $200 allowance, and a
    cheaper connection required when it saves $200 or more and adds no more than four hours."""
    if trip.checked_bag_fees or trip.requested_refundable:
        raise ValueError("bag fees or a refundable fare on an ordinary economy request are not modelled")
    llf = lowest(economy)
    if trip.requested_routing == Routing.NONSTOP:
        if trip.requested_airline:
            raise ValueError("two preferences at once are not modelled")
        return nonstop_request(trip, economy, llf, roles)
    if trip.requested_airline:
        preferred = one(cheapest([offer for offer in economy if offer.carrier == trip.requested_airline]),
                        "cheapest fare on the airline asked for")
        extra = preferred.fare_cents - llf.fare_cents
        if extra <= 0 or extra > ALLOWANCE_CENTS:
            raise ValueError("an airline request that is the lowest fare, or beyond the allowance, is not modelled")
        return answer(Decision.BOOK, [preferred], [ReasonCode.COMPARABLE_FARE_OPTION, ReasonCode.LOYALTY_PROGRAM_PREFERENCE,
                                                   ReasonCode.ALTERNATE_ROUTE_WITHIN_MARGIN],
                      roles, [*PREFERENCE_CLAUSES, Clause.SELECTION_OF_CARRIER],
                      f"Lines 398-401: a request for a specific carrier is subject to the personal preference criteria; "
                      f"lines 166-167 and 389-391: it costs {extra} cents more than the lowest logical fare, not more "
                      f"than $200, so it is a comparable option and needs no extra justification: {preferred.carrier}.")
    clauses = list(LOWEST_CLAUSES)
    reasons = [ReasonCode.LOWEST_FARE]
    if llf.stops:
        raise ValueError("a plain request whose lowest fare is a connection is not modelled")
    return answer(Decision.BOOK, [llf], reasons, roles, clauses,
                  f"Lines 145-148, 159-162 and 363-366: economy at the lowest logical fare, {llf.carrier} at "
                  f"{llf.fare_cents} cents; lines 47-49: the trip is authorized in writing.")


def nonstop_request(trip, economy, llf, roles):
    nonstop = one(cheapest([offer for offer in economy if offer.stops == 0]), "cheapest economy nonstop")
    connection = one(cheapest([offer for offer in economy if offer.stops > 0]), "cheapest economy connection")
    if connection.fare_cents >= nonstop.fare_cents:
        raise ValueError("a nonstop request where the nonstop is also the cheapest is not modelled")
    savings = nonstop.fare_cents - connection.fare_cents
    extra = extra_minutes(connection, nonstop)
    clauses = [*PREFERENCE_CLAUSES, Clause.CONNECTIONS, Clause.LOWEST_LOGICAL_FARE,
               Clause.LOWEST_LOGICAL_FARE_DEFINITION]
    if extra > EXTRA_MINUTES:
        if llf is not nonstop:
            raise ValueError("a lowest logical fare other than the nonstop beside a long connection is not modelled")
        return answer(Decision.BOOK, [nonstop, connection],
                      [ReasonCode.CONNECTION_TOO_LONG, ReasonCode.ALTERNATE_ROUTE_TOO_EXPENSIVE, ReasonCode.LOWEST_FARE,
                       ReasonCode.COST_SAVINGS], roles, clauses,
                      f"The connection saves {savings} cents but adds {extra} minutes, more than four hours: it is not "
                      "a required alternative (lines 167-169, 391-393) and, read with lines 370-372, not a stop the "
                      "lowest logical fare may add, so the requested nonstop is the lowest logical fare and needs no "
                      "justification. A reader who still counts the connection as the lowest logical fare books it "
                      "instead (lines 159-161 'any reasonable itineraries'); both are accepted.")
    if llf is not connection:
        raise ValueError("a connection within four hours that is not the lowest logical fare is not modelled")
    if savings == SAVINGS_CENTS:
        return answer(Decision.FLAG_FOR_APPROVAL, [nonstop, connection], UNCLEAR_REASONS,
                      [Approver.NOT_NAMED, Approver.PROCUREMENT_DEPARTMENT, *AREA_OFFICIALS], clauses,
                      f"The nonstop costs exactly $200 more than the connection, which adds {extra} minutes (within four "
                      "hours). Lines 166-167 and 389-391 make it a comparable option ('not higher than $200'), so the "
                      "traveller's preference stands; lines 167-169 and 391-393 require the connection ('savings of "
                      "$200 or more'). The two rules give different tickets at exactly $200 and the text does not say "
                      "which prevails; hold either offer.", phrase=UNCLEAR_PHRASE)
    if savings < SAVINGS_CENTS:
        return answer(Decision.BOOK, [nonstop], [ReasonCode.ALTERNATE_ROUTE_WITHIN_MARGIN,
                                                 ReasonCode.COMPARABLE_FARE_OPTION], roles, clauses,
                      f"Lines 166-167 and 389-391: the nonstop costs {savings} cents more than the lowest logical fare, "
                      "not more than $200, so it is a comparable option, and the connection saves less than $200, so "
                      "it is not required (lines 167-169): the nonstop the traveller asks for.")
    return answer(Decision.BOOK, [connection], [ReasonCode.COST_SAVINGS, ReasonCode.ALTERNATE_ROUTE_TOO_EXPENSIVE,
                                                ReasonCode.LOWEST_FARE], roles, clauses,
                  f"Lines 167-169 and 391-393: the connection saves {savings} cents ($200 or more) and adds {extra} "
                  "minutes (not more than four hours), so it is required; the nonstop is beyond the comparable "
                  "allowance and would need additional justification (lines 171-173), which the traveller declines.")


def personal(trip, offers, economy, roles):
    """Lines 573-597: official travel combined with personal days, with the prior authorization of the Director or
    Secretary; date changes are allowed if they do not increase the fare beyond the comparable options, and the
    traveller pays every difference."""
    if not plain(trip) or trip.requested_cabin != Cabin.ECONOMY or not trip.traveller_pays_difference:
        raise ValueError("only a plain economy date change paid by the traveller is modelled")
    permits = signed(trip, SignOffSubject.PERSONAL_DAYS)
    if len(permits) != 1 or permits[0].role not in PERSONAL_AUTHORIZERS:
        raise ValueError("personal days need one prior authorization by the Director or Secretary (lines 576-577)")
    approvers = [*roles, permits[0].role]
    wanted = lowest(economy)
    work = [offer for offer in on_route(trip, offers, trip.business_travel_date)
            if offer.seats_available and offer.cabin == Cabin.ECONOMY]
    base = lowest(work)
    extra = wanted.fare_cents - base.fare_cents
    if extra <= 0:
        raise ValueError("a personal date that is not dearer is not modelled")
    clauses = [*PERSONAL_CLAUSES, Clause.COMPARABLE_OPTIONS, Clause.PERSONAL_COSTS]
    if extra <= ALLOWANCE_CENTS:
        return answer(Decision.BOOK, [wanted],
                      [ReasonCode.PERSONAL_COST_PAID_BY_TRAVELER, ReasonCode.COMPARABLE_FARE_OPTION,
                       ReasonCode.ALTERNATE_ROUTE_WITHIN_MARGIN, ReasonCode.LOWEST_FARE], approvers, clauses,
                      f"Lines 585-588: a date change for personal days is allowed when it does not increase the fare "
                      f"beyond the comparable options; the fare on the traveller's day is {extra} cents above the "
                      f"lowest fare on the working day, not more than $200 (lines 166-167), and the traveller pays the "
                      f"difference (lines 596-597): {wanted.carrier} on {trip.travel_date}.")
    return answer(Decision.BOOK, [base],
                  [ReasonCode.PERSONAL_CHANGE_NOT_ALLOWED, ReasonCode.ALTERNATE_ROUTE_TOO_EXPENSIVE,
                   ReasonCode.PERSONAL_TRAVEL_NOT_COVERED], approvers, clauses,
                  f"Lines 585-590: the fare on the traveller's own day is {extra} cents above the lowest fare on the "
                  f"working day, beyond the comparable options ($200, lines 166-167), so the change is not allowed at "
                  f"booking; the traveller asked for what the policy allows instead: the lowest fare on "
                  f"{trip.business_travel_date}.")
