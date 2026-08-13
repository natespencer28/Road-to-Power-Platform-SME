#!/usr/bin/env python3
"""
Generates sample data for the Training & Certification Compliance spine project.

Dates are computed RELATIVE TO TODAY, so the mix of lapsed / expiring / current
records stays correct whenever you run it. Re-run any time your data goes stale.

    python3 generate.py

Writes six CSVs ready to import into Dataverse, in dependency order.
"""

import csv
import datetime as dt
from pathlib import Path

HERE = Path(__file__).parent
TODAY = dt.date.today()


def d(days):
    """A date `days` from today. Negative = past."""
    return (TODAY + dt.timedelta(days=days)).isoformat()


# ---------------------------------------------------------------- roles
ROLES = [
    ("ROLE-001", "Field Technician", "Operations"),
    ("ROLE-002", "Warehouse Operator", "Logistics"),
    ("ROLE-003", "Site Supervisor", "Operations"),
]

# ---------------------------------------------------------------- credentials
# code, name, validity months, category, renewal notes
CREDENTIALS = [
    ("CRED-001", "First Aid at Work", 36, "Safety",
     "One-day refresher course; book through an approved provider"),
    ("CRED-002", "Forklift Operator", 36, "Equipment",
     "Practical reassessment required"),
    ("CRED-003", "Working at Height", 24, "Safety",
     "Half-day refresher"),
    ("CRED-004", "Fire Warden", 24, "Safety",
     "Site-specific; must be renewed at current site"),
    ("CRED-005", "Manual Handling", 12, "Safety",
     "Available as e-learning"),
    ("CRED-006", "Confined Space Entry", 12, "Specialist",
     "Medical clearance required before booking"),
]

# ---------------------------------------------------------------- providers
PROVIDERS = [
    ("PROV-001", "Northgate Safety Training", "bookings@northgate-training.example",
     "0100 555 0142", "Classroom"),
    ("PROV-002", "Meridian Skills Academy", "enquiries@meridian-skills.example",
     "0100 555 0198", "Classroom"),
    ("PROV-003", "SafeStart Online", "support@safestart-online.example",
     "", "E-learning"),
    ("PROV-004", "In-house Training Team", "training@yourcompany.example",
     "", "Internal"),
]

# ---------------------------------------------------------------- people
# code, first, last, email, role, manager code, start offset days
PEOPLE = [
    ("EMP-001", "Dana",    "Whitfield", "dana.whitfield@example.com",   "ROLE-003", "",         -3200),
    ("EMP-002", "Marcus",  "Oyelaran",  "marcus.oyelaran@example.com",  "ROLE-003", "",         -2900),
    ("EMP-003", "Priya",   "Raghavan",  "priya.raghavan@example.com",   "ROLE-001", "EMP-001",  -2400),
    ("EMP-004", "Tomas",   "Lindqvist", "tomas.lindqvist@example.com",  "ROLE-001", "EMP-001",  -1900),
    ("EMP-005", "Aisha",   "Bello",     "aisha.bello@example.com",      "ROLE-001", "EMP-001",  -1500),
    ("EMP-006", "Grant",   "Mullins",   "grant.mullins@example.com",    "ROLE-002", "EMP-002",  -2100),
    ("EMP-007", "Sofia",   "Marchetti", "sofia.marchetti@example.com",  "ROLE-002", "EMP-002",  -1300),
    ("EMP-008", "Kwame",   "Asare",     "kwame.asare@example.com",      "ROLE-002", "EMP-002",    -45),
]

# ---------------------------------------------------------------- requirements
# role, credential, mandatory, grace days
REQUIREMENTS = [
    ("ROLE-001", "CRED-001", "Yes", 30),
    ("ROLE-001", "CRED-003", "Yes", 14),
    ("ROLE-001", "CRED-005", "Yes", 30),
    ("ROLE-001", "CRED-006", "No",  0),
    ("ROLE-002", "CRED-002", "Yes",  0),
    ("ROLE-002", "CRED-005", "Yes", 30),
    ("ROLE-002", "CRED-001", "No",  30),
    ("ROLE-003", "CRED-001", "Yes", 30),
    ("ROLE-003", "CRED-004", "Yes", 14),
    ("ROLE-003", "CRED-005", "Yes", 30),
    ("ROLE-003", "CRED-003", "Yes", 14),
]

# ---------------------------------------------------------------- completions
# The deliberate spread. Each tuple:
#   person, credential, provider, days-until-expiry, status label, evidence?, cost
#
# Negative expiry = already lapsed. This mix is what makes the Week 12
# reminder flows testable — uniform dates would hide bugs.
COMPLETIONS = [
    # --- LAPSED (reminders should already have fired and escalated) ---
    ("EMP-003", "CRED-005", "PROV-003",  -47, "Lapsed",        "Yes", 45),
    ("EMP-006", "CRED-002", "PROV-002",  -12, "Lapsed",        "Yes", 380),
    ("EMP-004", "CRED-003", "PROV-001",   -5, "Lapsed",        "No",  240),

    # --- EXPIRING INSIDE 30 DAYS (the 30-day reminder tier) ---
    ("EMP-001", "CRED-004", "PROV-004",    8, "Expiring Soon", "Yes",   0),
    ("EMP-005", "CRED-005", "PROV-003",   19, "Expiring Soon", "Yes",  45),
    ("EMP-007", "CRED-005", "PROV-003",   27, "Expiring Soon", "Yes",  45),

    # --- 60-DAY TIER ---
    ("EMP-002", "CRED-003", "PROV-001",   44, "Expiring Soon", "Yes", 240),
    ("EMP-003", "CRED-001", "PROV-001",   58, "Expiring Soon", "Yes", 165),

    # --- 90-DAY TIER ---
    ("EMP-004", "CRED-001", "PROV-002",   76, "Current",       "Yes", 165),
    ("EMP-006", "CRED-005", "PROV-003",   88, "Current",       "Yes",  45),

    # --- COMFORTABLY CURRENT ---
    ("EMP-001", "CRED-001", "PROV-001",  310, "Current",       "Yes", 165),
    ("EMP-001", "CRED-003", "PROV-001",  198, "Current",       "Yes", 240),
    ("EMP-001", "CRED-005", "PROV-003",  145, "Current",       "Yes",  45),
    ("EMP-002", "CRED-001", "PROV-002",  402, "Current",       "Yes", 165),
    ("EMP-002", "CRED-004", "PROV-004",  221, "Current",       "Yes",   0),
    ("EMP-002", "CRED-005", "PROV-003",  167, "Current",       "Yes",  45),
    ("EMP-003", "CRED-003", "PROV-001",  289, "Current",       "Yes", 240),
    ("EMP-003", "CRED-006", "PROV-002",  132, "Current",       "Yes", 520),
    ("EMP-004", "CRED-005", "PROV-003",  112, "Current",       "Yes",  45),
    ("EMP-005", "CRED-001", "PROV-001",  455, "Current",       "Yes", 165),
    ("EMP-005", "CRED-003", "PROV-001",  334, "Current",       "Yes", 240),
    ("EMP-006", "CRED-001", "PROV-002",  278, "Current",       "Yes", 165),
    ("EMP-007", "CRED-002", "PROV-002",  611, "Current",       "Yes", 380),
    ("EMP-002", "CRED-002", "PROV-002",  520, "Current",       "Yes", 380),
    ("EMP-001", "CRED-002", "PROV-002",  445, "Current",       "Yes", 380),

    # --- HISTORIC: superseded records, same person + credential ---
    # These prove your "latest completion wins" logic. If your app shows
    # Priya as lapsed on First Aid because it found the 2023 record, you
    # have a bug — and you want to find it now, not in production.
    ("EMP-003", "CRED-001", "PROV-001", -640, "Superseded",    "Yes", 150),
    ("EMP-001", "CRED-001", "PROV-001", -420, "Superseded",    "Yes", 150),
    ("EMP-006", "CRED-002", "PROV-002", -800, "Superseded",    "Yes", 350),

    # --- AWAITING VERIFICATION (sits mid-BPF, evidence not yet approved) ---
    ("EMP-004", "CRED-006", "PROV-002",  350, "Pending",       "No",  520),
    ("EMP-007", "CRED-001", "PROV-003",  365, "Pending",       "No",  165),
]

# EMP-008 (Kwame, new starter, 45 days in) has NO completions at all.
# He is the empty state — required to hold Forklift and Manual Handling,
# holds neither. Empty states are where apps usually look broken, so
# build against him early.


def months_before(expiry_days, validity_months):
    """Completed date = expiry minus the credential's validity window."""
    return expiry_days - int(validity_months * 30.44)


def write(name, header, rows):
    path = HERE / name
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {name:<28} {len(rows):>3} rows")


print(f"Generating sample data relative to {TODAY.isoformat()}\n")

write("1-roles.csv",
      ["Role Code", "Role Name", "Department"],
      ROLES)

write("2-credentials.csv",
      ["Credential Code", "Credential Name", "Validity Months", "Category", "Renewal Notes"],
      CREDENTIALS)

write("3-providers.csv",
      ["Provider Code", "Provider Name", "Email", "Phone", "Delivery Mode"],
      PROVIDERS)

write("4-people.csv",
      ["Employee Code", "First Name", "Last Name", "Email", "Role Code", "Manager Code", "Start Date"],
      [(c, f, l, e, r, m, d(s)) for c, f, l, e, r, m, s in PEOPLE])

write("5-role-requirements.csv",
      ["Role Code", "Credential Code", "Mandatory", "Grace Days"],
      REQUIREMENTS)

comp_rows = []
for i, (person, cred, prov, exp_days, status, evidence, cost) in enumerate(COMPLETIONS, 1):
    validity = next(c[2] for c in CREDENTIALS if c[0] == cred)
    comp_rows.append((
        f"COMP-{i:03d}", person, cred, prov,
        d(months_before(exp_days, validity)),
        d(exp_days),
        status, evidence, cost,
    ))

write("6-completions.csv",
      ["Completion Code", "Employee Code", "Credential Code", "Provider Code",
       "Completed Date", "Expiry Date", "Status", "Evidence Attached", "Cost"],
      comp_rows)

# ---------------------------------------------------------------- summary
lapsed = sum(1 for c in COMPLETIONS if c[3] < 0 and c[4] == "Lapsed")
soon30 = sum(1 for c in COMPLETIONS if 0 <= c[3] <= 30)
soon60 = sum(1 for c in COMPLETIONS if 30 < c[3] <= 60)
soon90 = sum(1 for c in COMPLETIONS if 60 < c[3] <= 90)
superseded = sum(1 for c in COMPLETIONS if c[4] == "Superseded")
pending = sum(1 for c in COMPLETIONS if c[4] == "Pending")

print(f"""
Spread check — this is what makes the Week 12 flows testable:
  Lapsed now .................... {lapsed}
  Expiring within 30 days ....... {soon30}
  Expiring 31-60 days ........... {soon60}
  Expiring 61-90 days ........... {soon90}
  Superseded (older duplicates) . {superseded}
  Pending verification .......... {pending}
  People with zero records ...... 1  (EMP-008, new starter)

Import in numbered order — 1 through 6. Later files reference earlier ones.
""")
