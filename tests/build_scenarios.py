"""Writes the OAS scenario JSON files (an authoring aid, not a test; the JSON files are the truth).

    uv run python tests/build_scenarios.py

Expected answers are hand-written here; tests/test_scenarios.py checks them against rules.solve.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = (ROOT / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = ROOT / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def aside(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- clauses the answers rest on -----
AUTH = keep(47, 49, "All requests for GS/OAS Official Travel must be authorized in advance and in writing by the "
            "corresponding area's highest authority (Director or Secretary, the Chief of Staff or the Secretary "
            "General)", "every trip is authorized in advance and in writing by the area's highest authority")
GUEST_DEF = keep(79, 80, "OAS Traveler: includes Staff Members, Time Based Natural CPRs, SOCs, guests and every person "
                 "(unless specifically written out) that travels on behalf of the GS/OAS or/and with GS/OAS funds.",
                 "a guest travelling on GS/OAS funds is an OAS traveller")
APPROVER_DEF = keep(84, 85, None, "the area's highest authority (Director or Secretary, Chief of Staff or Secretary "
                    "General) gives travel authorizations")
TRAVEL_CLASS = keep(145, 148, None, "economy at the lowest logical fare for all but the Secretary General, the Assistant "
                    "Secretary General and the Chair of the Permanent Council")
PREMIUM = keep(149, 151, None, "any class other than economy is an exception needing a Premium Fare Authorization Form")
LLF_DEF = keep(159, 162, None, "the lowest logical fare: any reasonable itinerary, possibly with a stop; lowest "
               "available fares whenever possible")
PREF_DEF = keep(163, 165, None, "not taking the lowest logical fare is reported as personal preference")
COMPARABLE = keep(166, 173, None, "options within $200 of the lowest logical fare are comparable; connections are "
                  "required when they save $200 or more without adding more than four hours ('$2002' is $200 and "
                  "footnote 2)")
FOOTNOTE = keep(185, 186, None, "footnote 2: the amount is US$200")
TIMELY = keep(278, 284, None, "travel plans approved no later than three weeks before travel; late purchases need "
              "additional written approval from the duly authorized official in the requesting area")
OWN = keep(294, 296, None, "only the Secretary General, the Assistant Secretary General and the Chair of the Permanent "
           "Council may approve their own travel request")
CLASS = keep(324, 335, "requires that all tickets paid for with the funds of the Organization be purchased in Economy "
             "Class, except for tickets purchased for travel by the Secretary General, the Assistant Secretary "
             "General, and the Chair of the Permanent Council",
             "economy class for every ticket paid with the Organization's funds, except the three officials")
CLASS_EXC = keep(351, 353, None, "the Premium Fare Authorization Form must be approved by the Secretary General")
LLF = keep(363, 366, "Some LLF may require at least one stop or layover. Lowest available fares must be used whenever "
           "possible.", "the lowest logical fare; lowest available fares whenever possible")
CONNECT = keep(370, 372, None, "stops added for the lowest logical fare should not add more than four hours each way")
PREF = keep(387, 396, None, "personal preference: comparable within $200; connections required when they save $200 or "
            "more within four hours; beyond the allowance the case is reported and may need justification")
CARRIER = keep(398, 401, None, "a request for a specific carrier is subject to the personal preference criteria")
ANCILLARY = keep(425, 430, None, "ancillary fees, baggage included, are not counted when finding the lowest logical fare")
PERSONAL = keep(573, 583, None, "official and personal travel may be combined with the Director's or Secretary's prior "
                "authorization; personal costs are documented and paid by the traveller")
PERMISSIBLE = keep(585, 592, None, "date changes for personal days are allowed if they do not increase the fare beyond "
                   "the comparable options")
PERSONAL_PAY = keep(593, 597, "All expenses or differences in payment arising from personal changes shall also be paid "
                    "by the traveler.", "the traveller pays every difference arising from personal changes")
THIRD = keep(602, 606, None, "when travel is already paid by a third party, the GS/OAS covers only the added cost of "
             "deviating")
IACHR = keep(638, 642, None, "the Secretary General's exception lets the elected IACHR Commissioner buy full economy "
             "fares")
INSTITUTION = keep(644, 649, None, "guests from institutions that cannot receive payments: the GS/OAS buys the fare "
                   "through its travel agency")
VACATION = keep(719, 727, None, "personal travel is at the traveller's expense and not booked by the corporate agents")

# ----- nearby clauses that must not change the answer -----
UPGRADES = aside(413, 416, "upgrades to other than Economy Class using personal funds, points, miles and similar "
                 "programs are allowed under this policy but they are not encouraged",
                 "upgrades with the traveller's own miles: not a cabin the GS/OAS buys")
FREQUENT = aside(477, 478, "GS/OAS permits travelers to retain their frequent flyer mileage points",
                 "miles are kept; it does not choose the fare")
RAIL = aside(174, 176, "Amtrak's \"Acela Express\" is considered Business Class.", "a rail rule, not air")
FOOTNOTE_CHAIR = aside(330, 332, "with the exception of air travel by the chairman of the Permanent Council",
                       "the exception names the Chair alone, not the Chair's delegation")
TOGETHER = aside(630, 632, "the maximum number of GS/OAS Staff/Employees who can travel together on a single aircraft",
                 "a limit with no number, for DP to apply; two travellers are not a group")
ADVANCES = aside(314, 316, "should be paid to travelers by the DFAMS one week before the travel date",
                 "a date rule for per diem advances, not for approvals or fares")
PRICE_MATCH = aside(355, 357, "the TMC is required to match any price for itinerary that a traveler may find elsewhere",
                    "a price match on an identical itinerary, which the request does not raise")
TEC = aside(197, 199, "within thirty (30) days of their estimated return travel date", "an expense-claim deadline")
GROUPS = aside(708, 708, "Groups are defined as council meetings, conferences or events that involve 10 or more "
               "individuals.", "a group definition; one traveller is not a group")
REUSE = aside(561, 562, "Most unused tickets expire after 3 or 12 months.", "unused tickets, not this purchase")
EMERGENCY = aside(302, 305, "in case of emergencies, and when approved by the Secretariat for Administration and "
                  "Finance, the Individual Travel Request/Authorization Form may not be required",
                  "an emergency rule; the trip is not an emergency")

# ----- builders -----


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_title": "", "position": "STAFF_MEMBER", "works_for": "", "origin": "",
        "destination": "", "travel_date": "", "business_travel_date": "", "return_date": "", "booking_date": "",
        "work_starts": "", "purpose": "", "purpose_kind": "MEETING", "requested_cabin": "ECONOMY",
        "requested_routing": "ANY", "requested_airline": "", "requested_refundable": False,
        "traveller_pays_difference": False, "checked_bag_fees": "", "ticket_from_others": "",
        "ticket_from_others_suffices": False, "sign_offs": [],
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    if not base["business_travel_date"]:
        base["business_travel_date"] = base["travel_date"]
    return base


def sign(role, name, subject, signed_on, covers, cabin="NONE"):
    return {"role": role, "name": name, "subject": subject, "cabin": cabin, "signed_on": signed_on, "covers": covers}


def authorized(role, name, signed_on, covers="Individual Travel Request/Authorization Form for this trip, approved"):
    return sign(role, name, "TRAVEL_AUTHORIZATION", signed_on, covers)


def offer(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    return {"decision": decision, "offer_slots": sorted(slots), "cabins": sorted(cabins),
            "reason_codes": sorted(reasons), "approvers": sorted(approvers), "clauses": sorted(clauses),
            "unclear_phrase": phrase}


def search(origin, destination, date, flights, offers, name="main"):
    return {"name": name, "origin": origin, "destination": destination, "date": date, "return_date": "",
            "background": 0, "flights": flights, "offers": offers}


S = []


def scenario(id, category, overlays, request, trip_, searches, exp, must_keep, notes, twin_of="", twin_fact="",
             flag_twins=(), ambiguity="none", distractors=()):
    if isinstance(searches, dict):
        searches = [searches]
    S.append({
        "id": id, "category": category, "overlays": list(overlays), "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": list(flag_twins), "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": searches}, "expected": exp, "must_keep": list(must_keep),
        "distractors": list(distractors), "design_notes": notes,
    })


def on_file(role):
    """Rule 4': a booking accepts the role whose sign-off it relies on, and NONE."""
    return ["NONE", role]


LOWEST_CLAUSES = ["CLASS_OF_SERVICE", "LOWEST_LOGICAL_FARE", "LOWEST_LOGICAL_FARE_DEFINITION", "TRAVEL_CLASS"]
CLASS_CLAUSES = ["CLASS_OF_SERVICE", "CABIN_EXCEPTIONS", "PREMIUM_TRAVEL", "TRAVEL_CLASS"]
SENIOR_CLAUSES = ["CLASS_OF_SERVICE", "TRAVEL_CLASS"]
PREFERENCE_CLAUSES = ["COMPARABLE_OPTIONS", "PERSONAL_PREFERENCE", "PERSONAL_PREFERENCE_DEFINITION"]
ROUTE_CLAUSES = PREFERENCE_CLAUSES + ["CONNECTIONS", "LOWEST_LOGICAL_FARE", "LOWEST_LOGICAL_FARE_DEFINITION"]
PERSONAL_CLAUSES = ["COMPARABLE_OPTIONS", "OFFICIAL_WITH_PERSONAL", "PERMISSIBLE_CHANGES", "PERSONAL_COSTS"]
NO_CLASS = ["ECONOMY_CLASS_REQUIRED", "UPGRADE_NOT_ELIGIBLE"]
REQUIRED_CONNECTION = ["ALTERNATE_ROUTE_TOO_EXPENSIVE", "COST_SAVINGS", "LOWEST_FARE"]
LOW = [TRAVEL_CLASS, CLASS, LLF, AUTH]
NO_JUSTIFY = "if the policy lets me have it without any extra justification; if not, book what the policy calls for"

# ===== easy (5) =====

scenario(
    "agave-ridge", "easy", ["upgrade_not_taken"],
    "I'm flying Dulles to Ottawa on February 9th for the meeting with Global Affairs Canada the next morning. "
    "Economy is fine for this one; book the lowest fare.",
    trip(traveller_name="Ernesto Valdivia", traveller_title="Secretary General", position="SECRETARY_GENERAL",
         works_for="Office of the Secretary General", origin="IAD", destination="YOW", travel_date="2027-02-09",
         booking_date="2026-12-15", work_starts="2027-02-10 09:00",
         purpose="Bilateral meeting with Global Affairs Canada in Ottawa", purpose_kind="MEETING",
         sign_offs=[authorized("SECRETARY_GENERAL", "Ernesto Valdivia", "2026-12-15")]),
    search("IAD", "YOW", "2027-02-09", {
        "united": {"carrier": "UA", "depart": "09:00"},
        "aircanada": {"carrier": "AC", "via": ["YYZ"], "depart": "07:30"},
    }, [
        offer("united-economy", "united", "ECONOMY", 28900),
        offer("united-business", "united", "BUSINESS", 79000),
        offer("aircanada-economy", "aircanada", "ECONOMY", 31800),
        offer("aircanada-business", "aircanada", "BUSINESS", 86000),
    ]),
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["LOWEST_FARE"], on_file("SECRETARY_GENERAL"),
             LOWEST_CLAUSES + ["OWN_APPROVAL"]),
    [TRAVEL_CLASS, CLASS, LLF, OWN],
    "The Secretary General is outside the economy rule (lines 145-146, 324-328) and may approve his own trip (lines "
    "294-296), but asks for the lowest economy fare: United at $289. Business is permitted and correctly not taken.")

scenario(
    "basalt-vine", "easy", ["dearer_option"],
    "Dulles to Santiago on March 8th, overnight, for the regional consultations that open the next afternoon. "
    "Business class, please.",
    trip(traveller_name="Amb. Lucia Ferreyra", traveller_title="Chair of the Permanent Council",
         position="PERMANENT_COUNCIL_CHAIR", works_for="Permanent Council of the OAS", origin="IAD", destination="SCL",
         travel_date="2027-03-08", booking_date="2027-01-18", work_starts="2027-03-09 15:00",
         purpose="Regional consultations of the Permanent Council in Santiago", purpose_kind="MISSION",
         requested_cabin="BUSINESS",
         sign_offs=[authorized("CHIEF_OF_STAFF", "Mariano Ocampo", "2027-01-15")]),
    search("IAD", "SCL", "2027-03-08", {
        "latam": {"carrier": "LA", "depart": "21:10"},
        "united": {"carrier": "UA", "depart": "22:05"},
    }, [
        offer("latam-economy", "latam", "ECONOMY", 104000),
        offer("latam-business", "latam", "BUSINESS", 362000),
        offer("united-economy", "united", "ECONOMY", 111000),
        offer("united-business", "united", "BUSINESS", 398000),
    ]),
    expected("BOOK", ["latam-business"], ["BUSINESS"], ["SENIOR_ROLE_ENTITLEMENT"], on_file("CHIEF_OF_STAFF"),
             SENIOR_CLAUSES),
    [TRAVEL_CLASS, CLASS, AUTH],
    "Tickets for the Chair of the Permanent Council are excepted from economy class (lines 145-146, 324-328; footnote "
    "3). She asks for business: the cheapest business fare, LATAM at $3,620. The Chief of Staff authorized the trip.")

scenario(
    "condor-flats", "easy", ["upgrade_not_taken"],
    "Dulles to Sao Paulo on April 12th, overnight, for the trade-facilitation workshop the following afternoon. "
    "I'd like business class for the overnight flight if the policy allows it; if not, book what it allows.",
    trip(traveller_name="Gabriel Monteiro", traveller_title="Director, Department of Economic Development",
         position="DIRECTOR", works_for="Department of Economic Development, Executive Secretariat for Integral "
         "Development", origin="IAD", destination="GRU", travel_date="2027-04-12", booking_date="2027-02-22",
         work_starts="2027-04-13 14:00", purpose="Trade-facilitation workshop in Sao Paulo", purpose_kind="CONFERENCE",
         requested_cabin="BUSINESS",
         sign_offs=[authorized("SECRETARY", "Kim Osei-Barrow", "2027-02-19")]),
    search("IAD", "GRU", "2027-04-12", {
        "united": {"carrier": "UA", "depart": "21:30", "minutes": [595]},
        "latam": {"carrier": "LA", "depart": "22:10", "minutes": [600]},
    }, [
        offer("united-economy", "united", "ECONOMY", 98500),
        offer("united-business", "united", "BUSINESS", 435000),
        offer("latam-economy", "latam", "ECONOMY", 102000),
        offer("latam-business", "latam", "BUSINESS", 390000),
    ]),
    expected("BOOK", ["united-economy"], ["ECONOMY"], NO_CLASS, on_file("SECRETARY"), CLASS_CLAUSES),
    [TRAVEL_CLASS, CLASS, PREMIUM, CLASS_EXC, AUTH],
    "Every ticket paid with the Organization's funds is economy except the three officials (lines 145-148, 324-328); "
    "another class needs a Premium Fare Authorization Form approved by the Secretary General (149-151, 351-353), and "
    "the Director has none. A ten-hour overnight flight changes nothing: the handbook has no duration rule. The "
    "traveller asked for what the policy allows otherwise: the lowest economy fare, United at $985.")

scenario(
    "dahlia-mesa", "easy", ["dearer_option"],
    "Dulles to Sao Paulo on May 17th, overnight, for the regional security conference the next afternoon. The "
    "Secretary General approved my Premium Fare Authorization Form for business class on this trip. Business, please.",
    trip(traveller_name="Patricia Holloway", traveller_title="Senior Specialist, Department of Public Security",
         works_for="Department of Public Security, Secretariat for Multidimensional Security", origin="IAD",
         destination="GRU", travel_date="2027-05-17", booking_date="2027-03-29", work_starts="2027-05-18 14:00",
         purpose="Regional security conference in Sao Paulo", purpose_kind="CONFERENCE", requested_cabin="BUSINESS",
         sign_offs=[authorized("DIRECTOR", "Hector Lozano", "2027-03-22"),
                    sign("SECRETARY_GENERAL", "Ernesto Valdivia", "PREMIUM_FARE_FORM", "2027-03-26",
                         "Premium Fare Authorization Form: business class for this trip (medical certificate on "
                         "file)", cabin="BUSINESS")]),
    search("IAD", "GRU", "2027-05-17", {
        "united": {"carrier": "UA", "depart": "21:30", "minutes": [595]},
        "latam": {"carrier": "LA", "depart": "22:10", "minutes": [600]},
    }, [
        offer("united-economy", "united", "ECONOMY", 97000),
        offer("united-business", "united", "BUSINESS", 428000),
        offer("latam-economy", "latam", "ECONOMY", 99500),
        offer("latam-business", "latam", "BUSINESS", 386000),
    ]),
    expected("BOOK", ["latam-business"], ["BUSINESS"], ["PREMIUM_FARE_AUTHORIZED"],
             ["NONE", "DIRECTOR", "SECRETARY_GENERAL"], CLASS_CLAUSES),
    [PREMIUM, CLASS_EXC, CLASS, AUTH],
    "Business is an exception under lines 149-151, processed with a Premium Fare Authorization Form that 'must be "
    "approved by the Secretary General' (351-353); his approval is on file for business on this trip. The cheapest "
    "business fare: LATAM at $3,860.")

MEX = {"origin": "IAD", "destination": "MEX", "travel_date": "2027-01-04", "work_starts": "2027-01-05 09:00",
       "purpose": "Electoral observation planning meetings in Mexico City", "purpose_kind": "MISSION",
       "works_for": "Department for Electoral Cooperation and Observation"}
MEX_REQUEST = ("Dulles to Mexico City on Monday, January 4th, for the electoral observation planning meetings that "
               "start Tuesday morning. Please book my flight.")


def mex():
    return search("IAD", "MEX", "2027-01-04", {
        "aeromexico": {"carrier": "AM", "depart": "09:10"},
        "united": {"carrier": "UA", "depart": "11:40"},
    }, [
        offer("aeromexico-economy", "aeromexico", "ECONOMY", 41200),
        offer("united-economy", "united", "ECONOMY", 44700),
    ])


scenario(
    "egret-shoal", "easy", ["date_arithmetic", "month_end", "outside_air_section"], MEX_REQUEST,
    trip(traveller_name="Rosa Quintanilla", traveller_title="Electoral Specialist", booking_date="2026-12-14",
         sign_offs=[authorized("DIRECTOR", "Tomas Arrieta", "2026-12-14")], **MEX),
    mex(),
    expected("BOOK", ["aeromexico-economy"], ["ECONOMY"], ["LOWEST_FARE"], on_file("DIRECTOR"),
             LOWEST_CLAUSES + ["ADVANCE_TIMELINESS"]),
    LOW + [TIMELY],
    "Authorized on December 14 for travel on January 4: 21 days, which is 'no later than three (3) weeks prior to "
    "the travel date' (lines 280-281), so the purchase is not late. The lowest logical fare: Aeromexico at $412.",
    distractors=[ADVANCES])

# ===== boundary twins (6) =====

LAX = {"origin": "IAD", "destination": "LAX", "travel_date": "2027-03-15", "booking_date": "2027-01-25",
       "work_starts": "2027-03-16 09:00", "purpose": "Inter-American cybersecurity forum in Los Angeles",
       "purpose_kind": "CONFERENCE", "requested_routing": "NONSTOP",
       "works_for": "Inter-American Committee against Terrorism, Secretariat for Multidimensional Security"}
LAX_REQUEST = ("Dulles to Los Angeles on March 15th for the cybersecurity forum, which opens the next morning. I'd "
               f"rather fly nonstop, {NO_JUSTIFY}.")


def lax(nonstop_cents):
    return search("IAD", "LAX", "2027-03-15", {
        "nonstop": {"carrier": "UA", "depart": "08:00", "minutes": [330]},
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "08:00", "minutes": [200, 200], "layovers": [80]},
    }, [
        offer("nonstop-economy", "nonstop", "ECONOMY", nonstop_cents),
        offer("dallas-economy", "dallas", "ECONOMY", 31000),
    ])


LAX_TRIP = dict(traveller_name="Daniel Achterberg", traveller_title="Program Officer",
                sign_offs=[authorized("SECRETARY", "Farah Mendoza-Lyle", "2027-01-20")], **LAX)

scenario(
    "fern-canyon", "boundary_twin", ["multi_leg", "dearer_option"], LAX_REQUEST, trip(**LAX_TRIP), lax(50900),
    expected("BOOK", ["nonstop-economy"], ["ECONOMY"], ["ALTERNATE_ROUTE_WITHIN_MARGIN", "COMPARABLE_FARE_OPTION"],
             on_file("SECRETARY"), ROUTE_CLAUSES),
    [COMPARABLE, PREF, FOOTNOTE, AUTH],
    "The connection through Dallas ($310, 150 minutes longer, both leave 08:00) is the lowest logical fare. The "
    "nonstop costs $199 more: 'not higher than $200', so it is a comparable option (lines 166-167, 389-391), and a "
    "saving of $199 does not make the connection required (lines 167-169). The traveller's nonstop is booked.",
    twin_of="guava-ledge", twin_fact="the nonstop costs $199 or $201 more than the connection")

scenario(
    "guava-ledge", "boundary_twin", ["multi_leg"], LAX_REQUEST, trip(**LAX_TRIP), lax(51100),
    expected("BOOK", ["dallas-economy"], ["ECONOMY"], REQUIRED_CONNECTION, on_file("SECRETARY"), ROUTE_CLAUSES),
    [COMPARABLE, PREF, CONNECT, FOOTNOTE, AUTH],
    "The nonstop now costs $201 more. The connection saves '$200 or more' and adds 150 minutes, within four hours, so "
    "it is required (lines 167-169, 391-393); the nonstop exceeds the allowance and would need additional "
    "justification (171-173), which the traveller declines. Book the Dallas connection.",
    twin_of="fern-canyon", twin_fact="the nonstop costs $201 or $199 more than the connection")

GRU = {"origin": "IAD", "destination": "GRU", "travel_date": "2027-06-07", "booking_date": "2027-04-19",
       "work_starts": "2027-06-08 09:00", "purpose": "Inter-American water-resources dialogue in Sao Paulo",
       "purpose_kind": "CONFERENCE", "requested_routing": "NONSTOP",
       "works_for": "Department of Sustainable Development"}
GRU_REQUEST = ("Dulles to Sao Paulo on June 7th for the water-resources dialogue, which starts the next morning. I'd "
               f"rather fly nonstop, {NO_JUSTIFY}.")


def gru(layover):
    return search("IAD", "GRU", "2027-06-07", {
        "nonstop": {"carrier": "UA", "depart": "08:00", "minutes": [595]},
        "miami": {"carrier": "AA", "via": ["MIA"], "depart": "08:00", "minutes": [160, 500], "layovers": [layover]},
    }, [
        offer("nonstop-economy", "nonstop", "ECONOMY", 124000),
        offer("miami-economy", "miami", "ECONOMY", 94000),
    ])


GRU_TRIP = dict(traveller_name="Ines Barrientos", traveller_title="Water Resources Specialist",
                sign_offs=[authorized("DIRECTOR", "Marc Beaumont", "2027-04-12")], **GRU)

scenario(
    "heron-pampa", "boundary_twin", ["multi_leg"], GRU_REQUEST, trip(**GRU_TRIP), gru(175),
    expected("BOOK", ["miami-economy"], ["ECONOMY"], REQUIRED_CONNECTION, on_file("DIRECTOR"), ROUTE_CLAUSES),
    [COMPARABLE, PREF, CONNECT, AUTH],
    "The Miami connection saves $300 and, leaving at the same time, lands exactly 240 minutes after the nonstop "
    "(elapsed 835 against 595). That does not extend the one-way air travel time 'by more than four (4) hours', so "
    "the connection is required (lines 167-169, 370-372, 391-393).",
    twin_of="ibis-knoll", twin_fact="the Miami layover is 175 or 176 minutes (240 or 241 minutes longer)")

scenario(
    "ibis-knoll", "boundary_twin", ["multi_leg", "dearer_option"], GRU_REQUEST, trip(**GRU_TRIP), gru(176),
    expected("BOOK", ["miami-economy", "nonstop-economy"], ["ECONOMY"],
             ["ALTERNATE_ROUTE_TOO_EXPENSIVE", "CONNECTION_TOO_LONG", "COST_SAVINGS", "LOWEST_FARE"],
             on_file("DIRECTOR"), ROUTE_CLAUSES),
    [COMPARABLE, PREF, CONNECT, AUTH],
    "The connection now adds 241 minutes, more than four hours: it is no longer required (lines 167-169), and stops "
    "added for the lowest logical fare should not add more than four hours (370-372), so the nonstop is the lowest "
    "logical fare and the traveller's choice needs no justification. A reader who still counts the connection as the "
    "lowest logical fare ('any reasonable itineraries', 159-161) books it; both are accepted.",
    twin_of="heron-pampa", twin_fact="the Miami layover is 176 or 175 minutes (241 or 240 minutes longer)")

BOG_PERSONAL = {"origin": "IAD", "destination": "BOG", "travel_date": "2027-02-13", "business_travel_date": "2027-02-15",
                "booking_date": "2026-12-28", "work_starts": "2027-02-16 09:00",
                "purpose": "Justice-sector cooperation meetings in Bogota (Tuesday to Thursday)",
                "purpose_kind": "MEETING", "traveller_pays_difference": True,
                "works_for": "Department of International Law, Secretariat for Legal Affairs"}
BOG_PERSONAL_REQUEST = (
    "My Bogota meetings start Tuesday morning, so the trip needs a flight on Monday, February 15th, but I'd like to "
    "fly out on Saturday the 13th and spend the weekend there at my own cost. I'll pay any difference in the fare. If "
    "leaving Saturday isn't allowed, book the Monday flight.")


def bog_personal(saturday_cents):
    return [
        search("IAD", "BOG", "2027-02-13", {
            "avianca": {"carrier": "AV", "depart": "08:30"},
            "united": {"carrier": "UA", "depart": "10:15"},
        }, [
            offer("saturday-avianca", "avianca", "ECONOMY", saturday_cents),
            offer("saturday-united", "united", "ECONOMY", 64000),
        ], name="saturday"),
        search("IAD", "BOG", "2027-02-15", {
            "avianca": {"carrier": "AV", "depart": "08:30"},
            "united": {"carrier": "UA", "depart": "10:15"},
        }, [
            offer("monday-avianca", "avianca", "ECONOMY", 38000),
            offer("monday-united", "united", "ECONOMY", 45500),
        ], name="monday"),
    ]


BOG_PERSONAL_TRIP = dict(
    traveller_name="Mateo Garzon", traveller_title="Senior Legal Officer",
    sign_offs=[authorized("DIRECTOR", "Ana Lucia Prado", "2026-12-21"),
               sign("DIRECTOR", "Ana Lucia Prado", "PERSONAL_DAYS", "2026-12-21",
                    "Personal days in Bogota on February 13-14 combined with the official trip; personal time and "
                    "costs documented and paid by the traveller")],
    **BOG_PERSONAL)

scenario(
    "jacaranda-cove", "boundary_twin", ["personal_travel", "outside_air_section", "dearer_option"],
    BOG_PERSONAL_REQUEST, trip(**BOG_PERSONAL_TRIP), bog_personal(58000),
    expected("BOOK", ["saturday-avianca"], ["ECONOMY"],
             ["ALTERNATE_ROUTE_WITHIN_MARGIN", "COMPARABLE_FARE_OPTION", "LOWEST_FARE", "PERSONAL_COST_PAID_BY_TRAVELER"], on_file("DIRECTOR"),
             PERSONAL_CLAUSES),
    [PERSONAL, PERMISSIBLE, PERSONAL_PAY, COMPARABLE, AUTH],
    "Personal days are authorized by the Director (lines 573-577). A date change is allowed 'provided that these "
    "changes do not increase the fare cost beyond the comparable options' (585-588): Saturday's lowest fare ($580) is "
    "exactly $200 above Monday's ($380), 'not higher than $200' (166-167), so it is allowed and the traveller pays the "
    "difference (596-597).",
    twin_of="kapok-strand", twin_fact="Saturday's lowest fare is $200 or $201 above Monday's")

scenario(
    "kapok-strand", "boundary_twin", ["personal_travel", "outside_air_section"],
    BOG_PERSONAL_REQUEST, trip(**BOG_PERSONAL_TRIP), bog_personal(58100),
    expected("BOOK", ["monday-avianca"], ["ECONOMY"],
             ["ALTERNATE_ROUTE_TOO_EXPENSIVE", "PERSONAL_CHANGE_NOT_ALLOWED", "PERSONAL_TRAVEL_NOT_COVERED"],
             on_file("DIRECTOR"), PERSONAL_CLAUSES),
    [PERSONAL, PERMISSIBLE, COMPARABLE, AUTH],
    "Saturday's lowest fare is now $201 above Monday's, beyond the comparable options (lines 166-167), so the date "
    "change is not allowed at booking (585-590), even with the traveller paying. The request's fallback: Monday's "
    "lowest fare, Avianca at $380.",
    twin_of="jacaranda-cove", twin_fact="Saturday's lowest fare is $201 or $200 above Monday's")

# ===== multi-rule (4) =====

scenario(
    "llama-terrace", "multi_rule", ["dearer_option", "outside_air_section"],
    "Dulles to San Juan on April 26th for the Caribbean disaster-resilience summit the next morning. I signed my own "
    "travel request for this one. Business class, please.",
    trip(traveller_name="Nathaniel Brathwaite", traveller_title="Assistant Secretary General",
         position="ASSISTANT_SECRETARY_GENERAL", works_for="Office of the Assistant Secretary General", origin="IAD",
         destination="SJU", travel_date="2027-04-26", booking_date="2027-03-08", work_starts="2027-04-27 09:00",
         purpose="Caribbean disaster-resilience summit in San Juan", purpose_kind="CONFERENCE",
         requested_cabin="BUSINESS",
         sign_offs=[authorized("ASSISTANT_SECRETARY_GENERAL", "Nathaniel Brathwaite", "2027-03-08")]),
    search("IAD", "SJU", "2027-04-26", {
        "united": {"carrier": "UA", "depart": "08:00"},
        "american": {"carrier": "AA", "via": ["MIA"], "depart": "07:05"},
    }, [
        offer("united-economy", "united", "ECONOMY", 31500),
        offer("united-business", "united", "BUSINESS", 115000),
        offer("american-economy", "american", "ECONOMY", 29800),
        offer("american-business", "american", "BUSINESS", 124000),
    ]),
    expected("BOOK", ["united-business"], ["BUSINESS"], ["SENIOR_ROLE_ENTITLEMENT"],
             on_file("ASSISTANT_SECRETARY_GENERAL"), SENIOR_CLAUSES + ["OWN_APPROVAL"]),
    [TRAVEL_CLASS, CLASS, OWN],
    "Two exceptions meet: the Assistant Secretary General may approve his own travel request (lines 294-296, unlike "
    "every other traveller), and his tickets are not held to economy (145-146, 324-328). Business at its cheapest: "
    "United at $1,150.")

scenario(
    "mango-quarry", "multi_rule", ["date_arithmetic", "month_end", "outside_air_section"], MEX_REQUEST,
    trip(traveller_name="Rosa Quintanilla", traveller_title="Electoral Specialist", booking_date="2026-12-21",
         sign_offs=[authorized("DIRECTOR", "Tomas Arrieta", "2026-12-21"),
                    sign("DIRECTOR", "Tomas Arrieta", "LATE_PURCHASE_APPROVAL", "2026-12-21",
                         "Additional written approval to buy the fare for this trip now")], **MEX),
    mex(),
    expected("BOOK", ["aeromexico-economy"], ["ECONOMY"], ["LATE_PURCHASE_APPROVED", "LOWEST_FARE"],
             on_file("DIRECTOR"), LOWEST_CLAUSES + ["ADVANCE_TIMELINESS"]),
    LOW + [TIMELY],
    "Authorized on December 21 for travel on January 4: 14 days, later than three weeks before travel, so the late "
    "purchase needs 'additional written approval from the duly authorized official in the requesting area' (lines "
    "280-284). The Director's additional approval is on file: book the lowest logical fare, Aeromexico at $412.",
    distractors=[ADVANCES])

scenario(
    "nopal-harbor", "multi_rule", ["dearer_option"],
    "Dulles to Miami on March 1st for the hurricane-preparedness workshop the next morning. I'd rather fly United, "
    f"{NO_JUSTIFY}.",
    trip(traveller_name="Keisha Thompson", traveller_title="Disaster Risk Officer",
         works_for="Department of Sustainable Development", origin="IAD", destination="MIA", travel_date="2027-03-01",
         booking_date="2027-01-11", work_starts="2027-03-02 09:00",
         purpose="Hurricane-preparedness workshop in Miami", purpose_kind="CONFERENCE",
         requested_airline="United Airlines",
         sign_offs=[authorized("DIRECTOR", "Marc Beaumont", "2027-01-08")]),
    search("IAD", "MIA", "2027-03-01", {
        "american": {"carrier": "AA", "depart": "07:45"},
        "united": {"carrier": "UA", "depart": "10:05"},
    }, [
        offer("american-economy", "american", "ECONOMY", 19800),
        offer("united-economy", "united", "ECONOMY", 33800),
    ]),
    expected("BOOK", ["united-economy"], ["ECONOMY"], ["ALTERNATE_ROUTE_WITHIN_MARGIN", "COMPARABLE_FARE_OPTION", "LOYALTY_PROGRAM_PREFERENCE"],
             on_file("DIRECTOR"), PREFERENCE_CLAUSES + ["SELECTION_OF_CARRIER"]),
    [CARRIER, COMPARABLE, PREF, AUTH],
    "A request for a specific carrier is 'subject to the Personal Preference criteria' (lines 398-401). United costs "
    "$140 more than the lowest logical fare, 'not higher than $200', so it is a comparable option (166-167, 389-391) "
    "and needs no extra justification: book United.",
    distractors=[FREQUENT])

scenario(
    "ocelot-spire", "multi_rule", ["dearer_option"],
    "Dulles to Los Angeles on May 3rd; I present at the Pacific trade forum at 9 the next morning. The Secretary "
    "General approved my Premium Fare Authorization Form for business class on this trip. First class is only about "
    "$300 more on the United nonstop, so could you put me in first? If the form doesn't cover that, book what it "
    "does cover.",
    trip(traveller_name="Simone Adeyemi", traveller_title="Trade Policy Advisor",
         works_for="Department of Economic Development", origin="IAD", destination="LAX", travel_date="2027-05-03",
         booking_date="2027-03-15", work_starts="2027-05-04 09:00", purpose="Pacific trade forum in Los Angeles",
         purpose_kind="CONFERENCE", requested_cabin="FIRST",
         sign_offs=[authorized("DIRECTOR", "Gabriel Monteiro", "2027-03-10"),
                    sign("SECRETARY_GENERAL", "Ernesto Valdivia", "PREMIUM_FARE_FORM", "2027-03-12",
                         "Premium Fare Authorization Form: business class for this trip (medical certificate on "
                         "file)", cabin="BUSINESS")]),
    search("IAD", "LAX", "2027-05-03", {
        "united": {"carrier": "UA", "depart": "08:15"},
        "american": {"carrier": "AA", "via": ["DFW"], "depart": "07:00"},
    }, [
        offer("united-economy", "united", "ECONOMY", 31000),
        offer("united-business", "united", "BUSINESS", 98000),
        offer("united-first", "united", "FIRST", 129000),
        offer("american-economy", "american", "ECONOMY", 29000),
        offer("american-business", "american", "BUSINESS", 104000),
    ]),
    expected("BOOK", ["united-business"], ["BUSINESS"], ["PREMIUM_FARE_AUTHORIZED", "UPGRADE_NOT_ELIGIBLE"],
             ["NONE", "DIRECTOR", "SECRETARY_GENERAL"], CLASS_CLAUSES),
    [PREMIUM, CLASS_EXC, CLASS, AUTH],
    "The Secretary General's approved form covers business (lines 149-151, 351-353); first is another class with no "
    "approved form, so it is not bought. The request's fallback: the cheapest business fare, United at $980.",
    distractors=[UPGRADES])

# ===== hidden clause (2) =====

scenario(
    "puma-lagoon", "hidden_clause", ["dearer_option", "outside_air_section"],
    "Dulles to Bogota on June 21st for the Commission's on-site hearings, which start the next morning. Hearing dates "
    "often move, so I'd like the full-fare economy ticket that can be changed or refunded without a fee.",
    trip(traveller_name="Dr. Valeria Cordero", traveller_title="Commissioner, Inter-American Commission on Human "
         "Rights (elected)", position="IACHR_COMMISSIONER", works_for="Inter-American Commission on Human Rights",
         origin="IAD", destination="BOG", travel_date="2027-06-21", booking_date="2027-05-03",
         work_starts="2027-06-22 09:00", purpose="On-site hearings of the IACHR in Bogota", purpose_kind="HEARING",
         requested_refundable=True,
         sign_offs=[authorized("SECRETARY", "Jorge Elizondo", "2027-04-28",
                               "Individual Travel Request/Authorization Form for this trip, approved by the Executive "
                               "Secretary of the IACHR")]),
    search("IAD", "BOG", "2027-06-21", {
        "avianca": {"carrier": "AV", "depart": "08:30"},
        "united": {"carrier": "UA", "depart": "10:15"},
    }, [
        offer("avianca-economy", "avianca", "ECONOMY", 38500),
        offer("avianca-flexible", "avianca", "ECONOMY", 89000, refundable=True),
        offer("avianca-business", "avianca", "BUSINESS", 160000),
        offer("united-economy", "united", "ECONOMY", 41000),
        offer("united-flexible", "united", "ECONOMY", 97500, refundable=True),
    ]),
    expected("BOOK", ["avianca-flexible"], ["ECONOMY"], ["FULL_ECONOMY_FARE_AUTHORIZED", "SENIOR_ROLE_ENTITLEMENT"],
             ["NONE", "SECRETARY", "SECRETARY_GENERAL"], ["HUMAN_RIGHTS_COMMISSIONERS"]),
    [IACHR, AUTH],
    "Section 8.6 (lines 638-642), under Special Circumstances, records the Secretary General's exception allowing "
    "the elected IACHR Commissioner to purchase full economy fares. The commissioner asks for one: the cheapest "
    "refundable economy fare, Avianca at $890, not the $385 lowest fare.")

scenario(
    "quetzal-bank", "hidden_clause", ["outside_air_section"],
    "We've invited Dr. Helen Park from the U.S. Centers for Disease Control as an expert for our mission in Bogota; "
    "as a U.S. Government official she can't receive payments in her own name. She flies Atlanta to Bogota on July "
    "12th, and the mission starts the next morning. She normally flies business on government trips; book that if "
    "our policy allows it, otherwise what it allows.",
    trip(traveller_name="Dr. Helen Park", traveller_title="Epidemiologist, U.S. Centers for Disease Control and "
         "Prevention (invited expert)", position="INVITED_EXPERT",
         works_for="U.S. Centers for Disease Control and Prevention", origin="ATL", destination="BOG",
         travel_date="2027-07-12", booking_date="2027-05-24", work_starts="2027-07-13 09:00",
         purpose="Expert on the OAS health-security mission in Bogota", purpose_kind="MISSION",
         requested_cabin="BUSINESS",
         sign_offs=[authorized("DIRECTOR", "Hector Lozano", "2027-05-20")]),
    search("ATL", "BOG", "2027-07-12", {
        "delta": {"carrier": "DL", "depart": "09:20"},
        "avianca": {"carrier": "AV", "depart": "12:40"},
    }, [
        offer("delta-economy", "delta", "ECONOMY", 52000),
        offer("delta-business", "delta", "BUSINESS", 145000),
        offer("avianca-economy", "avianca", "ECONOMY", 54500),
        offer("avianca-business", "avianca", "BUSINESS", 151000),
    ]),
    expected("BOOK", ["delta-economy"], ["ECONOMY"], NO_CLASS, on_file("DIRECTOR"),
             CLASS_CLAUSES + ["OAS_TRAVELER", "PAYMENT_RESTRICTED_INSTITUTIONS"]),
    [GUEST_DEF, INSTITUTION, CLASS, PREMIUM, AUTH],
    "A guest travelling with GS/OAS funds is an 'OAS Traveler' (lines 79-80, in Definitions), and for officials "
    "who cannot receive payments the GS/OAS buys the fare (8.7, lines 644-649). Every ticket paid with the "
    "Organization's funds is economy (324-328) and no Premium Fare form is on file: Delta economy at $520.")

# ===== distractor (2) =====

scenario(
    "rhea-dune", "distractor", ["upgrade_not_taken"],
    "Washington National to Orlando on February 22nd for the tourism ministers' meeting the next morning. Economy is "
    "fine; book the lowest fare. JetBlue would charge me $35 for my checked bag and American includes one on this "
    "fare, in case that matters.",
    trip(traveller_name="Amb. Lucia Ferreyra", traveller_title="Chair of the Permanent Council",
         position="PERMANENT_COUNCIL_CHAIR", works_for="Permanent Council of the OAS", origin="DCA", destination="MCO",
         travel_date="2027-02-22", booking_date="2027-01-04", work_starts="2027-02-23 09:00",
         purpose="Inter-American meeting of tourism ministers in Orlando", purpose_kind="MEETING",
         checked_bag_fees="JetBlue: $35 for the first checked bag; American: first checked bag included on this fare",
         sign_offs=[authorized("CHIEF_OF_STAFF", "Mariano Ocampo", "2027-01-04")]),
    search("DCA", "MCO", "2027-02-22", {
        "jetblue": {"carrier": "B6", "depart": "07:20"},
        "american": {"carrier": "AA", "depart": "09:35"},
    }, [
        offer("jetblue-economy", "jetblue", "ECONOMY", 13900),
        offer("american-economy", "american", "ECONOMY", 15200),
    ]),
    expected("BOOK", ["jetblue-economy"], ["ECONOMY"], ["ANCILLARY_FEES_EXCLUDED", "LOWEST_FARE"],
             on_file("CHIEF_OF_STAFF"), LOWEST_CLAUSES + ["ANCILLARY_FEES"]),
    [ANCILLARY, LLF, TRAVEL_CLASS, CLASS],
    "The Chair may fly another class (lines 145-146) but asks for the lowest economy fare. 'For the purpose of "
    "determining the LLF, airline ancillary service fees (including baggage) should not be included' (lines 427-428), "
    "and bag fees are reimbursed separately (428-430): JetBlue's $139 is the lowest fare, whatever the bag costs.",
    distractors=[PRICE_MATCH])

scenario(
    "sisal-crest", "distractor", [],
    "I'm going to Bogota on June 14th as adviser to the Chair of the Permanent Council for the consultations that "
    "open the next morning. The Chair is flying business; put me in business with her if that's allowed, otherwise "
    "book what the policy allows.",
    trip(traveller_name="Tomas Villalobos", traveller_title="Adviser to the Chair of the Permanent Council",
         position="ADVISER", works_for="Secretariat of the Permanent Council", origin="IAD", destination="BOG",
         travel_date="2027-06-14", booking_date="2027-04-26", work_starts="2027-06-15 09:00",
         purpose="Consultations of the Permanent Council in Bogota", purpose_kind="MISSION",
         requested_cabin="BUSINESS",
         sign_offs=[authorized("DIRECTOR", "Beatriz Solano", "2027-04-21")]),
    search("IAD", "BOG", "2027-06-14", {
        "avianca": {"carrier": "AV", "depart": "08:30"},
        "united": {"carrier": "UA", "depart": "10:15"},
    }, [
        offer("avianca-economy", "avianca", "ECONOMY", 39500),
        offer("avianca-business", "avianca", "BUSINESS", 165000),
        offer("united-economy", "united", "ECONOMY", 43000),
        offer("united-business", "united", "BUSINESS", 172000),
    ]),
    expected("BOOK", ["avianca-economy"], ["ECONOMY"], NO_CLASS, on_file("DIRECTOR"), CLASS_CLAUSES),
    [TRAVEL_CLASS, CLASS, PREMIUM, CLASS_EXC, AUTH],
    "The exception is for tickets 'purchased for travel by' the Chair herself (lines 324-328, 145-146); her adviser "
    "is held to economy and has no Premium Fare form. The rules on employees flying together (8.5) set no class. "
    "Avianca economy at $395.",
    distractors=[FOOTNOTE_CHAIR, TOGETHER])

# ===== refusal (2) =====

scenario(
    "tapir-hollow", "refusal", ["personal_travel", "outside_air_section"],
    "Could you book my holiday flight, Dulles to Mexico City on December 23rd? It's a family vacation over the "
    "holidays, nothing to do with work; I'll be on annual leave.",
    trip(traveller_name="Lena Fischer-Ruiz", traveller_title="Budget Analyst",
         works_for="Department of Financial and Administrative Management Services", origin="IAD", destination="MEX",
         travel_date="2026-12-23", booking_date="2026-11-24", work_starts="",
         purpose="Family vacation in Mexico City during annual leave", purpose_kind="VACATION"),
    search("IAD", "MEX", "2026-12-23", {
        "aeromexico": {"carrier": "AM", "depart": "09:10"},
        "united": {"carrier": "UA", "depart": "11:40"},
    }, [
        offer("aeromexico-economy", "aeromexico", "ECONOMY", 38000),
        offer("united-economy", "united", "ECONOMY", 41000),
    ]),
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             ["PERSONAL_VACATION"]),
    [VACATION],
    "Section 12 (lines 719-727): personal travel not associated with official travel goes through the travel "
    "agency's leisure section, 'the TMC corporate travel agents should not be used to book leisure trips', and all "
    "costs are the traveller's. The GS/OAS buys no ticket.",
    distractors=[GROUPS])

scenario(
    "urchin-bay", "refusal", ["outside_air_section"],
    "The Inter-American Development Bank has already bought my round trip to Santiago for its conference, out March "
    "1st and back March 6th. The OAS asked me to present at our own workshop in Santiago on March 5th, while I'm "
    "there. Please book whatever the OAS needs to buy for me to attend.",
    trip(traveller_name="Carlos Benitez", traveller_title="Senior Specialist, Department of Effective Public "
         "Management", works_for="Department of Effective Public Management", origin="IAD", destination="SCL",
         travel_date="2027-03-01", booking_date="2027-01-11", work_starts="2027-03-05 09:00",
         purpose="OAS public-management workshop in Santiago on March 5", purpose_kind="CONFERENCE",
         ticket_from_others="Round trip Dulles - Santiago bought by the Inter-American Development Bank: out March 1, "
         "back March 6", ticket_from_others_suffices=True,
         sign_offs=[authorized("DIRECTOR", "Ruth Kagame-Silva", "2027-01-06")]),
    search("IAD", "SCL", "2027-03-01", {
        "latam": {"carrier": "LA", "depart": "21:10"},
        "united": {"carrier": "UA", "depart": "22:05"},
    }, [
        offer("latam-economy", "latam", "ECONOMY", 99000),
        offer("united-economy", "united", "ECONOMY", 105000),
    ]),
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "THIRD_PARTY_TICKET_COVERS_TRIP"], on_file("DIRECTOR"),
             ["THIRD_PARTY_DEVIATIONS"]),
    [THIRD, AUTH],
    "Section 8.2 (lines 602-606): when the traveller already has travel plans paid by a third party, the GS/OAS pays "
    "only 'additional expenses paid to deviate from the original travel plans'. The IDB ticket already takes him to "
    "Santiago and home around the March 5 workshop, so there is nothing for the GS/OAS to buy. The Director's "
    "authorization is on file but unused (rule 4(b)).",
    distractors=[TEC])

# ===== flag (3) =====

scenario(
    "vicuna-marsh", "flag", ["multi_leg", "unclear_phrase"], LAX_REQUEST, trip(**LAX_TRIP), lax(51000),
    expected("FLAG_FOR_APPROVAL", ["dallas-economy", "nonstop-economy"], ["ECONOMY"],
             ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"],
             ["DIRECTOR", "NOT_NAMED", "PROCUREMENT_DEPARTMENT", "SECRETARY"],
             ROUTE_CLAUSES, phrase="savings of $200 or more"),
    [COMPARABLE, PREF, FOOTNOTE, AUTH],
    "The nonstop costs exactly $200 more than the connection, which adds 150 minutes. Lines 166-167 and 389-391 make "
    "it comparable ('not higher than $200'), so the traveller's preference stands; lines 167-169 and 391-393 require "
    "the connection ('savings of $200 or more'). Both rules are inclusive and they give different tickets; nothing "
    "says which prevails. Hold either offer.",
    flag_twins=["fern-canyon", "guava-ledge"],
    ambiguity={"phrase": "savings of $200 or more",
               "readings": ["a saving of exactly $200 makes the connection required, so book the connection",
                            ("an option exactly $200 above the lowest logical fare is still comparable ('not higher "
                            "than $200'), so the traveller's nonstop may be booked")]})

scenario(
    "wren-caldera", "flag", ["approval_required"],
    "Dulles to Sao Paulo on September 13th, overnight, for the anti-corruption follow-up meetings the next afternoon. "
    "The Chief of Staff signed my Premium Fare Authorization Form for business class on this trip because of my back. "
    "Business, please.",
    trip(traveller_name="Oscar Mejia-Ruiz", traveller_title="Legal Officer",
         works_for="Department of Legal Cooperation, Secretariat for Legal Affairs", origin="IAD", destination="GRU",
         travel_date="2027-09-13", booking_date="2027-07-26", work_starts="2027-09-14 14:00",
         purpose="Anti-corruption follow-up meetings in Sao Paulo", purpose_kind="MEETING", requested_cabin="BUSINESS",
         sign_offs=[authorized("DIRECTOR", "Ines Albornoz", "2027-07-19"),
                    sign("CHIEF_OF_STAFF", "Mariano Ocampo", "PREMIUM_FARE_FORM", "2027-07-22",
                         "Premium Fare Authorization Form: business class for this trip (medical certificate on file)",
                         cabin="BUSINESS")]),
    search("IAD", "GRU", "2027-09-13", {
        "united": {"carrier": "UA", "depart": "21:30", "minutes": [595]},
        "latam": {"carrier": "LA", "depart": "22:10", "minutes": [600]},
    }, [
        offer("united-economy", "united", "ECONOMY", 99000),
        offer("united-business", "united", "BUSINESS", 420000),
        offer("latam-economy", "latam", "ECONOMY", 103000),
        offer("latam-business", "latam", "BUSINESS", 395000),
    ]),
    expected("FLAG_FOR_APPROVAL", ["latam-business"], ["BUSINESS"], ["APPROVAL_REQUIRED"], ["SECRETARY_GENERAL"],
             CLASS_CLAUSES),
    [CLASS_EXC, PREMIUM, CLASS],
    "The Premium Fare Authorization Form 'must be approved by the Secretary General' (lines 351-352; also 334-335); "
    "the Chief of Staff signed it. Hold the cheapest business fare for the Secretary General. Approval required, not "
    "'no compliant offer'.",
    flag_twins=["dahlia-mesa", "condor-flats"],
    ambiguity="none: the Secretary General's approval of the form is required and missing; the text is clear")

scenario(
    "yucca-strait", "flag", ["date_arithmetic", "month_end", "outside_air_section", "approval_required"], MEX_REQUEST,
    trip(traveller_name="Rosa Quintanilla", traveller_title="Electoral Specialist", booking_date="2026-12-15",
         sign_offs=[authorized("DIRECTOR", "Tomas Arrieta", "2026-12-15")], **MEX),
    mex(),
    expected("FLAG_FOR_APPROVAL", ["aeromexico-economy"], ["ECONOMY"], ["ADVANCE_PURCHASE_TOO_LATE", "APPROVAL_REQUIRED"],
             ["DIRECTOR", "SECRETARY"], ["ADVANCE_TIMELINESS", "TRAVEL_ARRANGEMENTS"]),
    [TIMELY, APPROVER_DEF, AUTH],
    "Authorized on December 15 for travel on January 4: 20 days, later than 'three (3) weeks prior to the travel "
    "date' (lines 280-281). 'Fares purchased late ... would therefore require additional written approval from the "
    "duly authorized official in the requesting area' (283-284): the Director or Secretary (84-85). None is on file, "
    "so hold the lowest logical fare, Aeromexico at $412.",
    flag_twins=["egret-shoal", "mango-quarry"],
    ambiguity="none: the additional written approval for a late purchase is required and missing; the text is clear",
    distractors=[ADVANCES])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios to {OUT}")


if __name__ == "__main__":
    main()
