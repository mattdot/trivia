# Exemplar bank — learned from human evals

Distilled from rated candidate batches in `evals/`. Feeds the rules in
`.claude/skills/trivia-generator/SKILL.md`. Gold = imitate; Anti = avoid.
Each entry notes the *rule* it teaches so the pattern transfers off-topic.

## Gold (keep / great)

- **Most populous country that shares no land border with anyone** → Japan.
  *Rule:* a natural filter that knocks out the obvious giants and leaves 3–4 real finalists (Japan, Philippines, UK, Madagascar).
- **Which country has more ancient pyramids than any other?** → Sudan (~200–250, vs Egypt's ~138). *(rated "great")*
  *Rule:* surprising answer is the payoff; the dimension looks like it has one obvious answer (Egypt) and doesn't.
- **Northernmost capital of any independent nation** → Iceland (Reykjavík).
  *Rule:* clean extreme on a fresh axis; finalists cluster (Reykjavík, Helsinki, Oslo, Tallinn) so it's a real bet.
- **Largest country completely surrounded by just one other** → Lesotho. *(rated "fun")*
  *Rule:* obscure-but-fun filtered record; the *concept* is the delight. Set is naturally tiny (Lesotho, San Marino, Vatican); "largest" is a clean tiebreak, not a gerrymander.
- **UN member country with the fewest people of all** → Tuvalu.
  *Rule:* bottom-end inversion + a natural membership filter (excludes Vatican without it feeling rigged).

## Anti-patterns (cut — and why)

- **Chestnuts / warhorses** — largest landlocked (Kazakhstan), longest coastline (Canada), city on two continents (Istanbul), highest capital (La Paz). Rated "common." *Rule:* reasoning-sound but everyone's met them; the player recalls the *question*. Re-slice (region/hemisphere/era) so the answer moves, or drop.
- **Binary identity recall** — "largest city split between Europe and Asia" → Turkey. Rated "you either know it or don't." *Rule:* looks like it has finalists but the discriminating fact is a single thing you know or you don't — no bet to place.
- **Hint in the stem** — "broke away *in 2011*" (South Sudan), "*over a quarter-million* islands" (Sweden). *Rule:* never state the answer's own discriminating figure; the player matches the number instead of reasoning to it. Name the *category* ("world's newest nation"), not the value.
- **Gerrymandered filter** — "highest GDP per person *among countries big enough to rank*" (Luxembourg). Rated "arbitrary." *Rule:* the qualifier exists only to fence out Monaco, and the seam shows. If the clean answer is a technicality you must exclude, the dimension is wrong — pick another.
- **Mangled inversion wording** — the "lowest high point" stem (Maldives) was rated "worded incorrectly for this style." *Rule:* inversions need clean phrasing — "which country's highest point is the lowest in the world?" — not a clause pile-up.

## Gold (batch 2)

- **Off-register dimension** — "most coffee drunk per person" → Finland. Rated "finally an interesting dimension that isn't geography or demographics… would love more variety like this." *Rule:* the dimension that breaks the topic's default register is the one players find refreshing. Seed several per set.
- **Seen-but-can't-recall** — "only country in all four hemispheres" → Kiribati. Rated "I've seen this but can never remember the country." *Rule:* this is the sweet spot, not a flaw — the answer resists memorization, so reasoning still pays.
- **Largest country the Equator runs through** → Brazil; **most populous country whose capital isn't its largest city** → China; **fewest people per square mile** → Mongolia; **smallest country on the African mainland** → The Gambia. *Rule:* re-sliced / bottom-end records on natural filters that leave close finalists.

## Anti-patterns (batch 2)

- **Decorative filter (no competition)** — "most populous country that drives on the left" → India. Rated "not sure it'd throw many off India." *Rule:* a filter that narrows to the obvious giant isn't doing work; leave 2–4 contenders genuinely hard to rank, or the filter is just decoration.
- **Revealing set cardinality** — "the *only two* doubly-landlocked countries, which is larger?" Rated "why are we giving away that there are two?" *Rule:* the count is a clue; state the property, not how many qualify.
- **Unspecified metric on a superlative** — same item, "how are we measuring largest?" *Rule:* when "largest/biggest" could mean area or population, say which.
- **Named-comparator boundary** — "more first-language Spanish speakers than *Spain* itself" → Mexico. Rated "giving away that it's not Spain." *Rule:* "more than [named X]" eliminates X for the solver; drop the named comparison.
