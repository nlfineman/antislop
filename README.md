# antislop

Rules that keep prose from reading as machine-written. Four open-source guides are merged here into one file that a writing or editing agent can load.

## What to load

| File | Use |
| --- | --- |
| [ANTI-SLOP.md](ANTI-SLOP.md) | The merged rules. Add it to the system prompt of any agent that writes or edits prose. |
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

## Optional mechanical check

[slopless](https://github.com/berelevant-ai/slopless) is a linter that flags many of these patterns in Markdown without calling a model. It is not installed here. To try it, from a machine with Node 22 or later:

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
