# Sample Data — Training & Certification Compliance

Everything you need to build the spine project without touching a real personnel record.

```bash
python3 generate.py
```

Writes six CSVs. **Import them in numbered order** — later files reference earlier ones.

| File | Rows | What |
|---|---|---|
| `1-roles.csv` | 3 | Field Technician, Warehouse Operator, Site Supervisor |
| `2-credentials.csv` | 6 | Safety and equipment certs, 12/24/36-month validity |
| `3-providers.csv` | 4 | Three external, one in-house |
| `4-people.csv` | 8 | Two managers, six reports |
| `5-role-requirements.csv` | 11 | Who needs what, mandatory vs optional, grace periods |
| `6-completions.csv` | 30 | The heart of it |

All email addresses use `example.com`, which is reserved by RFC 2606 and can never belong to anyone. Nothing here can accidentally email a real person.

---

## Dates regenerate

The dates are computed **relative to the day you run the script**, not baked in. Run it in March and someone is lapsed by 47 days; run it in September and someone is *still* lapsed by 47 days.

Re-run it whenever your data drifts out of the useful range — likely around Week 12 when you start testing reminder flows, and again around Week 20.

---

## The spread, and why it's built this way

This is the part that matters more than the volume. Thirty rows with realistic *distribution* teach you more than a thousand uniform ones.

| Bucket | Count | What it exercises |
|---|---|---|
| Already lapsed | 3 | Escalation flows, the "you are non-compliant" state |
| Expiring ≤ 30 days | 3 | The 30-day reminder tier |
| Expiring 31–60 days | 2 | The 60-day tier |
| Expiring 61–90 days | 2 | The 90-day tier |
| Comfortably current | 15 | The boring majority — most of your UI |
| **Superseded duplicates** | 3 | Latest-record-wins logic |
| **Pending verification** | 2 | Mid-BPF states, missing evidence |
| **Person with zero records** | 1 | The empty state |

The last three rows are the ones I'd draw your attention to.

**Superseded duplicates** are three people who hold *two* completions for the same credential — an old expired one and a current valid one. If your app shows Priya as lapsed on First Aid because it found the 2021 record instead of the current one, you have a bug. Almost every beginner writes this bug. Better to meet it in Week 6 with three rows than in Week 20 with three hundred.

**Kwame Asare (EMP-008)** is a new starter with no completions at all. He's required to hold two mandatory credentials and holds neither. Build against him early — empty states are where apps look broken, and a gallery with nothing in it should say "no records" rather than render blank.

**Two pending records** have no evidence attached, so they sit mid-BPF. They're what your Week 13 approval flow acts on.

---

## The compliance picture on import day

Worth knowing so you can tell "my query is wrong" from "the data really says that":

| Person | Role | Status |
|---|---|---|
| Dana Whitfield | Site Supervisor | Compliant |
| Marcus Oyelaran | Site Supervisor | Compliant |
| Priya Raghavan | Field Technician | **Manual Handling lapsed** |
| Tomas Lindqvist | Field Technician | **Working at Height lapsed** |
| Aisha Bello | Field Technician | Compliant |
| Grant Mullins | Warehouse Operator | **Forklift lapsed** |
| Sofia Marchetti | Warehouse Operator | Compliant |
| Kwame Asare | Warehouse Operator | **Two credentials missing** |

Four of eight non-compliant. Higher than a healthy real organisation, deliberately — you need enough failure states to build against.

Reporting structure: Dana manages Priya, Tomas and Aisha. Marcus manages Grant, Sofia and Kwame. That's what makes Week 18's manager scope testable — Dana must see her three and never Marcus's.

---

## Building without a real compliance officer

You lose one genuine thing by using fake data: Week 11's real-user feedback. That's worth replacing rather than skipping, because watching someone else use your app is where the useful surprises live.

Three substitutes, roughly in order of value:

**1. Use it on yourself.** Load your own certification dates — PL-900 in Week 5, AB-410 in Week 21, AB-620 in Week 24 — alongside the fake staff. Most Microsoft associate certs now renew annually through free Learn assessments, and that window is easy to miss. By Week 13 the solution emails *you* about *your* renewals. A system you personally depend on is one you maintain properly, and maintenance is where the last stretch of expertise comes from.

**2. Find the adjacent real problem.** You may not have a compliance officer, but someone in your org tracks *something* that expires — equipment calibration, software licences, insurance certificates, contract renewals, safety inspections. Identical shape: a thing, a date, a person responsible, a warning window. Show them your app in Week 11 and ask whether it would work for their problem. Their answer is real feedback on a real need.

**3. Recruit any two colleagues.** They don't need to know the domain. Week 11's instruction is to watch them use it *without helping*, and most of what you learn is navigational — they can't find the button, they don't know what "lapsed" means, they expect the list sorted differently. None of that requires domain expertise to surface.

Do at least one. The plan works without it, but Week 11 is the point where a study project becomes something you've actually shipped, and that transition is worth protecting.

---

## When to move to real data

Not before **Week 24**, when the DLP review and governance layer exist.

Training records are personnel data. In a sandbox you're actively learning on — where you're deliberately misconfiguring table permissions in Week 18 to see what breaks — real staff records don't belong. Build the whole thing on invented people, get the security model right, review it under DLP, deploy through a pipeline, *then* decide whether real data goes in.

That ordering isn't caution for its own sake. It means that when you do show this to someone with authority over real records, you can walk them through a working security model instead of asking them to trust you.
