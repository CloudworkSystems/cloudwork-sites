# Site Engine Lessons

What we learn while building the Cloudwork Systems and True Convo websites by
hand, written down so the True Convo planning project can use it when it
designs the Site Engine module.

This file lives in the website repo on purpose. Nothing here is written into
`CloudworkSystems/open-convo`. The planning project reads this file (it can
read this repo) and decides what, if anything, goes into its own plans.

Where a lesson answers one of the open questions in open-convo's Site Engine
design note (`docs/design-notes/site-engine.md`, "Open Questions"), it says
which one, as **Q1** to **Q5**:

- Q1 Kinds of sites
- Q2 How the design is chosen
- Q3 How people edit
- Q4 How the public-facts sheet is filled
- Q5 Forms and booking

Started November 2, 2026 from the work in the thread "Evaluate Scrollcraft
skill for the sites" (November 1 to 2). The draft pages it describes are in
`trueconvo-day/` on the branch `claude/project-thread-8ve9p4`. None of it is
published.

## How to Keep This File Current

One habit, for every building session in this repo:

1. **When a preview goes to Patrick, add what was learned** to "The Log" at the
   bottom: the date, one line on what was tried, and one line on what it taught.
   One or two lines per round is enough.
2. **When Patrick reacts** (yes, no, "try again", a new idea), add his reaction
   in his own words if it changes direction, and what it means for Site Engine.
3. **If a log entry changes a standing lesson**, update the matching section
   above the log too, so the top of the file stays the current answer.
4. **Every pull request in this repo** ticks the lessons box in the pull
   request template: either "updated the lessons file" or "nothing new".

Write it the way this repo is written: plain language, invented people only,
no private details, no prices or claims that are not checked.

## The Biggest Lessons So Far

1. **Story first, pages second.** A visitor should understand in under a minute
   what a day with the product is like for one person. A list of features
   doesn't do that; a day in someone's life does. Site Engine should start by
   asking for the story (who is it for, what does their day look like), not for
   a page layout. (Q2, Q4)
2. **Show what you are building, then be honest once.** Patrick rejected a first
   take that labelled every step "In testing". What worked: show the finished
   product as intended, then one honest strip at the end ("Where this stands")
   that matches what is really built. For Site Engine: let the person describe
   their vision freely, but keep a separate, checked "what's real today" block
   that the privacy and honesty checks own. (Q1, Q4)
3. **Choose your own adventure.** Patrick's long-held picture of the site is a
   picker at the top: pick the person most like you, and the whole page swaps
   to their day. Five invented people share one design and one "spine". For
   Site Engine this suggests a site kind beyond one page: **one shell, many
   audience pages**, generated from one facts sheet plus one short story per
   audience. (Q1)
4. **A tool's name is not its feel.** The first take used the scroll-craft
   engine and still didn't feel like scroll-craft, and Patrick noticed at once.
   The feel came from its specific devices (layered planes moving at different
   speeds, pointer tilt, a spotlight, words building up, the page colour
   drifting through the day). Site Engine's design step should name the
   devices it uses, not just the library. (Q2)
5. **Drawn screens beat stock footage, for a product site.** With no video,
   everything was drawn in the page itself: free, nothing loaded from other
   sites, and closer to the real product than AI footage would be. Video
   earns its place only for atmosphere. (Q2)
6. **Preview at phone and desktop, every round.** Each round was screenshotted
   at both widths, in scroll order, before Patrick saw it. That caught real
   problems (a faint sunrise, a crowded title on phones). Site Engine's preview
   should always show both widths. (Q3)

## Tools Tried

| Tool | What it is | Cost | Verdict |
|---|---|---|---|
| scroll-craft (Nate Herk, github.com/nateherkai/scroll-craft, MIT) | Instructions for the AI plus a small scroll engine (two files, about 80 KB) and a screenshot checker | Free, except its media generator | **Use.** Engine copied unchanged into the site, loads nothing from other sites, ships no fonts. Its "taste" guide (type sizes, spacing, contrast) was followed. |
| scroll-craft's media generator (`kie.ai`) | Paid image and video generation, about 28 credits a still and 160 a 5-second clip (per the repo's example settings) | Paid, needs a card | **Skip.** Against the $0 rule. |
| Impeccable (Paul Bakaus, github.com/pbakaus/impeccable, Apache 2.0) | A design critique and polish pass | Free | **Not tried yet.** It stacks on top of scroll-craft, it doesn't replace it. |
| Higgsfield, fal.ai, Replicate | Higgsfield is a consumer subscription app bundling video models; fal.ai and Replicate are pay-per-clip services behind one key | Paid | **Skip** for now. |
| Local video models (Wan, LTX-Video, Hunyuan through ComfyUI) | Open video models running on the owner's own Mac | Free, but slow and needs a Mac with lots of memory | **Possible later**, for atmosphere only. Not tried. |

What this means for Site Engine: open-convo already plans scroll-craft and
Impeccable as True Convo capabilities. The working split is **scroll-craft
for motion and structure, Impeccable for critique, and media from the
person's own photos, drawings or a local model**, never a paid generator
without the person's yes.

## How Scroll-craft Behaves (Build Notes)

- The feel comes from: `data-sc-parallax` planes at different rates, pointer
  tilt and spotlight, kinetic text, and colour drift through the page. With no
  video, these carry the whole effect.
- The parallax offset is `rate × (progress − 0.5) × 100px`. A negative rate
  starts low and rises.
- Never set `position` on a `[data-sc-stage]` element: it breaks the sticky
  pin. (This bit us once.)
- A sideways rail (a pinned scene that pans) works well for "lots of things at
  once", such as a noon rail of every module.
- One signature move per page is enough. Here: the sun rising and setting as
  the visitor scrolls.
- Long pages get long fast. Take 3 was about 30 screens of scroll; that's
  worth checking on a phone before adding more.

## The Rules That Shaped Every Page

These are this project's rules. They map closely onto what Site Engine must
enforce for every user.

- **Honesty.** No claim that a feature works unless open-convo's `STATUS.md`
  says it's built and switched on. No invented testimonials, user counts,
  logos or reviews. People in examples are invented and say so. For Site
  Engine: a checked "honesty gate" beside the privacy gate, so the person's
  own site can't overclaim either.
- **Privacy and scripts.** No trackers, analytics, chat widgets, or anything
  loaded from another site. Fonts are copied into the site and served from it
  (Atkinson Hyperlegible Next, with its licence beside it). Each preview was
  tested for outside requests. For Site Engine: "nothing loaded from elsewhere"
  is easy to check automatically, so check it on every build.
- **$0.** Free tools only, free hosting the owner already has (GitHub,
  Cloudflare), nothing that needs a card.
- **Approvals.** Nothing goes live, changes DNS, adds a domain or creates an
  account without the owner's own yes. A preview at phone and desktop widths
  comes first. This matches Site Engine's "nothing goes public without
  approval".
- **Search engines kept out of drafts.** Draft pages carry
  `<meta name="robots" content="noindex">`.

## Generating Many Pages From One Shell

- Sam's page is written by hand and is the reference. The other four are
  generated by a small script (`trueconvo-day/tools/build-days.py`) from one
  shared shell plus each person's acts, with shared styles in one file
  (`day.css`). Edit the script, never the generated pages; each generated page
  says so at the top.
- This is the same shape Site Engine already uses (facts in, plain files out),
  extended to **several audiences per site**. A future Site Engine "story"
  field could hold each audience's acts, with the shell owned by the engine.
  (Q1, Q4)

## How Patrick Works With This (What Helped)

- He reacts to something he can see far better than to a description. A rough
  first scene within minutes was worth more than a plan.
- He thinks out loud in long voice notes and adds ideas as he goes (a new
  person arrived mid-build twice). The building session took each one,
  confirmed it in a line, and kept going.
- A choice with three clear options and a recommendation got an answer in
  minutes. For Site Engine: ask design questions as a few picks, not open
  questions. (Q2, Q3)
- He asked "is there anything wrong with...?" before adding personas; a
  straight answer plus one caution worked.

## Costs Avoided

- kie.ai media for a six-scene page: about 520 credits; a long "flythrough"
  page: about 2,000 (from the repo's example settings, not a quote).
- Any video subscription (Higgsfield or similar).
- Any font service, analytics or hosting fee.

## The Log

Newest last. One or two lines per round.

- **2026-11-01, scroll-craft check.** Found and read the repo itself (MIT,
  checked at commit `75d81f7`). Engine is local and clean; only the kie.ai
  generator costs money. Lesson: read the tool's own repo, not reviews of it.
- **2026-11-01, take 1 (morning only).** Built on the engine, every feature
  labelled "In testing". Lesson: correct but flat; the labels and the
  built-today framing undersold the product.
- **2026-11-02, Patrick: "try again ... not what we can give the person right
  now, what we're trying to make."** Lesson: describe the vision; keep the
  honesty in one place.
- **2026-11-02, Patrick: "I feel like you didn't use the scroll craft at
  all."** Lesson: the devices make the feel, not the library.
- **2026-11-02, take 2 (whole day, layered hero, real scroll-craft devices).**
  Patrick: "I don't hate this take." Lesson: layered planes, tilt and drift
  carry the effect without video.
- **2026-11-02, take 3 (every intended module, the home network, build your
  own, no frontier model needed).** Lesson: the vision includes
  extensibility (build software for your own home and stop there, or package
  it and sell it) and local AI as the floor. Pages get long; check on a phone.
- **2026-11-02, take 4 (five people, pick at the top).** Patrick: picking
  your own adventure is "always been the thing I've had in mind". Lesson: one
  shell, many audiences, generated from one script.
- **2026-11-02, video question.** Higgsfield, kie.ai, fal.ai and Replicate are
  all paid; the free route is a local model on the Mac. Lesson: for a product
  site, drawn screens are usually better than AI footage.
