# antislop

Rules that keep prose from reading as machine-written. Four open-source guides are merged here into one file that a writing or editing agent can load.

## What to load

| File | Use |
| --- | --- |
| [ANTI-SLOP.md](ANTI-SLOP.md) | The merged rules. Add it to the system prompt of any agent that writes or edits prose. |
| [examples/before-after.md](examples/before-after.md) | Worked rewrites for each pattern. Load it with the rules. |
| [tools/slopcheck.py](tools/slopcheck.py) | A checker that fails a draft containing the patterns. |
| [sources/](sources/) | The four original guides, unmodified, with their licenses. Reference only. |

`ANTI-SLOP.md` is plain Markdown with no tool-specific syntax, so it works with any model.

## Where the merged rules differ from the sources

The four guides disagree with each other in places. `ANTI-SLOP.md` settles each one:

| Topic | Source positions | Rule here |
| --- | --- | --- |
| Em dashes | stop-slop and humanizer: none. no-ai-slop: one or two in a long piece. | None, because zero can be checked mechanically. |
| Adverbs | stop-slop: remove all. no-ai-slop: remove the empty ones. | Remove the empty ones. |
| Lists of three | stop-slop: use two. humanizer: keep three when the meaning has three parts. | Keep three real items. Decorative triads go. |
| Sentences opening with Why, What, How | stop-slop: restructure all. | Not adopted. The blanket rule produces stiff copy. |
| Hedges | humanizer: cut stacked qualifiers. | Cut stacked ones. Keep every attribution and every statement of real doubt. |
| Vague sentences | All four: replace with a specific. | Replace only with a fact from the source material. Otherwise simplify or cut. Never invent. |
| Endings | Sources: cut punchy closers. | End on a concrete consequence, date, or figure. No aphorisms. |

The sources' instructions for chat replies, code comments, fiction, and encyclopedia articles are left out.

## Checking a draft

`tools/slopcheck.py` needs Python 3 and nothing else.

```bash
python3 tools/slopcheck.py draft.md
```

It prints each finding with its line, column, and rule, and exits `0` when the draft is clean, `1` when it has errors, and `2` when it could not run. Errors are the strong tells: dashes, empty contrasts, run-ups, closers, fragments, unnamed authority, importance claims, and the banned words. Warnings are weaker signs such as adverbs and vague links, and they fail the check only with `--strict`.

| Option | Effect |
| --- | --- |
| `--strict` | Warnings also fail |
| `--json` | Findings as JSON, for an agent to read |
| `--ignore RULE` | Skip one rule. Repeat for more. |
| `--list-rules` | Print every rule id |
| `-` | Read from standard input |

The checker skips code, link targets, blockquotes, and text inside double quotation marks, so quoted speech is never flagged. To exempt a passage, put `<!-- slopcheck-disable -->` before it and `<!-- slopcheck-enable -->` after it.

To use it with a writing agent, tell the agent: "After drafting, run `python3 tools/slopcheck.py --json` on the draft and revise until it exits 0. Do not use `--ignore` or the disable comment to pass."

A clean result means the listed patterns are absent. It does not mean the writing is good, and it cannot tell whether a sentence says anything. The rules and examples cover what a pattern match cannot.

Run the checker's own tests with:

```bash
python3 tools/test_slopcheck.py
```

## Another mechanical check

[slopless](https://github.com/berelevant-ai/slopless) is a separate, larger linter with more than 50 rules. It is not installed here. To try it, from a machine with Node 22 or later:

```bash
npx slopless "draft.md"
```

It prints JSON findings and exits `0` when clean. Its default rules run locally. Its optional "Jev" checks send the text to a third-party API (TypeSafe) and need an API key.

## Sources and credit

All four are MIT licensed. The copies in `sources/` are unmodified and each folder carries the original license.

| Source | Author | Copied at commit | What it contributed |
| --- | --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer) | Siqi Chen | `b48c832f0f80` | The ranking of tells by strength, the explanation of why models write this way, borrowed authority, vague connection, the fact-preservation check. Its patterns derive from Wikipedia's "Signs of AI writing". |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | Peter Yang | `000650b15698` | Voice preservation, the minimum effective edit, the portability test, colon reveals, synonym cycling, detection mode. |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | Hardik Pandya | `8da1f030185b` | False agency, vague declaratives, the phrase lists, the quick checks. |
| [berelevant-ai/slopless](https://github.com/berelevant-ai/slopless) | websmasher / berelevant.ai | `abfe9b99021c` | The mechanical linter. Only its README and license are copied here. |

To refresh from upstream, replace the files in `sources/` with the current versions, update the commit column, and review `ANTI-SLOP.md` against whatever changed.
