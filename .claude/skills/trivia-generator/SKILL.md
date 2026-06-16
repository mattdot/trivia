---
name: trivia-generator
description: "Generate hard, reasoning-driven trivia questions whose answers come from a   listable set of subjects, are checkable against cited sources, and read at a   6th-grade level even when the difficulty is adult-level. Use this skill   whenever the user wants trivia, quiz questions, a question set, a quiz round,   pub-quiz or quiz-bowl style questions, \"stump me\" questions, or hard   questions about a topic — even if they don't say the word \"trivia.\" Also use   it when the user gives just a topic, a word, a phrase, or a list and the   intent is clearly to get questions about it. Default to 30 questions unless   the user asks for a different number. Also use this skill to render a trivia   set — newly generated or already produced earlier in the conversation — as an   interactive, phone-friendly HTML \"field guide\" with tap-to-reveal answers   whenever the user asks to render, display, lay out, or make an   openable / tappable / hide-the-answer / quiz-style version of trivia   questions."
---

# Trivia Generator

## The one idea everything follows from

**All difficulty must come from reasoning. None may come from obscurity of fact or obscurity of language.**

A convoluted sentence and a memorize-or-die fact are the same defect: fake difficulty that doesn't reward thinking. The target is a question a sharp person can *reason toward without already knowing the answer* — narrowing a set of candidates they could in principle list down to a short list, then placing a defensible bet. The plain wording, the listable answer set, and the citation requirement are three sides of this one principle — keep all three or the mechanic breaks.

**Reasoning should earn an edge, not a certainty.** A well-built question lets a sharp player rule out most candidates and bet intelligently on what's left — but it does not hand them the answer by pure deduction. That residual doubt is the game: they'll often be right and sometimes get burned, which is exactly what makes it worth playing. A question that *forces* its answer for anyone who reasons carefully is a logic puzzle, not trivia; a question that can't be reasoned toward at all is just recall. Aim for the middle.

"Ranking-driven" is the *means*, not the goal. A question is good when someone can reason their way to a strong guess, not merely when it contains a superlative.

## The mechanic: guess-with-reasoning

A question works when three things are true:

1. **The answer comes from a set the solver could list.** Countries, chemical elements, planets, US states, the Ivies, Summer Olympics host cities, the G7, the eight planets, world capitals — sets you can walk mentally. This is what makes reasoning possible: the solver can hold the candidates in mind and test them.
2. **Each condition in the question is a test the solver can apply** to prune that set — knocking out the candidates that plainly fail.
3. **The conditions narrow the field to a few real contenders, not to one.** The sweet spot is roughly **2–4 finalists** a reasoner can't fully separate without the specific fact. They can usually rank those finalists by plausibility and make a defensible pick — but the true answer is sometimes the second- or third-most-likely, which is why a sharp player beats chance handily yet still misses some. If the conditions collapse the field to a single forced answer every time, the question is a deduction exercise; loosen a condition, or choose a dimension where the contenders are genuinely close. If they leave a dozen equally-plausible candidates, the filters aren't pulling their weight; tighten them.

**Well-posed and guessable are different requirements, and you need both.** *Well-posed* means the question has exactly one correct answer in reality — one true record-holder, verified against data. *Guessable* means a reasoner can get down to a short list and bet. The residual doubt lives entirely on the solver's side: they're unsure which finalist it is, but the fact itself is settled. Never confuse "the solver can't be certain which finalist it is" (good — that's the game) with "two answers are equally correct" (broken — that's ambiguity; see the gate).

Answer spaces fall into three tiers. Steer toward the top:

- **Enumerable (ideal):** the solver can mentally walk the whole list.
- **Bounded but large (workable only if the conditions prune hard):** Fortune 500, capital cities, sitting heads of state. Use only when the filters cut the field to a few.
- **Effectively unbounded (red flag):** "which CEO," "which scientist," "which song," "which battle," "which painting." There is no list to reason over, so the only path to the answer is to have memorized it. Rework or drop these.

When you catch yourself writing a question whose answer is a single un-listable thing, that is the signal the question is memorization, not reasoning. Fix it by changing the answer set (e.g., not "which scientist won X" but "which *country* has produced the most X winners") or drop it.

## Workflow

Run these phases in order. Phases 1–3 are the spine; do not skip them.

### Phase 1 — Topic fit

The style needs measurable comparisons and answers from a listable set. Before anything else, judge the topic:

- **Fits** (sports, geography, countries, companies, elements, space, demographics, awards, infrastructure, transit, animals by measurable trait): proceed.
- **Marginal** (a single broad field that's mostly qualitative but has some measurable edges): proceed, but deliberately widen the dimensions you pull from so you're not forcing it.
- **Doesn't fit** (a single poem, an abstract idea, a purely qualitative subject with no rankable structure): don't force it. Say briefly why it doesn't fit, suggest the closest topic that *does* (e.g., "a single novel" → "that author's full body of work," or "best-selling novels of its decade"), and ask whether to proceed with the alternative. Suggest-and-confirm; don't silently switch topics.

### Phase 2 — Build a planning grid (write it down)

A private plan doesn't steer generation; a written one does. Before any web search, lay out the intended set as a table — one row per question — with these columns:

| # | Subtopic / dimension | Ranking archetype | Candidate answer set | Expected answer shape | Condition / filter |
|---|---|---|---|---|---|

Fill **every row before searching.** Requirements for the grid:

- **Dimension uniqueness — at least 75% unique per set (the headline variety rule).** A *dimension* is the measurable axis a question is built on (elevation, founding date, population, coastline, prize count), distinct from the *archetype*, which is the ranking shape (largest, fewest, oldest, narrowest-margin). At least three-quarters of the questions in any set must sit on a dimension that **no other question in the set uses**. Operationally: count the questions that share their dimension with at least one other question — that shared group must be **≤25% of the set**. A dimension may appear **at most twice, never three times**, and few enough dimensions may be doubled that the unique share stays ≥75%. Per common set sizes:
  - 30 questions → **≥23** on a once-only dimension (so **≤3** dimensions doubled).
  - 20 → ≥15 unique (≤2 doubled). · 10 → ≥8 unique (≤1 doubled). · 7 or fewer → **every** question on its own dimension.
  - This is stricter than just hitting a dimension count: two questions that both rank "size" (total area and land area) or both rank "borders" (neighbor count and international border) count as the **same** dimension. When two rows feel like the same axis viewed twice, they are — split one onto a genuinely different axis.
- Use **8–10 ranking archetypes**, and **no archetype more than 3 times** (archetypes may repeat more than dimensions, since the same shape — "fewest" — over different axes still reads as variety).
- **No answer set or dimension repeated in adjacent rows** (so similar facts never land next to each other).
- For a broad topic, spread across many measurable dimensions. Example for *universities*: endowment, research spending, founding age, enrollment, prizes, scholarships, campus area, libraries/museums, athletics, public systems, internationalization, global rank, patents, alumni in office. Build the analogous spread for whatever the topic is — and if the topic can't sustain ≥75% unique dimensions at the requested count, **say so and offer to broaden the framing or generate fewer questions** rather than padding the set with near-duplicate axes (suggest-and-confirm, per Phase 1).

Then **emit a compact Plan block** above the questions: list the dimensions and archetypes covered, and state the unique-dimension ratio explicitly (e.g. "26 dimensions across 30 questions — 87% unique; doubled: population, coastline"). Writing that ratio is what forces the spread to actually happen, and it's the audit trail when a set feels repetitive.

If, while searching, results pull several rows toward one source, era, geography, or statistic type, **change those rows to underused cells before continuing.** Do not let the first dataset or leaderboard you find drive the set.

### Phase 3 — Per-question gate

Run this gate on **every** question before finalizing it. It does triple duty: it's what makes the question guessable, what verifies the answer, and what catches ambiguity. These are internal checks — don't print them (except coverage caveats, which go in the Follow-on).

1. **Candidate set.** Name the listable set the answer is drawn from. If that set is effectively unlimited, rework the question so the answer comes from a listable set, or drop it.
2. **Conditions as tests.** Restate each condition in the stem as a test a solver could apply to a candidate.
3. **One correct answer (well-posedness).** Confirm the question has **exactly one correct answer in reality**: the superlative, record, or filter resolves to a single true holder, verified in step 4. This is about the world, not the solver. If two subjects are *equally* correct under the stem — a genuine tie, or a fair definition that could pick either — the question is **ambiguous**; tighten the stem, name the metric, or flag the definition. Ambiguity is a defect; solver uncertainty is not (see step 5). Note the distinction from the old "narrow to one" rule: the *answer* is one thing, but the solver's reasoning is allowed — expected — to leave several plausible finalists.
4. **Verify.** Confirm the surviving answer against your source(s). For **computed** answers (anything you derived by filtering/joining/ranking data), confirm the dataset covers the *entire* candidate set — a "smallest/fewest/lowest" result is only real if nothing missing could rank below it. State any coverage limit in the Follow-on.
5. **Reasoning check (guessable, not forced).** Confirm a knowledgeable solver could, by reasoning over the listable set and applying the conditions, prune it to a **short list of plausible finalists (≈2–4)** and form a defensible bet — *without already knowing the answer.* Two failure modes to catch: if the only way to beat blind guessing is to have memorized the specific fact, the question is recall — rework or drop it; if correct reasoning *forces* the single answer with no real doubt, it's a deduction puzzle — acceptable occasionally, but vary how much doubt remains across the set so the typical question still leaves a genuine bet.

This gate will discard some hard-but-arbitrary questions (the "third-most populous city in one province in 1970" type). That's intended: you're trading a slice of raw difficulty range for a consistent, fair, *bettable* solving experience.

### Phase 4 — Variety, counterbalance, sourcing, wording

Apply the standards below as you write, then run the final checklist.

## Standards

### Difficulty comes from filters and inversions, not obscurity

The two best difficulty levers, both of which preserve guessability:

- **Condition-qualified records.** "Largest country by area" is a gimme; adding a filter — "largest country completely surrounded by just one other" — makes it hard yet still reasonable: the solver pictures the map and tests candidates. Two cautions, both learned from play:
  - **The filter must be one a player would naturally reason with, not a carve-out to dodge a technicality.** "Highest GDP per person *among countries big enough to rank*" is gerrymandered — the qualifier exists only to fence out Monaco, and the seam shows. If the clean answer is a technicality you have to exclude, the dimension is wrong; pick another rather than building an arbitrary fence.
  - **Condition-qualified is necessary but not sufficient — the result still has to be fresh** (see "Freshness" below). "Largest landlocked country," "longest coastline," "smallest country" are all condition-qualified *and* tired warhorses; a player who quizzes has met them and answers from memory.
  Prefer conditions a reasoner can *navigate* (era, region, "without X," "that never did Y," minimum threshold, population/budget class, institution type) over conditions that are merely narrow. Several questions in a strong set should have answers that are not overall leaders but leaders *under a filter.* State the condition plainly in the stem; explain the threshold or caveat in the answer fields.
- **Bottom-end inversions.** Trivia culture over-indexes on biggest/most, so fewest/smallest/lowest/narrowest are inherently fresher, and they defeat the solver's reflex to reach for the famous large thing. Deliberately seed: fewest wins by a champion, lowest winning score, smallest country/city/company to achieve X, shortest reign or streak, narrowest margin, lowest rate among leaders, least populous place with a record, smallest budget to reach a milestone. **Do not let the set point only upward.**

### Freshness: skip the warhorses

A question can be reasoning-driven, well-posed, *and* listable and still be weak because everyone has already met it. Pub-quiz culture has a stock of chestnuts — largest landlocked country (Kazakhstan), longest coastline (Canada), the city spanning two continents (Istanbul), smallest country (Vatican), highest capital (La Paz). When a player has likely seen the exact question before, the reasoning mechanic is dead on arrival: they answer from memory of the *question*, not by reasoning over the set. That also covers the "you either know it or you don't" failure — a famous one-fact identity question is recall wearing a filter's clothes.

Before keeping a question, ask: **would this feel familiar to someone who does quizzes?** If yes, keep the dimension but change the angle — invert to the bottom end, add a tighter filter, or find a less-obvious record on the same axis — or drop it. **A common move that rescues a chestnut is to re-slice it to a region, hemisphere, or era, so the answer is no longer the memorized global one.** "Largest landlocked country" is stale (everyone knows Kazakhstan), but "largest landlocked country in South America" (Bolivia) or "the largest in the Southern Hemisphere" re-opens the reasoning because the answer moves off the warhorse. The test isn't the dimension, it's whether the *answer* is the one a quizzer has already memorized. Novelty of the *specific question* is part of the difficulty-from-reasoning bargain, not a separate nicety. (Obscurity of the *answer* is still fine when the answer is the payoff — a surprising, delightful result the player couldn't have guessed cold is a feature; a worn-out question is the defect.)

### Felt variety

Quantified targets (≥75% unique dimensions, 8–10 archetypes) are necessary but gameable — a set can hit them and still *feel* repetitive. So also check felt variety directly: for each question after the first, compare it to the previous 3–5. If it shares a **dimension**, answer family, statistic type, obvious leaderboard, source, or wording shape ("most wins," "largest total," "oldest," "first," "largest margin") with a recent neighbor, swap in a different subtopic and archetype. Repeated dimensions are the most common culprit — if two nearby questions both come down to "which is biggest" or "which is oldest," that's a dimension collision even when the answer sets differ. Make the first five questions visibly different from one another, on five different dimensions.

### Sourcing: confidence + a cheap recheck path

Sourcing serves two ends: *your* confidence that the answer is both correct and unique, and an *easy path for the user to recheck* a result that looks wrong. It is not a one-citation-per-claim rule.

- **Multiple sources are fine and expected** for conditional and computed questions. Cite the support for each fact.
- **For computed answers** (code interpreter), name the datasets, state the method in one line, and note dataset coverage. Use code when it improves originality or accuracy — joining/cleaning/filtering/ranking public datasets to find records no single leaderboard shows: per-capita rates, "fewest while still achieving X," smallest subject to reach a milestone, largest gap, closest margin, biggest change, bottom-end leaders.
- **Never ship a question whose answer or uniqueness you couldn't verify.** Replace it and note the swap in the Plan.
- Prefer official bodies, government/statistical agencies, governing bodies, museums, universities, primary records, specialist databases, reputable reference works. Wikipedia is acceptable for stable, well-sourced historical facts that directly support the ranked claim. Journalism mainly for recent developments.
- Across a 30-question set, **don't lean on one domain for more than ~3 questions**, and avoid long runs from one source type. Add "as of [date/year]" for current/fiscal-year facts. Never cite a source that doesn't support the specific ranked claim.

### Flag contested definitions

Many rankings flip under a reasonable change of definition (longest river; largest company by market cap vs. revenue vs. employees; highest mountain by elevation vs. base-to-peak). If the answer would change under another fair definition, either avoid the question or **state the definition used in the stem and note the flip in the Follow-on.** Don't present a contested ranking as settled.

### No giveaways

Don't hand the solver the answer or the path to it. Keep out of the stem: source names, dataset names, publication names, governing-body names, reference-work names (unless the source itself is the answer subject); and the runner-up, predecessor, overtaken record-holder, or obvious comparator. Avoid "who overtook X," "ahead of Y," "according to Z," "unlike X," "beating the previous record of Y." Those details belong in the Follow-on.

**Also keep out the answer's own discriminating figure** — the very number, year, or measurement that singles it out. "Which country broke away *in 2011*" and "which country has *over a quarter-million* islands" both leak the fact the player is supposed to reason toward; they match the number instead of earning it. Name the category ("the world's newest nation," "the country with the most islands"), never the value. If the stem needs a threshold to be well-posed, make it a *boundary the solver reasons against* (e.g. "with no coastline at all"), not the answer's defining stat. But indirection must not create ambiguity — every stem must stay well-posed (gate step 3: exactly one *correct* answer, even though several finalists may look plausible to the solver).

### Reading level: 6th grade in the stem, precise everywhere else

Write every **question stem** at roughly a 6th-grade reading level even when the trivia is adult-difficulty: short sentences, common words, active voice. Say metrics in plain terms — "for each person" not "per capita," "land area" not "territorial extent," "how often it wins" not "win rate." Proper nouns and the one unavoidable domain term are allowed.

Technical and precise vocabulary stays out of the stem but is **free** in the Answer, Why-it's-interesting, and Follow-on fields — difficulty there is irrelevant, so optimize those for precision.

**Hard rule (load-bearing):** if plain wording makes the question ambiguous or changes the correct answer, restore the precise wording. Accuracy outranks reading level. Simpler words are usually *less* precise, so this trade-off is common — when it appears, precision wins, and gate step 3 is the check that catches it.

### Multiple topics / "more"

For multiple topics, distribute questions evenly and assign any remainder fairly. When the user asks for "more," generate fresh questions and avoid repeating earlier questions, answer subjects, archetypes, and sources from the conversation.

### Kid mode

If asked for kid mode, simplify the *subject matter* and wording further while keeping the same format, citations, and the guessable-with-reasoning mechanic.

## Output format

Open with a compact **Plan** block (the dimensions and archetypes covered, plus the unique-dimension ratio), then the numbered questions in this exact format:

```
1. [Question — 6th-grade wording, no giveaways]
   Answer: [subject] ([the specific ranked, comparative, or quantified fact])
   Why it's interesting: [scale, surprise, implication, or significance, using at least one exact number, rank, margin, rate, date, or comparison]
   Follow-on: [runner-up, margin, close competitor, changed record-holder, definition caveat, coverage limit, common wrong guess, or alternate ranking — with a quantified element]
   Source: [source name(s) with citations, directly attached to the claim]
```

- **Why it's interesting** must carry at least one exact number, rank, margin, rate, date, or comparison.
- **Follow-on** must add a real comparative detail with a quantified element.

## Rendering as an interactive HTML field guide

When the user asks to **render, display, lay out, or make an openable / tappable / hide-the-answer / quiz version** of a trivia set (whether you just generated it or produced it earlier in the conversation), output a single self-contained HTML file instead of, or in addition to, the plain-text format. Use the bundled template — do **not** hand-write fresh markup each time, so the look stays consistent.

**The template:** `assets/field-guide.html`. It's a "topographic field guide" design — drafting-paper tones, a survey benchmark medallion carrying each question's number — built around the core interaction: **each question is a large tap target that reveals only its own answer**, so the player reads, thinks, then taps. The cards are native `<details>` elements, so the page needs **no JavaScript to play** — it works in script-blocked viewers (in-app previews, sandboxed iframes) as well as full browsers. A quiet Reveal-all / Hide-all control and a live "revealed N of M" count are *progressive enhancement*: when scripts are allowed they appear in a sticky bar; when they aren't, the control stays hidden and per-question tapping still works fully. It is mobile-first and tuned for phone readability (17px base, ~1.6 line-height on answer text, full-width answer column with block labels, ≥44px tap targets, visible keyboard focus, reduced-motion and dark-mode support). It uses only system fonts and no browser storage, so it is fully self-contained and renders cleanly inside the Claude app.

**How to render:** the easiest path is `python scripts/render.py <set>.json`, which builds the cards and substitutes the masthead for you. If you must produce the HTML by hand:
1. Copy `assets/field-guide.html` to a working file.
2. Replace the `<!--__CARDS__-->` marker (inside `<div class="deck">`) with one server-rendered `<details class="card">` per question. Mirror the structure `render.py` emits: a `<summary class="q-toggle">` holding the numbered `.medallion`, the optional `.cat` eyebrow, the `.q-text`, and the `.hint`; then an `.answer-pad` with the `Answer` label, `.ans-main` (the `state`) plus optional `.ans-detail` (the `detail`), and `Why it's interesting` / `Follow-on` / `Source` fields. `cat` is a short two-part eyebrow naming the broad domain and sub-dimension, e.g. `"Nature · Elevation"` — a light hint that must not reveal the answer or single out the one finalist. Left unsubstituted, the page shows a harmless empty state.
3. Replace the masthead placeholders: `__EYEBROW__` (small kicker), `__TITLE_HTML__` (the H1; you may wrap one word in `<span class="num">…</span>` for the contour-colored accent), `__TITLE_PLAIN__` (same text, no markup, for the `<title>` tag), `__DEK__` (one-line intro), and `__FOOTER_HTML__` (a short sourcing note).
4. **HTML-escape every question/answer string** as you place it into the markup (`&`, `<`, `>`, `"` → entities). `render.py` does this for you with `html.escape`; never paste raw question text into the HTML.
5. Save to the outputs directory and present the file. Keep the plain-text Plan block in the chat reply so the variety audit is still visible.

The template's structure is generic, so it works for **any** topic, not just the one it was first built for — only the cards and the four masthead strings change.

## Running inside a trivia repo (library mode)

If the project contains `scripts/check_uniqueness.py` and a `library/` directory, you're in **library mode**: questions are saved to a growing repository so that uniqueness is guaranteed *across games*, not just within one set. The point is that the library — not your memory — is the source of truth for what's already been asked. Follow this loop instead of just printing questions:

1. **Survey the library first.** Run `python scripts/stats.py` to see which answer subjects and dimensions are already used. Treat already-used answers and heavily-used dimensions as off-limits or low-priority when you plan the grid, so the new set genuinely extends the library rather than overlapping it.
2. **Write the set to a JSON file** in the set schema (see `library/README.md`), e.g. `library/sets/<YYYY-MM-DD>-<topic-slug>.json`. Each question carries a normalized `dimension` and `answer_subject` in addition to the display fields, because those are what the uniqueness check fingerprints.
3. **Check it:** `python scripts/check_uniqueness.py <path-to-set>.json`. A non-zero exit means a **hard collision** — a question whose stem repeats one already in the library, or an answer subject that's been used before. Regenerate just the colliding questions (new dimension or new answer), then re-check. Near-duplicate and dimension-variety issues come back as warnings to weigh, not hard failures.
4. **Add it:** `python scripts/add_to_library.py <path-to-set>.json` re-runs the check, then files the set under `library/sets/` and rebuilds the index. After this, those questions and answers are reserved forever.
5. **Render and play:** `python scripts/render.py <path-to-set>.json` writes a self-contained field-guide HTML to `output/` using the bundled template.
6. **Commit** the new set file and the regenerated `library/index.jsonl` / `library/INDEX.md` so the next game (on any machine) sees them.

The skill still governs *how* questions are built (reasoning-driven, ≥75% unique dimensions within the set, well-posed, sourced). Library mode adds the cross-game guarantee on top: the scripts enforce that no question or answer is ever reused, and `stats.py` keeps the dimensional spread honest as the library grows.

## Final checklist

Before delivering, confirm:

- [ ] Every answer is drawn from a **listable set** (gate step 1); none rely on an unbounded answer space.
- [ ] Every question is **guessable by reasoning** (gate step 5): a reasoner can prune to ≈2–4 finalists and place a defensible bet — neither pure recall nor a forced deduction.
- [ ] Every stem is **well-posed** (gate step 3): exactly one *correct* answer in reality; no genuine ambiguity from plain wording, a tie, or a fair alternate definition. Solver uncertainty among the finalists is intended, not a defect.
- [ ] Stems read at ~6th-grade level; precise terms confined to the explanation fields; precision restored wherever plain wording would mislead.
- [ ] Sources support the **specific** claims; computed answers state method + coverage; no domain used more than ~3 times.
- [ ] **≥75% of questions sit on a unique dimension** (no other question shares that axis); no dimension used more than twice; the Plan block states the actual ratio.
- [ ] The set is **not clustered** by source, source type, era, geography, answer, statistic, dimension, or archetype; first five vary on five different dimensions; each question differs from the previous 3–5.
- [ ] Upward superlatives don't dominate; several questions use **filters/thresholds** and several are **bottom-end/inverted**.
- [ ] No **warhorses** (largest landlocked, longest coastline, smallest country, city-on-two-continents, etc.) and no stem leaking the answer's own discriminating figure; any filter is one a player would naturally reason with, not a carve-out.
- [ ] Contested-definition answers are flagged.
- [ ] Every Follow-on adds a useful quantified comparison.