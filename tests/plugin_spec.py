"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "oas" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 24-scenario row).
MIX = {"easy": 5, "boundary_twin": 6, "multi_rule": 4, "hidden_clause": 2, "distractor": 2, "refusal": 2, "flag": 3}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has. No overnight-stop rule; the one
# multi-traveller clause (8.5, lines 630-636) sets no number ("please contact DP"), so no multi-traveller case.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1, "dearer_option": 2,
    "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "secretary", "general", "assistant", "chair", "council", "permanent", "director", "chief", "staff", "adviser",
    "commissioner", "iachr", "human", "rights", "guest", "expert", "invited", "government", "premium", "form",
    "economy", "business", "first", "coach", "class", "fare", "full", "flexible", "refundable", "nonstop", "direct",
    "connection", "connecting", "layover", "stop", "hours", "savings", "comparable", "preference", "personal",
    "vacation", "holiday", "leave", "weekend", "saturday", "monday", "late", "weeks", "timely", "approval",
    "authorization", "own", "self", "bag", "baggage", "fee", "ancillary", "united", "carrier", "airline", "miles",
    "upgrade", "third", "party", "idb", "deviation", "procurement", "tmc", "agency", "lowest", "logical",
    "llf", "exception", "exempt", "senior",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.Position, contract.Purpose, contract.Routing, contract.SignOffSubject]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section).
MAX_PASS_ALWAYS_FLAG = 1
MAX_PASS_ALWAYS_LOWEST = 9

# Hand-built duration cases: this handbook has no duration threshold (rules.DURATION_RULES is empty); its four-hour
# limit is relative to the nonstop and is tested through the heron-pampa / ibis-knoll twins.
DURATION_CASES = []
