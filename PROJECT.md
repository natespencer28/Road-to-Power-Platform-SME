# Spine Project — Training & Certification Compliance

The one solution you build across all 24 weeks. Each phase adds a product; nothing gets thrown away.

**The problem it solves:** roles require credentials, credentials expire, and somebody needs to know who is falling out of compliance *before* it happens rather than after. Today that is almost certainly a spreadsheet that one person maintains and nobody else trusts.

---

## Data model

Six tables and one join. Deliberately small — Week 2 should be spent learning Dataverse, not fighting your own schema.

```
        Role ────────< Role Requirement >──────── Credential
          │                                            │
          │                                            │
        Person ──────────< Completion >────────────────┘
                                │
                                └──── Training Provider
```

| Table | What it holds | Notes |
|---|---|---|
| **Person** | Staff member, their role, their manager | Consider using the built-in Contact table — decide in Week 10 and write down why |
| **Role** | Job role: Technician, Nurse, Driver, Operator | Small reference table |
| **Credential** | A certification or training type, plus its validity period in months | "Forklift Operator", valid 36 months |
| **Role Requirement** | Joins Role to Credential — who needs what | Also holds *mandatory vs optional* and any grace period |
| **Completion** | The heart of it: person + credential + completed date + expiry date + evidence | Everything else exists to serve this table |
| **Training Provider** | Who delivered it, cost, contact | Lets you report on spend later |

**The one modeling decision worth thinking about:** Role Requirement could be a plain N:N relationship between Role and Credential. Make it a table instead — you need somewhere to put *mandatory*, *grace period*, and eventually *effective date*. An N:N gives you nowhere to hang that. This is the exact tradeoff Week 2's AI drill asks you to argue.

---

## The logic that makes it work

Everything downstream depends on one calculation: **how many days until this expires.**

| Layer | What lives there | Week |
|---|---|---|
| Calculated column | Days until expiry; status (Current / Expiring Soon / Lapsed) | 3 |
| Rollup column | Lapsed credential count per person | 3 |
| Business rule | Require evidence before a completion can be marked done | 3, 7 |
| Business process flow | Required → Scheduled → Attended → Evidence Submitted → Verified | 7 |
| Cloud flow | Nightly expiry scan; reminders at 90 / 60 / 30 days; escalation | 12, 13 |

**The architectural question you'll settle in Week 15:** is status a calculated column read live, or a value a nightly flow stamps onto the record? Both work at 500 rows. They diverge sharply at 100,000, and they behave differently in reporting. Deciding this in writing, with reasons, is the single most SME-ish thing in the whole plan.

---

## What each product contributes

| Weeks | Product | What you build |
|---|---|---|
| 2–4 | **Dataverse** | Schema, expiry logic, three security roles |
| 6–7 | **Model-driven app** | Compliance officer's back office — every person, every gap |
| 8–11 | **Canvas app** | "My Training" for staff; team view for managers; certificate photo capture; badge scan for session check-in |
| 12–16 | **Power Automate** | Nightly scan, tiered reminders, evidence approval, escalation, weekly digest, spreadsheet import |
| 17–19 | **Power Pages** | Staff portal — see your own record, upload a certificate, no licence needed |
| 20–23 | **Copilot Studio** | Agent answering "am I current", "what am I missing", "how do I renew" |
| 24 | **ALM** | Managed solution, environment variables, DEV → TEST → PROD pipeline, DLP |

---

## Three security roles

Design these once in Week 4; the portal in Week 18 mirrors them exactly.

| Role | Sees | Dataverse depth | Power Pages scope |
|---|---|---|---|
| **Staff** | Only their own completions | User | Self |
| **Manager** | Their direct reports' completions | Business Unit / Parent-Child | Contact or Account |
| **Compliance Officer** | Everything, read and write | Organization | Global |

This mapping is why this project suits the curriculum so well. Portal table permissions are usually taught abstractly; here the Self scope is the entire reason the portal exists.

---

## Sample data to load in Week 2

Enough to be realistic, small enough to eyeball.

- **8 people** across **3 roles**, with at least two reporting to the same manager
- **6 credentials** with different validity periods — 12, 24 and 36 months
- **~40 completions**, with expiry dates deliberately spread:
  - a few already lapsed
  - a few expiring inside 30 days
  - a few at 60 and 90 days
  - the rest comfortably current
- **One person deliberately missing a mandatory credential** — that empty state is what the whole solution is for, and empty states are where apps usually look broken

That staggered spread is what makes Week 12's reminder flows testable. Uniform dates will hide bugs.

---

## Scope discipline

Things that will tempt you and should wait until after Week 24:

- Integrating with a real HR system or LMS. Use invented data; waiting on someone else's API access is the classic way to stall in Week 2.
- Cost tracking and budget reporting. Interesting, but it teaches you nothing new.
- Multi-org or multi-country compliance rules. Adds complexity without adding a product.
- Anything involving real personnel records before Week 24's DLP review. Build on fake people until the governance layer exists.

The plan already has a rebuild built into it. Weeks 21–24 are where you fix the schema decisions you got wrong in Week 2 — and you will get some wrong. That's the design, not a failure.

---

## A useful side effect

Load your own certification dates into it: PL-900 in Week 5, AB-410 in Week 21, AB-620 in Week 24. Most Microsoft associate certifications now renew annually through free Microsoft Learn assessments, and the renewal window is easy to miss.

By Week 13 the solution will email you about your own renewals. That is a small thing, but a system you personally depend on is a system you maintain properly — and maintenance is where the last stretch of expertise actually comes from.
