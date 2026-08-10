# Power Platform — 24-Week Block Plan

A self-contained progress tracker for a 24-week study block covering Dataverse, Power Apps, Power Automate, Power Pages and Copilot Studio, built around the certifications that survived Microsoft's 2026 portfolio reset.

One self-contained HTML file. No framework, no backend, no build step required to deploy. The full plan is readable even with JavaScript off; JavaScript adds the checkboxes, notes and saved progress.

---

## Deploy to GitHub Pages

**1. Create the repo**

```bash
mkdir power-platform-plan && cd power-platform-plan
git init
# drop index.html in here (plus the other files if you want to edit the plan later)
git add .
git commit -m "24-week Power Platform block plan"
```

**2. Push it**

Create an empty repo on GitHub (no README, no .gitignore — you already have files), then:

```bash
git remote add origin https://github.com/YOUR-USERNAME/power-platform-plan.git
git branch -M main
git push -u origin main
```

**3. Turn on Pages**

Repo → **Settings** → **Pages** → under *Build and deployment*, set **Source** to `Deploy from a branch`, **Branch** to `main` and folder to `/ (root)`. Save.

Roughly a minute later it's live at:

```
https://YOUR-USERNAME.github.io/power-platform-plan/
```

`index.html` is served automatically as the index — no configuration needed, and no Jekyll build to worry about since there are no underscore-prefixed files.

**Private repos:** GitHub Pages on private repos requires a paid plan. If you want this private and free, use the "run it locally" option below instead.

---

## Other ways to run it

| Method | How | Notes |
|---|---|---|
| **Locally** | Double-click `index.html` | Works fully offline once fonts are cached. Progress saves per-browser. |
| **Netlify Drop** | Drag the folder onto [app.netlify.com/drop](https://app.netlify.com/drop) | No account needed, live in seconds |
| **Cloudflare Pages** | Connect the same GitHub repo | Free, private repos allowed |
| **SharePoint / internal** | Upload and serve as a static page | Check your tenant allows inline scripts |

---

## How progress works

There is no server and no account. Everything you tick is written to `localStorage` under the key `pp24.v1`, scoped to the exact origin you're viewing from.

**What that means in practice:**

- Progress does **not** follow you between devices or browsers
- Clearing site data wipes it
- `localhost` and your Pages URL are different origins, so they keep separate progress
- Private/incognito windows lose it on close

**So use Export.** The button at the bottom downloads a small JSON file. Import it on your other machine, or commit it to the repo as a backup. Getting to week 19 and losing six months of notes to a cleared cache would be a genuinely bad afternoon.

If local storage is blocked entirely (some embedded previews and locked-down browsers do this), a banner appears at the top and the app runs in memory for that session. Everything still works; nothing persists.

---

## Files

| File | What it is |
|---|---|
| `index.html` | **The app.** Self-contained — this is the only file GitHub Pages needs. |
| `plan.json` | The curriculum: 25 weeks, phases, credentials, links. |
| `PROJECT.md` | The spine project spec — data model, security roles, sample data. |
| `template.html` | Page shell, styles and script, with `<!--PLACEHOLDERS-->`. |
| `build.py` | Renders `plan.json` + `template.html` into `index.html`. |

You can deploy `index.html` alone and ignore the rest. The other three exist so editing the plan doesn't mean hand-editing 120KB of markup.

---

## It works without JavaScript

Every week, item and checkpoint is written into the HTML itself. With JS disabled or blocked, the page is a complete, readable, scrollable plan — you just don't get checkboxes.

With JS on, the script adds a `js` class to `<body>`, which collapses the stack into one week at a time and switches on the tracker: ticking, notes, progress, the strip, export/import.

That ordering matters. The script only collapses the view *after* every handler has bound successfully, so a script failure leaves you with the full readable document rather than a blank page.

---

## Making it yours

Edit `plan.json`, then rebuild:

```bash
python3 build.py
```

No dependencies — standard library only. Each week looks like:

```json
{
  "n": 8,
  "phase": 2,
  "title": "Canvas apps & Power Fx",
  "intent": "One line on why this week exists.",
  "trial": "Optional licensing note, renders as a callout",
  "note": "Optional general callout",
  "exam": "AB-410",
  "learn": ["..."],
  "watch": ["..."],
  "build": ["..."],
  "ai": "The week's AI drill — prose, not a checkbox",
  "checkpoint": "The gate. Ticking this marks the week done."
}
```

Add or remove items freely; counts and percentages recalculate. Two things to keep consistent:

- **Every week needs a `checkpoint`** — it drives week completion and the strip fill.
- **`PHASES[].weeks` must cover 0–24 exactly**, or the strip brackets misalign.

**The spine project** is Training & Certification Compliance — see `PROJECT.md` for the data model and build spec. Every week's `build` items name its real entities (Person, Credential, Completion, Role Requirement) rather than generic placeholders.

To swap it for a different domain, rewrite the `build` arrays and rebuild. `retheme.py` shows the pattern: a dict of week-number overrides applied to `plan.json`. `plan.generic.json.bak` is the original domain-neutral version if you want to start from that instead.

Prefer not to run Python? Edit `index.html` directly — the text is all there in plain markup. You'll just be editing it in two places (the visible HTML and nothing else, since the item counts derive from the DOM).

---

## Keyboard

| Key | Does |
|---|---|
| `←` `→` | Previous / next week |
| `Space` or `Enter` | Toggle the focused item |
| `Tab` | Move between items |

---

## A note on the certification data

The credential list reflects the state of Microsoft's portfolio as of **August 2026**, after a year in which PL-100, PL-500, PL-600 and the Copilot Studio applied skill were all retired and PL-200 was given an end date of 31 August 2026. The plan targets PL-900 → AB-410 → AB-620 instead.

Microsoft moves these dates. Before you book anything, check the credential pages linked in the app's reference panel — they're the authoritative source, and this file is a snapshot.
