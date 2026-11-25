"""Each tool's and task's typed input and output (see nanoagent.plugin.v0001.contract): declarations only.

The first part is the original-handbook template's shared contract and is the same in every plugin made from
it. The HANDBOOK-SPECIFIC part in the middle is filled per handbook: the scenario ids, the closed lists of
approvers and sections, and the trip record; the shared inputs and outputs after it refer to those names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output

# ---------------------------------------------------------------------------------------------------------
# SHARED (template): keep identical across plugins, except the agent task's id in Task.BOOK_FLIGHT.
# ---------------------------------------------------------------------------------------------------------


class Tool(Enum):
    BOOKING_REQUIREMENTS = "booking_requirements"
    GET_TRIP = "get_trip"
    SEARCH_FLIGHTS = "search_flights"
    SOLVE_BOOKING = "solve_booking"


class Task(Enum):
    BOOKING_REQUIREMENTS = "booking-requirements"
    SEARCH_FLIGHTS = "search-flights"
    BOOK_FLIGHT = "book-oas-flight"


class Decision(Enum):
    BOOK = "BOOK"
    REFUSE = "REFUSE"
    FLAG_FOR_APPROVAL = "FLAG_FOR_APPROVAL"


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"
    NONE = "NONE"


class ReasonCode(Enum):
    """Why the decision was made. The list is shared by every handbook plugin, so it also holds reasons
    that a given handbook never uses."""

    LOWEST_FARE = "LOWEST_FARE"
    UPGRADE_NOT_ELIGIBLE = "UPGRADE_NOT_ELIGIBLE"
    CLIENT_REIMBURSABLE = "CLIENT_REIMBURSABLE"
    UPGRADE_WITHIN_FARE_MARGIN = "UPGRADE_WITHIN_FARE_MARGIN"
    MEDICAL_NEED = "MEDICAL_NEED"
    COST_SAVINGS = "COST_SAVINGS"
    NO_ECONOMY_SEATS_URGENT = "NO_ECONOMY_SEATS_URGENT"
    TRAVELER_PAYS_UPGRADE = "TRAVELER_PAYS_UPGRADE"
    LONG_FLIGHT_APPROVED = "LONG_FLIGHT_APPROVED"
    LONG_FLIGHT_CONDITION_NOT_MET = "LONG_FLIGHT_CONDITION_NOT_MET"
    PREMIUM_ECONOMY_ALLOWED = "PREMIUM_ECONOMY_ALLOWED"
    UPGRADE_COST_NOT_NOMINAL = "UPGRADE_COST_NOT_NOMINAL"
    ALTERNATE_ROUTE_WITHIN_MARGIN = "ALTERNATE_ROUTE_WITHIN_MARGIN"
    ALTERNATE_ROUTE_TOO_EXPENSIVE = "ALTERNATE_ROUTE_TOO_EXPENSIVE"
    LOYALTY_PROGRAM_PREFERENCE = "LOYALTY_PROGRAM_PREFERENCE"
    COMPANION_NOT_COVERED = "COMPANION_NOT_COVERED"
    PERSONAL_TRAVEL_NOT_COVERED = "PERSONAL_TRAVEL_NOT_COVERED"
    OUTSIDE_POLICY_SCOPE = "OUTSIDE_POLICY_SCOPE"
    NO_COMPLIANT_OFFER = "NO_COMPLIANT_OFFER"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNCLEAR_POLICY_TEXT = "UNCLEAR_POLICY_TEXT"
    ADVANCE_PURCHASE_TOO_LATE = "ADVANCE_PURCHASE_TOO_LATE"
    DISTANCE_BELOW_MINIMUM = "DISTANCE_BELOW_MINIMUM"
    DRIVING_EXPECTED = "DRIVING_EXPECTED"
    RAIL_PREFERRED = "RAIL_PREFERRED"
    REFUNDABLE_FARE_NOT_ALLOWED = "REFUNDABLE_FARE_NOT_ALLOWED"
    PREFERRED_CARRIER_REQUIRED = "PREFERRED_CARRIER_REQUIRED"
    CONNECTION_TOO_LONG = "CONNECTION_TOO_LONG"
    OVERNIGHT_STOP_REQUIRED = "OVERNIGHT_STOP_REQUIRED"
    NATIONAL_CARRIER_REQUIRED = "NATIONAL_CARRIER_REQUIRED"
    SENIOR_ROLE_ENTITLEMENT = "SENIOR_ROLE_ENTITLEMENT"
    INTERNATIONAL_LONG_FLIGHT = "INTERNATIONAL_LONG_FLIGHT"
    TRAVELLER_LIMIT_PER_FLIGHT = "TRAVELLER_LIMIT_PER_FLIGHT"
    # HANDBOOK-SPECIFIC reason codes go below this line; keep every shared one above.
    ECONOMY_CLASS_REQUIRED = "ECONOMY_CLASS_REQUIRED"
    PREMIUM_FARE_AUTHORIZED = "PREMIUM_FARE_AUTHORIZED"
    FULL_ECONOMY_FARE_AUTHORIZED = "FULL_ECONOMY_FARE_AUTHORIZED"
    COMPARABLE_FARE_OPTION = "COMPARABLE_FARE_OPTION"
    LATE_PURCHASE_APPROVED = "LATE_PURCHASE_APPROVED"
    ANCILLARY_FEES_EXCLUDED = "ANCILLARY_FEES_EXCLUDED"
    PERSONAL_COST_PAID_BY_TRAVELER = "PERSONAL_COST_PAID_BY_TRAVELER"
    PERSONAL_CHANGE_NOT_ALLOWED = "PERSONAL_CHANGE_NOT_ALLOWED"
    THIRD_PARTY_TICKET_COVERS_TRIP = "THIRD_PARTY_TICKET_COVERS_TRIP"
    # Decoys: codes for rules of other handbooks that this one lacks, so the list hints at none of its own rules.
    NEXT_OF_KIN_TRAVEL = "NEXT_OF_KIN_TRAVEL"
    FLY_AMERICA_US_CARRIER_REQUIRED = "FLY_AMERICA_US_CARRIER_REQUIRED"
    OPEN_SKIES_AGREEMENT = "OPEN_SKIES_AGREEMENT"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    EXTENDED_TRAVEL_SAVINGS = "EXTENDED_TRAVEL_SAVINGS"
    DENIED_BOARDING_NOT_ALLOWED = "DENIED_BOARDING_NOT_ALLOWED"
    CHANCELLOR_WRITTEN_AUTHORIZATION = "CHANCELLOR_WRITTEN_AUTHORIZATION"
    DOUBLE_BOOKING_PROHIBITED = "DOUBLE_BOOKING_PROHIBITED"
    PRIVATE_AIRCRAFT_NOT_APPROVED = "PRIVATE_AIRCRAFT_NOT_APPROVED"
    TRAVEL_PACKAGE_NOT_ITEMIZED = "TRAVEL_PACKAGE_NOT_ITEMIZED"


class TripType(Enum):
    ONE_WAY = "ONE_WAY"
    ROUND_TRIP = "ROUND_TRIP"


class Topic(Enum):
    ALL = "ALL"
    FIELDS = "FIELDS"
    AIRPORTS = "AIRPORTS"


CODE = "An IATA airport code, e.g. JFK"


@dataclass
class Airport(Output):
    code: Annotated[str, CODE]
    name: Annotated[str, "The airport's name"]
    city: Annotated[str, "The city it serves"]
    country: Annotated[str, "Its country, as an ISO code"]


@dataclass
class Segment(Output):
    flight_number: Annotated[str, "The airline's flight number, e.g. BA 117"]
    origin: Annotated[str, CODE]
    destination: Annotated[str, CODE]
    depart_local: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, local time at that airport"]
    arrive_local: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, local time at that airport"]
    depart_utc: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, UTC"]
    arrive_utc: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, UTC"]
    scheduled_minutes: Annotated[int, "Its scheduled time from departure to arrival, in minutes"]


@dataclass
class Offer(Output):
    offer_id: Annotated[str, "The offer's id, to submit when booking or holding it"]
    carrier: Annotated[str, "The airline"]
    trip_type: Annotated[TripType, "ONE_WAY, or ROUND_TRIP when the fare covers the flights out and back"]
    cabin: Annotated[Cabin, "The cabin sold on every flight of the offer"]
    fare_cents: Annotated[int, "The whole fare for one passenger, in cents of the search's currency"]
    seats_available: Annotated[bool, "False when this cabin is sold out on these flights: it is listed but cannot be bought"]
    refundable: Annotated[bool, "Whether the fare can be refunded or changed without a fee"]
    stops: Annotated[int, "Connections on the way out; zero for a nonstop"]
    segments: Annotated[list[Segment], "The flights out, in order"]
    layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights out"]
    stopover_nights: Annotated[list[bool], "Per connection out: true when it is a ticketed stopover with a hotel night booked"]
    flying_minutes: Annotated[int, "The flights' scheduled minutes out added together, ground time left out"]
    elapsed_minutes: Annotated[int, "Minutes from the first departure out to the last arrival, ground time included"]
    return_segments: Annotated[list[Segment], "For a round trip, the flights back, in order; empty otherwise"]
    return_layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights back"]
    return_stopover_nights: Annotated[list[bool], "Per connection back: true for a ticketed stopover with a hotel night"]
    return_flying_minutes: Annotated[int, "The flights' scheduled minutes back added together; zero one way"]
    return_elapsed_minutes: Annotated[int, "Minutes from the first departure back to the last arrival; zero one way"]


# ---------------------------------------------------------------------------------------------------------
# HANDBOOK-SPECIFIC: Travel Policy of the General Secretariat of the Organization of American States
# (Administrative Memorandum 122, Appendix A).
# ---------------------------------------------------------------------------------------------------------


class Scenario(Enum):
    AGAVE_RIDGE = "agave-ridge"
    BASALT_VINE = "basalt-vine"
    CONDOR_FLATS = "condor-flats"
    DAHLIA_MESA = "dahlia-mesa"
    EGRET_SHOAL = "egret-shoal"
    FERN_CANYON = "fern-canyon"
    GUAVA_LEDGE = "guava-ledge"
    HERON_PAMPA = "heron-pampa"
    IBIS_KNOLL = "ibis-knoll"
    JACARANDA_COVE = "jacaranda-cove"
    KAPOK_STRAND = "kapok-strand"
    LLAMA_TERRACE = "llama-terrace"
    MANGO_QUARRY = "mango-quarry"
    NOPAL_HARBOR = "nopal-harbor"
    OCELOT_SPIRE = "ocelot-spire"
    PUMA_LAGOON = "puma-lagoon"
    QUETZAL_BANK = "quetzal-bank"
    RHEA_DUNE = "rhea-dune"
    SISAL_CREST = "sisal-crest"
    TAPIR_HOLLOW = "tapir-hollow"
    URCHIN_BAY = "urchin-bay"
    VICUNA_MARSH = "vicuna-marsh"
    WREN_CALDERA = "wren-caldera"
    YUCCA_STRAIT = "yucca-strait"


class Approver(Enum):
    """Roles that may sign off. NONE: the decision relies on no one's sign-off, given or awaited (one for
    something else may be on file). NOT_NAMED: one is needed, but the handbook names no role."""

    NONE = "NONE"
    NOT_NAMED = "NOT_NAMED"
    SUPERVISOR = "SUPERVISOR"
    DIRECTOR = "DIRECTOR"
    SECRETARY = "SECRETARY"
    CHIEF_OF_STAFF = "CHIEF_OF_STAFF"
    ASSISTANT_SECRETARY_GENERAL = "ASSISTANT_SECRETARY_GENERAL"
    SECRETARY_GENERAL = "SECRETARY_GENERAL"
    PERMANENT_COUNCIL_CHAIR = "PERMANENT_COUNCIL_CHAIR"
    ADMINISTRATION_FINANCE_SECRETARY = "ADMINISTRATION_FINANCE_SECRETARY"
    PROCUREMENT_DEPARTMENT = "PROCUREMENT_DEPARTMENT"
    HUMAN_RESOURCES = "HUMAN_RESOURCES"
    TRAVEL_AGENCY = "TRAVEL_AGENCY"
    CHIEF_FINANCIAL_OFFICER = "CHIEF_FINANCIAL_OFFICER"
    BOARD_OF_EXTERNAL_AUDITORS = "BOARD_OF_EXTERNAL_AUDITORS"


class Clause(Enum):
    """The handbook's sections, by heading."""

    INTRODUCTION = "INTRODUCTION"
    POLICY_SUMMARY = "POLICY_SUMMARY"
    DEFINITIONS = "DEFINITIONS"
    OAS_TRAVELER = "OAS_TRAVELER"
    AUTHORIZED_APPROVER = "AUTHORIZED_APPROVER"
    TRAVEL_CLASS = "TRAVEL_CLASS"
    PREMIUM_TRAVEL = "PREMIUM_TRAVEL"
    LOWEST_LOGICAL_FARE_DEFINITION = "LOWEST_LOGICAL_FARE_DEFINITION"
    PERSONAL_PREFERENCE_DEFINITION = "PERSONAL_PREFERENCE_DEFINITION"
    COMPARABLE_OPTIONS = "COMPARABLE_OPTIONS"
    RAIL_TRAVEL = "RAIL_TRAVEL"
    MANDATORY_TRAVEL_AGENCY = "MANDATORY_TRAVEL_AGENCY"
    TRAVEL_ARRANGEMENTS = "TRAVEL_ARRANGEMENTS"
    ADVANCE_TIMELINESS = "ADVANCE_TIMELINESS"
    AUTHORIZING = "AUTHORIZING"
    OWN_APPROVAL = "OWN_APPROVAL"
    TRANSPORTATION = "TRANSPORTATION"
    CLASS_OF_SERVICE = "CLASS_OF_SERVICE"
    FARES = "FARES"
    CABIN_EXCEPTIONS = "CABIN_EXCEPTIONS"
    PRICE_MATCH = "PRICE_MATCH"
    LOWEST_LOGICAL_FARE = "LOWEST_LOGICAL_FARE"
    CONNECTIONS = "CONNECTIONS"
    PERSONAL_PREFERENCE = "PERSONAL_PREFERENCE"
    SELECTION_OF_CARRIER = "SELECTION_OF_CARRIER"
    ALTERNATE_AIRPORTS = "ALTERNATE_AIRPORTS"
    AIRLINE_UPGRADES = "AIRLINE_UPGRADES"
    ANCILLARY_FEES = "ANCILLARY_FEES"
    FREQUENT_FLIER = "FREQUENT_FLIER"
    SPECIAL_CIRCUMSTANCES = "SPECIAL_CIRCUMSTANCES"
    OFFICIAL_WITH_PERSONAL = "OFFICIAL_WITH_PERSONAL"
    PERMISSIBLE_CHANGES = "PERMISSIBLE_CHANGES"
    PERSONAL_COSTS = "PERSONAL_COSTS"
    THIRD_PARTY_DEVIATIONS = "THIRD_PARTY_DEVIATIONS"
    FLYING_TOGETHER = "FLYING_TOGETHER"
    HUMAN_RIGHTS_COMMISSIONERS = "HUMAN_RIGHTS_COMMISSIONERS"
    PAYMENT_RESTRICTED_INSTITUTIONS = "PAYMENT_RESTRICTED_INSTITUTIONS"
    GROUPS_AND_MEETINGS = "GROUPS_AND_MEETINGS"
    PERSONAL_VACATION = "PERSONAL_VACATION"
    PERSONAL_ACCOUNTABILITY = "PERSONAL_ACCOUNTABILITY"


class Position(Enum):
    STAFF_MEMBER = "STAFF_MEMBER"
    DIRECTOR = "DIRECTOR"
    SECRETARY = "SECRETARY"
    CHIEF_OF_STAFF = "CHIEF_OF_STAFF"
    ADVISER = "ADVISER"
    ASSISTANT_SECRETARY_GENERAL = "ASSISTANT_SECRETARY_GENERAL"
    SECRETARY_GENERAL = "SECRETARY_GENERAL"
    PERMANENT_COUNCIL_CHAIR = "PERMANENT_COUNCIL_CHAIR"
    PERMANENT_REPRESENTATIVE = "PERMANENT_REPRESENTATIVE"
    IACHR_COMMISSIONER = "IACHR_COMMISSIONER"
    INVITED_EXPERT = "INVITED_EXPERT"
    CONSULTANT = "CONSULTANT"


class Purpose(Enum):
    MISSION = "MISSION"
    MEETING = "MEETING"
    CONFERENCE = "CONFERENCE"
    HEARING = "HEARING"
    WORK_ASSIGNMENT = "WORK_ASSIGNMENT"
    HOME_LEAVE = "HOME_LEAVE"
    VACATION = "VACATION"


class Routing(Enum):
    ANY = "ANY"
    NONSTOP = "NONSTOP"


class SignOffSubject(Enum):
    TRAVEL_AUTHORIZATION = "TRAVEL_AUTHORIZATION"
    PREMIUM_FARE_FORM = "PREMIUM_FARE_FORM"
    LATE_PURCHASE_APPROVAL = "LATE_PURCHASE_APPROVAL"
    PERSONAL_DAYS = "PERSONAL_DAYS"
    EMERGENCY_TRAVEL = "EMERGENCY_TRAVEL"
    CARRIER_REQUEST = "CARRIER_REQUEST"


@dataclass
class SignOff(Output):
    role: Annotated[Approver, "The signer's role"]
    name: Annotated[str, "Their name"]
    subject: Annotated[SignOffSubject, "What they signed"]
    cabin: Annotated[Cabin, "The cabin a premium fare form names; NONE for every other kind of sign-off"]
    signed_on: Annotated[str, "The day it was signed, YYYY-MM-DD"]
    covers: Annotated[str, "What the sign-off says, in plain words"]


@dataclass
class Trip(Output):
    traveller_name: Annotated[str, "Who flies"]
    traveller_title: Annotated[str, "Their title"]
    position: Annotated[Position, "The traveller's position"]
    works_for: Annotated[str, "The traveller's department or office, or their own organisation for someone from outside"]
    origin: Annotated[Airport, "Where the flight leaves from"]
    destination: Annotated[Airport, "Where it goes"]
    travel_date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport"]
    business_travel_date: Annotated[str, "The day the work itself would need the flight, YYYY-MM-DD; the same as travel_date unless the traveller adds days of their own"]
    return_date: Annotated[str, "For a round trip bought as one fare, the day to fly back, YYYY-MM-DD; empty for one way"]
    booking_date: Annotated[str, "Today in this world, the day the ticket is bought, YYYY-MM-DD"]
    work_starts: Annotated[str, "When the work at the destination begins: YYYY-MM-DD HH:MM, local time there; empty when the trip has no work"]
    purpose: Annotated[str, "Why the trip is made, in plain words"]
    purpose_kind: Annotated[Purpose, "The kind of trip"]
    requested_cabin: Annotated[Cabin, "The cabin the traveller asks for"]
    requested_routing: Annotated[Routing, "NONSTOP when the traveller asks for a nonstop flight; ANY otherwise"]
    requested_airline: Annotated[str, "The airline the traveller asks for, as search_flights names airlines; empty when none"]
    requested_refundable: Annotated[bool, "Whether the traveller asks for a fare that can be refunded or changed without a fee"]
    traveller_pays_difference: Annotated[bool, "Whether the traveller offers to pay, out of pocket, what the requested ticket costs above the one the organisation would buy"]
    checked_bag_fees: Annotated[str, "Checked bag fees the traveller expects to pay, by airline; empty when none are given"]
    ticket_from_others: Annotated[str, "A ticket for this trip already bought by another organisation, and what it covers; empty when none"]
    ticket_from_others_suffices: Annotated[bool, "Whether that ticket already takes the traveller to the work and home again on the days needed; false when there is none"]
    sign_offs: Annotated[list[SignOff], "Sign-offs on file for this trip, each signed on or before today"]


# ---------------------------------------------------------------------------------------------------------
# SHARED (template), continued: the tools' and tasks' inputs and outputs.
# ---------------------------------------------------------------------------------------------------------


@dataclass
class TaskInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    request: Annotated[str, "The traveller's request, in their own words"]


@dataclass
class TripInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id, as the task input gives it"]


@dataclass
class TripOutput(Output):
    scenario: Annotated[Scenario, "The case id"]
    request: Annotated[str, "The traveller's request, in their own words"]
    trip: Annotated[Trip, "The trip record behind the request"]


@dataclass
class SearchInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    origin: Annotated[str, "The airport to leave from: An IATA airport code, e.g. JFK"]
    destination: Annotated[str, "The airport to fly to: An IATA airport code, e.g. JFK"]
    date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport, on or after the booking date"]
    return_date: Annotated[str, "For round-trip fares, the day to fly back, YYYY-MM-DD, local at the destination; empty for one way"]


@dataclass
class SearchOutput(Output):
    note: Annotated[str, "Where the offers come from, and a word when this case lists none for the search"]
    currency: Annotated[str, "The currency of every fare, as an ISO code"]
    offers: Annotated[list[Offer], "Every offer leaving on that local date, in departure order"]


@dataclass
class BookingOutput(Output):
    decision: Annotated[
        Decision,
        "BOOK: buy offer_id now. REFUSE: buy nothing, because the organisation buys no ticket at all for this request. "
        "FLAG_FOR_APPROVAL: hold offer_id and buy nothing yet, because someone must approve it first or "
        "the handbook's words leave the answer open",
    ]
    offer_id: Annotated[str, "The offer bought or held, exactly as search_flights listed it; empty when refusing"]
    cabin: Annotated[Cabin, "That offer's cabin; NONE when refusing"]
    reason_code: Annotated[ReasonCode, "Why, from the closed list"]
    approver: Annotated[
        Approver,
        "The role whose sign-off this decision relies on, whether already on file or still awaited; NONE when "
        "this decision relies on no one's sign-off, even if a sign-off for something else is on file; NOT_NAMED "
        "when a sign-off is needed but the handbook names no role",
    ]
    clause: Annotated[Clause, "The handbook section the decision rests on"]


@dataclass
class SolveOutput(Output):
    trip: Annotated[Trip, "The trip record"]
    offers: Annotated[list[Offer], "Every offer on the trip's route and date"]
    decision: Annotated[Decision, "The correct decision"]
    offer_ids: Annotated[list[str], "Every offer id that is a correct choice; empty when refusing"]
    cabins: Annotated[list[Cabin], "Every correct cabin"]
    reason_codes: Annotated[list[ReasonCode], "Every accepted reason"]
    approvers: Annotated[list[Approver], "Every accepted approver"]
    clauses: Annotated[list[Clause], "Every accepted section"]
    unclear_phrase: Annotated[str, "For a hold over unclear words, those words; empty otherwise"]
    explanation: Annotated[str, "How the answer key reached the answer"]


@dataclass
class FieldHelp(Output):
    name: Annotated[str, "The trip record field's name"]
    kind: Annotated[str, "Its type"]
    description: Annotated[str, "What it means"]


@dataclass
class RequirementsInput(Output):
    topic: Annotated[Topic, "ALL for everything, FIELDS for the trip record's fields, AIRPORTS for the airport list"]


@dataclass
class RequirementsOutput(Output):
    fields: Annotated[list[FieldHelp], "The trip record's fields; empty for AIRPORTS"]
    conventions: Annotated[list[str], "How times, dates, fares and seats work in this world; empty for AIRPORTS"]
    airports: Annotated[list[Airport], "The airports the simulated world knows; empty for FIELDS"]


TOOLS = {
    Tool.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Tool.GET_TRIP: (TripInput, TripOutput),
    Tool.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Tool.SOLVE_BOOKING: (TaskInput, SolveOutput),
}
TASKS = {
    Task.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Task.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Task.BOOK_FLIGHT: (TaskInput, BookingOutput),
}
