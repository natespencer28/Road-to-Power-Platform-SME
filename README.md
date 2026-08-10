# Power Platform — 24-Week Block Plan

A self-contained progress tracker for a 24-week study block covering Dataverse, Power Apps, Power Automate, Power Pages and Copilot Studio, built around the certifications that survived Microsoft's 2026 portfolio reset.

One HTML file. No build step, no framework, no backend. Progress lives in your browser's local storage.

---

## Deploy to GitHub Pages

**1. Create the repo**

```bash
mkdir power-platform-plan && cd power-platform-plan
git init
# drop index.html and README.md in here
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

## Making it yours

All 25 weeks live in a single `WEEKS` array near the top of the `<script>` block. Each entry:

```js
{
  n: 8,                          // week number, 0–24
  phase: 2,                      // index into PHASES
  title: "Canvas apps & Power Fx",
  intent: "One line on why this week exists.",
  trial: "Optional — licensing note, renders as a callout",
  note:  "Optional — general callout",
  exam:  "AB-410",               // optional — inverts the strip cell
  learn: ["..."],                // checkbox list
  watch: ["..."],                // checkbox list
  build: ["..."],                // checkbox list
  ai:    "The week's AI drill — prose, not a checkbox",
  checkpoint: "The gate. Ticking this marks the week done."
}
```

Add or remove items freely — counts and percentages recalculate themselves. The one thing to keep consistent: every week needs a `checkpoint`, because that's what drives week completion and the strip fill.

**Swapping the spine project** is the most likely edit. The plan assumes a service request and asset tracker; if your work is inspections, onboarding, grant applications or client intake, search the `build` arrays for the request/asset language and substitute your domain. The architecture is identical.

Changing phase structure means editing `PHASES` too — the `weeks` arrays there must still cover 0–24 exactly, or the strip brackets will misalign.

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
