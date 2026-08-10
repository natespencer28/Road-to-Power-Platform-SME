#!/usr/bin/env python3
"""
Rewrites plan.json so every week builds one spine project:
Training & Certification Compliance.

Run once:  python3 retheme.py && python3 build.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
data = json.loads((HERE / "plan.json").read_text())

# week number -> fields to replace
OVERRIDE = {
0: {
  "build": [
    "Sign up for the Power Apps Developer Plan — free, full Dataverse sandbox for all 24 weeks",
    "Create DEV, TEST and PROD environments if your tenant allows it",
    "Sign in to Microsoft Learn so module progress tracks",
    "Set up a notes repo — OneNote, Obsidian or GitHub",
    "Find out who tracks training compliance at your org today, and what they use (probably a spreadsheet)",
    "Book PL-900 for Week 5"
  ],
  "checkpoint": "Environments live, PL-900 booked, and you know whose spreadsheet you're replacing.",
  "note": "Do not start the Copilot Studio or Power Pages trials yet. They are timed — Week 17 and Week 20."
},
1: {
  "intent": "Turn 'track training compliance' into a written brief with real entities and a real definition of compliant.",
  "build": [
    "Create your DEV environment; note its type, region and Dataverse status",
    "Explore the Maker Portal, Admin Center and platform analytics",
    "Write down the credentials your org actually requires, and which roles need each one",
    "Define 'compliant' precisely — is someone expiring in 10 days compliant, or not?"
  ],
  "ai": "Have an AI assistant play requirements analyst and interrogate your definition of compliance: grace periods, provisional status, exemptions, people holding two roles. Those edge cases are the whole design.",
  "checkpoint": "One-page brief: the credentials, the roles that need them, and a precise definition of compliant."
},
2: {
  "intent": "Six tables, one join. Simple enough to learn Dataverse rather than fight your own schema.",
  "build": [
    "Model on paper first: Person, Role, Credential, Role Requirement, Completion, Training Provider",
    "Build the tables — Completion is the important one (person + credential + completed date + expiry date)",
    "Role Requirement joins Role to Credential and is where 'who needs what' lives",
    "Create the relationships; set cascade on delete so removing a Credential doesn't orphan Completions",
    "Load 8 people, 6 credentials, 3 roles and 40 completions with expiry dates spread across the next year"
  ],
  "ai": "Ask AI to critique the schema as a Dataverse model — specifically whether Role Requirement should be a table or an N:N relationship, and what you lose either way. Then have it generate 40 rows of completions with realistic date spread.",
  "checkpoint": "An ERD you drew, plus six tables with completions that expire at staggered, believable dates."
},
3: {
  "intent": "Expiry dates are the engine of this whole solution. Get the calculation layer right before anything reads from it.",
  "build": [
    "Calculated column on Completion: days until expiry",
    "Calculated column: status — Current, Expiring Soon, Lapsed — driven by that date",
    "Rollup on Person: count of lapsed credentials (and meet the 12-hour recalculation lag the easy way)",
    "Business rules: require Evidence when status is set to Completed; hide renewal fields on new records",
    "Views: Expiring in 30 Days, Lapsed, Compliant, and My Team's Gaps",
    "Alternate key on Completion (person + credential + completed date) for safe imports"
  ],
  "ai": "Ask whether 'days until expiry' should be a calculated column, a rollup, or a flow that stamps a value nightly — and what breaks with each at 10,000 rows. Verify against docs; this is exactly where AI overreaches.",
  "checkpoint": "A 300-word explainer on why you put expiry logic where you put it. The rollup lag should feature."
},
4: {
  "intent": "Three roles with genuinely different reach. This is the design Week 18's portal will depend on.",
  "build": [
    "Create three roles: Staff, Manager, Compliance Officer",
    "Staff read their own Completions only — privilege depth User",
    "Manager reads their reports' Completions — depth Business Unit or Parent-Child",
    "Compliance Officer reads and writes everything — depth Organization",
    "Column-level security on any sensitive field (medical clearance, disciplinary notes)",
    "Create a second user account, log in as them, and confirm Staff genuinely cannot see a colleague's record"
  ],
  "ai": "Have AI quiz you on PL-900 objectives — 25 scenario questions cold, then explanations for every miss, then five harder ones on your weakest domain.",
  "checkpoint": "Security matrix (role × table × privilege), verified by logging in as a Staff user and failing to see someone else's training."
},
5: {},
6: {
  "intent": "The compliance officer's back office. Model-driven first, so you work with the data model rather than around it.",
  "build": [
    "Model-driven app for the compliance officer",
    "Person main form with tabs: Details, Required Credentials, Completions, Gaps",
    "Sub-grid on Person showing every Completion with expiry and status",
    "Quick create for logging a completion in a hurry",
    "Sitemap: People, Completions, Credentials, Roles, Providers",
    "Chart: completions by status, and a view of everything lapsing in 60 days"
  ],
  "ai": "Ask AI to review the Person form for a compliance officer doing 30 record reviews an hour — field grouping, tab order, what should be visible without scrolling.",
  "checkpoint": "A compliance officer could open any person and answer 'are they current?' in under five seconds."
},
7: {
  "intent": "A completion has a lifecycle: it gets scheduled, attended, evidenced, verified. Model it properly.",
  "build": [
    "BPF on Completion: Required → Scheduled → Attended → Evidence Submitted → Verified",
    "Stage-gate it — cannot reach Verified without an evidence attachment and a verifier",
    "Business rules that show the provider and cost fields only from Scheduled onward",
    "Embed a canvas app on the Person form showing a compliance summary",
    "Editable grid on the Completions sub-grid for fast bulk date entry"
  ],
  "ai": "Ask AI to explain the table a BPF generates in Dataverse and why it matters when you later report on how long verification takes. Verify against docs.",
  "checkpoint": "Working BPF where a completion cannot be marked Verified without evidence attached."
},
8: {
  "intent": "The staff-facing app: what am I required to hold, what's expiring, what do I do about it.",
  "build": [
    "Canvas app 'My Training' filtered to the signed-in user",
    "Gallery of my credentials sorted by expiry, colour-coded by status — delegable filters only",
    "A required-but-missing list, computed from my Role's Role Requirements",
    "Form to request a renewal, using Patch with validation and error handling",
    "Screens: My Training, Details, Request Renewal, Team View (managers only)"
  ],
  "ai": "Feed your filter formulas to AI for delegation review — date comparisons against Dataverse are where delegation quietly breaks. Verify every suggestion; models invent Power Fx functions that don't exist.",
  "checkpoint": "Zero delegation warnings, tested against 2,000+ completion rows."
},
9: {
  "intent": "The mobile case is real here: people finish external training and hold a paper certificate.",
  "build": [
    "Rebuild responsive with containers — managers will open this on a phone",
    "Camera: photograph a paper certificate and attach it as evidence to a Completion",
    "Barcode or QR scanner: scan a badge ID to check someone in at a training session",
    "Two reusable components — a status pill and an expiry countdown chip",
    "Optimise: concurrent loading, minimal OnStart, App.StartScreen so managers land on Team View"
  ],
  "ai": "Have AI generate a Power Fx theme object — status colours for Current, Expiring, Lapsed — and apply it globally so the app and the components agree.",
  "checkpoint": "Loads in under 3 seconds, and you have photographed a certificate onto a record from your actual phone."
},
10: {
  "intent": "Connection references matter now because Week 24's ALM work depends on them.",
  "build": [
    "Office 365 Users connector to resolve a person's manager for escalation",
    "Pull the signed-in user's profile so 'My Training' needs no manual identity mapping",
    "Build one custom connector against a public REST API to learn the mechanics",
    "Understand connection references properly",
    "Write down your answer to: should Person be a Dataverse table, or the built-in Contact table?"
  ],
  "ai": "Give AI an OpenAPI spec, have it explain each operation and draft the connector definition. Import and test it.",
  "checkpoint": "The app resolves the signed-in user and their manager without a hardcoded lookup table."
},
11: {
  "intent": "No new material. This is the week a study project becomes a work project.",
  "build": [
    "Put 'My Training' in front of two or three colleagues and a manager",
    "Watch them use it without helping — do not explain, do not defend",
    "Ask one question only: 'is this list right?' Wrong data destroys trust faster than bad UI",
    "Fix the top five problems they hit",
    "Write a short user guide"
  ],
  "ai": "Feed your observation notes to AI and ask it to sort issues into UX, data model and training problems. The sorting is the point — each needs a different fix.",
  "checkpoint": "Three real people have used it. Bug list written, top five fixed."
},
12: {
  "intent": "Date arithmetic is the core skill of this project and this week is where you learn it properly.",
  "build": [
    "Scheduled flow: nightly scan of Completions for anything crossing 90, 60 or 30 days out",
    "Automated flow on Completion create/update using filtering attributes so it fires only when expiry changes",
    "Trigger condition preventing the flow re-triggering itself when it stamps a reminder-sent field",
    "Instant flow from the canvas app to submit a renewal request",
    "Master: formatDateTime, addDays, startOfDay, if, coalesce, first, length",
    "Weekly digest flow listing everyone expiring in the next 30 days"
  ],
  "ai": "Describe each date calculation in plain English and get the expression. Strong AI use case — but test every one against a record you know the answer for, especially timezone handling.",
  "checkpoint": "Reminders fire at 90, 60 and 30 days with no duplicates and no self-triggering loop."
},
13: {
  "intent": "Evidence verification is an approval. Overdue credentials are an escalation. Both must fail loudly.",
  "build": [
    "Approval flow: staff submits evidence, compliance officer approves or rejects with a reason",
    "Rejection writes the reason back to the record and notifies the person",
    "Escalation: lapsed for 7 days notifies the manager; 14 days notifies the manager's manager",
    "Try / Catch / Finally using Scopes with configured run-after",
    "Adaptive card approval posted to Teams so nobody has to open an app",
    "Terminate with a meaningful message when a person has no manager set"
  ],
  "ai": "Ask AI to design a resilience strategy for the nightly expiry scan: what retries, what fails loudly, what degrades gracefully. A silent failure here means nobody gets warned — the worst outcome in the whole solution.",
  "checkpoint": "Break the nightly scan deliberately and confirm a human finds out it broke."
},
14: {
  "intent": "Legacy systems are the norm in compliance. Your predecessor's spreadsheet is the point.",
  "build": [
    "Child flow that formats and sends a notification, called from the reminder, escalation and approval flows",
    "Direct Dataverse Web API calls via HTTP with Azure AD auth",
    "Desktop flow that opens the existing training spreadsheet or LMS export and loads completions into Dataverse",
    "Apply to each with concurrency tuning on the nightly scan — and know when concurrency breaks your logic"
  ],
  "ai": "Ask AI to review your flow architecture for coupling: if you rename the expiry column, which flows break? Refactor the worst offender.",
  "checkpoint": "One child flow serving three parents, and a desktop flow that imports the old spreadsheet."
},
15: {
  "intent": "You now have expiry logic in three or four different layers. Decide where it actually belongs.",
  "build": [
    "Document a decision tree: status calculation, reminder timing, compliance percentage, escalation — which layer and why",
    "Refactor two pieces you put in the wrong place back in Phase 1",
    "Settle the big one in writing: is status a calculated column read live, or a value a nightly flow stamps?"
  ],
  "ai": "Present the status-calculation question and ask for recommendations with tradeoffs — latency, reporting, licensing, what happens at 100,000 rows. Argue back where you disagree. The disagreement is the exercise.",
  "checkpoint": "A written business logic decision matrix for this solution. Genuinely SME-level output."
},
16: {},
17: {
  "intent": "Staff need to see and act on their own record without a Power Apps licence. That's what Pages is for.",
  "build": [
    "Provision a site from a template",
    "Design Studio: pages, sections, navigation, styling, theming",
    "A My Credentials page listing the signed-in person's completions with expiry dates",
    "A form to upload a certificate as evidence",
    "Publish, then view it signed out and confirm nothing leaks"
  ],
  "ai": "Ask AI to draft the information architecture: what someone sees on landing, how they learn they're lapsed, and how few clicks it takes to fix it.",
  "checkpoint": "A published site showing a real person their real credentials."
},
18: {
  "intent": "This is the week that matters, and this project is the ideal case for it: everyone sees their own record and nobody else's.",
  "build": [
    "Configure authentication plus at least one external identity provider",
    "Table permission with Self scope so a person reads only their own Completions",
    "Table permission with Contact or Account scope so a manager reads their team's",
    "Web roles: Staff, Manager, Compliance Officer — mirroring your Week 4 Dataverse roles",
    "Multistep form for evidence submission with save-and-resume",
    "Sign in as one person, take another person's record GUID, put it in the URL, and confirm you get nothing"
  ],
  "ai": "Describe your table permission config and ask AI to find data exposure risks — then verify each manually. Don't outsource the conclusion; a confident wrong answer here exposes staff records.",
  "checkpoint": "A written security test log: 8+ access scenarios, expected result, actual result. The URL-tampering test must fail closed."
},
19: {
  "intent": "Turn the portal from a content site into something people actually transact on.",
  "build": [
    "Liquid rendering the signed-in person's completions — fetchxml, entitylist, entityview",
    "A team compliance summary page for managers, rendered with Liquid",
    "Portal Web API for client-side evidence upload without a full page reload",
    "Custom JavaScript validating that a completion date isn't in the future",
    "Portal submission triggers your Week 13 approval flow",
    "Custom CSS matched to your organisation's brand"
  ],
  "ai": "Have AI generate the Liquid, then explain the security implications of every tag used. Liquid will happily render records the user shouldn't see if your permissions are loose.",
  "checkpoint": "A person uploads a certificate on the portal, it writes to Dataverse, the approval fires, the compliance officer is notified."
},
20: {
  "intent": "The questions people ask about compliance are repetitive and predictable. That is exactly what an agent is for.",
  "build": [
    "Agent with topics for: am I current, what am I missing, when does X expire, how do I renew",
    "Knowledge sources: your training policy document, the provider list, a renewal FAQ",
    "Action calling a flow that looks up the asker's own completions",
    "Action that files a renewal request on their behalf",
    "Generative answers scoped so it refuses to discuss anyone else's records",
    "Publish to Teams and test with a real colleague"
  ],
  "ai": "Iterate the agent's instructions with AI: draft, test against ten real questions, feed the failures back, revise. Pay attention to it answering about other people — that's the failure that matters.",
  "checkpoint": "A published agent that tells you your own status and refuses to tell you someone else's."
},
21: {},
22: {
  "intent": "AB-620 territory and the genuine frontier of the platform.",
  "build": [
    "Connect your agent to an MCP server as a tool source",
    "Build a second specialist agent — a Training Finder that searches provider catalogues — and hand off to it",
    "Custom connectors and API actions as agent tools",
    "Adaptive cards rendering a person's credential list with expiry chips",
    "A custom prompt from the Microsoft Foundry model catalog",
    "Explore computer use for a UI-driven task, such as booking on a provider's website"
  ],
  "ai": "Use AI to design the decomposition — the compliance agent knows records, the finder agent knows courses, and neither should do the other's job. Reasoning about boundaries out loud is how you get good at this.",
  "checkpoint": "Two agents, one MCP tool integration, one working handoff from compliance to training-finder."
},
23: {
  "intent": "Almost nobody does this part. That is exactly why it differentiates you.",
  "build": [
    "A test set of 30+ real questions staff would ask, with expected outcomes",
    "Run evaluations, review results, iterate on instructions and knowledge",
    "Wire up Application Insights for agent telemetry",
    "Package the agent into a solution with environment variables — no hardcoded values",
    "Deploy DEV to TEST via Power Platform Pipelines"
  ],
  "ai": "Ask AI for 40 adversarial utterances, weighted toward attempts to extract another person's training records by indirect phrasing. That is the specific risk in this solution, and it's real red-teaming.",
  "checkpoint": "Evaluation results before and after one iteration, showing measured improvement — and zero cross-user leaks."
},
24: {
  "intent": "The capstone. Package it properly, ship it through a pipeline, and write down why you built it the way you did.",
  "build": [
    "Package everything as a managed solution with proper publisher and prefix",
    "Externalise every connection reference and environment variable — reminder thresholds should not be hardcoded",
    "Full DEV to TEST to PROD deployment via pipelines",
    "Apply a DLP policy and document its impact — this solution handles staff records",
    "Install the CoE Starter Kit in a sandbox and explore what it surfaces",
    "Write an architecture decision record: the status-calculation choice, the security model, the portal permission design",
    "Sit AB-620 this week or next, depending on how Weeks 22–23 went"
  ],
  "ai": "Have AI argue the opposing side of every decision in your ADR. Where you can't defend yourself, you've found a gap.",
  "checkpoint": "Deployed to PROD through a pipeline. ADR written. Real staff checking their own compliance."
}
}

for w in data["WEEKS"]:
    patch = OVERRIDE.get(w["n"])
    if patch:
        w.update(patch)

(HERE / "plan.json").write_text(json.dumps(data, indent=2))
touched = sum(1 for k, v in OVERRIDE.items() if v)
print(f"Retheme applied — {touched} weeks rewritten for Training & Certification Compliance")
