#!/usr/bin/env python3
"""slopcheck: flag machine-writing patterns in Markdown or plain text.

Usage:
    python3 tools/slopcheck.py draft.md [more.md ...]
    cat draft.md | python3 tools/slopcheck.py -

Exit status: 0 clean, 1 findings, 2 could not run.
Errors always fail. Warnings fail only with --strict.

Skipped: fenced code, inline code, link targets, blockquotes, text inside
double quotation marks, and anything between
<!-- slopcheck-disable --> and <!-- slopcheck-enable -->.

No dependencies beyond the Python 3 standard library.
"""
import argparse
import json
import re
import sys

ERROR, WARN = "error", "warn"
I = re.IGNORECASE
START = r"(?:^|(?<=[.!?]\s))"          # start of a sentence
AP = r"['’]"                       # straight or curly apostrophe
W = r"[\w'’-]+"                    # one word


def alt(*items):
    return r"\b(?:" + "|".join(items) + r")\b"


# (rule id, severity, compiled pattern, message)
RULES = [
    ("dash", ERROR,
     re.compile(r"—|(?<!\d)–(?!\d)|(?<=\s)--(?=\s)"),
     "Dash used as punctuation. Use a period, comma, colon, or parentheses."),

    ("contrast", ERROR,
     re.compile(
         r"\b(?:not|n" + AP + r"t)\s+(?:just|only|merely|simply)\b[^.?!]{0,100}?\bbut\b"
         r"|\b(?:(?:is|are|was|were|does|did)n" + AP + r"t"
         r"|(?:is|are|was|were|does|did|it" + AP + r"s|that" + AP + r"s|this is)\s+not)\b"
         r"[^.?!;]{1,80}[.;,]\s+(?:it|that|this|they)"
         r"(?:" + AP + r"s|" + AP + r"re|\s+(?:is|are|was|were|means?))\b"
         r"|\bnot because\b[^.?!]{1,80}[.,;]\s*(?:but\s+)?because\b"
         r"|\bthe (?:real )?(?:question|answer|problem|issue|point) (?:is|was)(?:n" + AP + r"t|\s+not)\b"
         r"|\bstops? being\b[^.?!]{1,60}\bstarts? being\b", I),
     "Contrast that adds weight and no claim. State the positive half directly."),

    ("negative-list", ERROR,
     re.compile(START + r"Not (?:an? |the )?[^.?!]{1,40}[.]\s+Not\b"),
     "Negative listing. Say what the thing is."),

    ("closer", ERROR,
     re.compile(alt(
         r"let that sink in", r"read that again", r"full stop\.",
         r"that" + AP + r"s it\.", r"that(?: is|" + AP + r"s) the (?:real|whole) \w+",
         r"only time will tell", r"(?:it )?remains to be seen",
         r"and that" + AP + r"s (?:okay|ok)\b"), I),
     "Closer that repeats or stalls. End on the last concrete fact."),

    ("run-up", ERROR,
     re.compile(alt(
         r"here(?:" + AP + r"s| is) the thing", r"here(?:" + AP + r"s| is) what (?:you need|i mean|nobody)",
         r"here" + AP + r"s why (?:that|this|it) matters", r"let" + AP + r"s dive in",
         r"let" + AP + r"s (?:break (?:this|it) down|unpack|explore|be honest)",
         r"let me be clear", r"make no mistake", r"the (?:uncomfortable |hard |simple )?truth is",
         r"the reality is", r"it turns out", r"can we talk about", r"what if i told you",
         r"think about it", r"plot twist", r"without further ado", r"real talk",
         r"what most people (?:miss|get wrong)", r"the part (?:everyone|most people) (?:misses|miss|skips|skip)",
         r"what nobody tells you"), I),
     "Run-up before the point. Cut it and state the point."),

    ("deep-saying", ERROR,
     re.compile(alt(
         r"at its core", r"the deeper issue", r"the heart of the matter",
         r"what really matters", r"the real question is",
         r"is the (?:currency|language|architecture) of"), I),
     "Saying that sounds deep. Replace with the specific claim."),

    ("no-one", ERROR,
     re.compile(START + alt(
         r"To be clear", r"Don" + AP + r"t get me wrong", r"This is not to say",
         r"Some might say", r"You might think", r"One might be tempted",
         r"It would be easy to (?:assume|think|say)")),
     "Arguing with no one. Remove it, or name who made the argument."),

    ("question-answer", ERROR,
     re.compile(START + r"(?:" + W + r"\s){0,4}" + W + r"\?\s+[A-Z][^.?!]{0,40}[.!]"),
     "Question answered at once. State the answer."),

    ("residue", ERROR,
     re.compile(alt(
         r"great question", r"i hope this helps", r"would you like me to",
         r"let me know if you", r"as of my last (?:update|training)",
         r"as an ai\b", r"based on (?:the )?available information",
         r"while (?:specific )?details are limited"), I),
     "Chatbot residue. Remove it."),

    ("importance", ERROR,
     re.compile(alt(
         r"pivotal moment", r"stands? as a testament", r"plays? an? (?:key|vital|crucial|pivotal) role",
         r"underscor(?:es|ing|ed) (?:the|its) (?:importance|significance)",
         r"reflects? a broader", r"sets? the stage for", r"sends? a clear message",
         r"the stakes are high", r"the implications are significant",
         r"a step in the right direction", r"the future looks bright",
         r"lasting legacy", r"indelible mark"), I),
     "Importance claim. State the fact and give the number, people, or deadline."),

    ("ing-clause", ERROR,
     re.compile(r",\s+(?:highlighting|underscoring|reflecting|showcasing|emphasizing|"
                r"signaling|symbolizing|raising questions about|cementing)\b", I),
     "Bolted-on -ing clause. Cut it or say what happened next."),

    ("unnamed-authority", ERROR,
     re.compile(alt(
         r"experts (?:say|agree|argue|warn|believe)", r"critics (?:say|argue|contend)",
         r"observers (?:say|note)", r"many (?:believe|argue|say)", r"studies show",
         r"industry reports (?:suggest|show)", r"widely regarded as", r"some critics"), I),
     "Unnamed authority. Name the person or publication, or cut the claim."),

    ("sweeping", ERROR,
     re.compile(alt(r"everyone knows", r"nobody saw (?:it|this) coming",
                    r"it" + AP + r"s no secret that", r"needless to say"), I),
     "Sweeping claim. Say who, how many, or how often."),

    ("dodging-is", ERROR,
     re.compile(alt(r"serves? as an?", r"stands? as an?", r"functions? as an?", r"boasts?"), I),
     "Use is, are, or has."),

    ("banned-word", ERROR,
     re.compile(alt(
         r"delv(?:e|es|ed|ing)", r"tapestry", r"testament", r"realm", r"beacon", r"interplay",
         r"intricate", r"intricac(?:y|ies)", r"multifaceted", r"meticulous(?:ly)?", r"pivotal",
         r"paramount", r"vibrant", r"transformative", r"groundbreaking", r"cutting-edge",
         r"game[- ]changer", r"paradigm shift", r"leverag(?:e|es|ed|ing)",
         r"utiliz(?:e|es|ed|ing)", r"facilitat(?:e|es|ed|ing)", r"foster(?:s|ed|ing)?",
         r"empower(?:s|ed|ing)?", r"streamlin(?:e|es|ed|ing)", r"supercharg(?:e|es|ed|ing)",
         r"showcas(?:e|es|ed|ing)", r"underscor(?:e|es|ed|ing)", r"garner(?:s|ed|ing)?",
         r"bolster(?:s|ed|ing)?", r"ever-evolving", r"lean(?:s|ed|ing)? into",
         r"doubl(?:e|es|ed|ing) down", r"deep dive", r"circl(?:e|es|ed|ing) back",
         r"moving forward", r"going forward", r"nestled", r"breathtaking", r"world-class",
         r"diverse array", r"in the heart of")),
     "Overused AI word. Use the plain word or cut it."),

    ("filler-phrase", ERROR,
     re.compile(alt(
         r"it" + AP + r"s worth noting", r"it is worth noting", r"it" + AP + r"s important to note",
         r"it is important to note", r"at the end of the day", r"when it comes to",
         r"in today" + AP + r"s world", r"in a world where", r"in an era of",
         r"with regard to", r"in order to"), I),
     "Filler phrase. Cut it."),

    ("emoji", ERROR,
     re.compile("[\U0001F000-\U0001FAFF☀-➿]"),
     "Emoji."),

    ("weak-word", WARN,
     re.compile(alt(
         r"landscape", r"robust", r"highlight(?:s|ed|ing)?", r"enhanc(?:e|es|ed|ing)",
         r"navigat(?:e|es|ed|ing)", r"quietly", r"crucial(?:ly)?", r"harness(?:es|ed|ing)?",
         r"elevat(?:e|es|ed|ing)", r"embark(?:s|ed|ing)?", r"unpack(?:s|ed|ing)?",
         r"renowned", r"stunning")),
     "Often an AI tell. Keep only if literal or technical."),

    ("adverb", WARN,
     re.compile(alt(
         r"really", r"literally", r"genuinely", r"honestly", r"simply", r"actually", r"truly",
         r"deeply", r"fundamentally", r"inherently", r"inevitably", r"importantly",
         r"interestingly", r"additionally"), I),
     "Adverb. Cut it if the sentence means the same without it."),

    ("vague-link", WARN,
     re.compile(alt(r"linked to", r"tied to", r"associated with", r"in connection with"), I),
     "Vague connection. Say what the relationship is, if the sources say."),

    ("colon-reveal", WARN,
     re.compile(START + r"(?:The|One|Another|My|Our|His|Her|Their)\s(?:" + W + r"\s){0,3}"
                + W + r":\s+[^,.:;?!\n]{3,60}[.!]"),
     "Possible colon reveal. Write a plain sentence."),

    ("stacked-qualifier", WARN,
     re.compile(alt(r"could potentially", r"might arguably", r"may possibly",
                    r"could possibly", r"might potentially"), I),
     "Stacked qualifiers. Keep one, and only if the sources are uncertain."),
]

SHAPE_RULES = {
    "fragments": (ERROR, "Three short fragments in a row. Merge them into a sentence with a claim."),
    "repeated-opener": (WARN, "Three sentences in a row open with the same word."),
    "short-paragraph": (WARN, "One short sentence standing alone. Check that it adds a fact."),
    "bold-emphasis": (WARN, "Bold used for emphasis inside a sentence."),
}

ALL_RULE_IDS = [r[0] for r in RULES] + list(SHAPE_RULES)


def blank(match):
    return " " * len(match.group(0))


def mask_line(line):
    """Replace text that must not be checked with spaces, keeping columns."""
    line = re.sub(r"`[^`]*`", blank, line)
    line = re.sub(r"\]\([^)]*\)", blank, line)
    line = re.sub(r"https?://\S+", blank, line)
    line = re.sub(r'"[^"]*"', blank, line)
    line = re.sub(r"“[^”]*”", blank, line)
    return line


def prepare(text):
    """Return a list of masked lines, same length and numbering as the input."""
    out, in_code, disabled = [], False, False
    for raw in text.split("\n"):
        stripped = raw.strip()
        if re.match(r"^(```|~~~)", stripped):
            in_code = not in_code
            out.append("")
            continue
        if "slopcheck-disable" in raw:
            disabled = True
        if "slopcheck-enable" in raw:
            disabled = False
            out.append("")
            continue
        if in_code or disabled or stripped.startswith(">") or stripped.startswith("<!--"):
            out.append("")
            continue
        out.append(mask_line(raw))
    return out


def paragraphs(lines):
    """Yield (first line number, text) for each run of non-empty lines."""
    start, buf = None, []
    for n, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = n
            buf.append(line)
        elif buf:
            yield start, "\n".join(buf)
            start, buf = None, []
    if buf:
        yield start, "\n".join(buf)


def is_prose(par):
    if re.fullmatch(r"\s*\*\*[^*\n]+\*\*:?\s*", par):
        return False          # a bold label on its own line
    return not re.match(r"\s*(#|\||[-*+]\s|\d+[.)]\s|\()", par)


def sentences(par):
    flat = re.sub(r"\s+", " ", par).strip()
    return [s for s in re.split(r"(?<=[.!?])\s+", flat) if re.search(r"\w", s)]


def check(text):
    findings = []
    lines = prepare(text)

    def add(rule, severity, message, line, col, snippet):
        findings.append({"rule": rule, "severity": severity, "line": line, "col": col,
                         "message": message, "text": snippet.strip()[:80]})

    previous_was_prose = False
    for first, par in paragraphs(lines):
        for rule, severity, pattern, message in RULES:
            for m in pattern.finditer(par):
                before = par[:m.start()]
                line = first + before.count("\n")
                col = m.start() - (before.rfind("\n") + 1) + 1
                add(rule, severity, message, line, col, m.group(0))

        prose = is_prose(par)
        if prose:
            sents = sentences(par)
            counts = [len(re.findall(r"\w+", s)) for s in sents]
            for i in range(len(sents) - 2):
                if all(c <= 3 for c in counts[i:i + 3]):
                    sev, msg = SHAPE_RULES["fragments"]
                    add("fragments", sev, msg, first, 1, " ".join(sents[i:i + 3]))
                    break
            openers = [re.match(r"\W*(\w+)", s).group(1).lower() for s in sents]
            for i in range(len(openers) - 2):
                if openers[i] == openers[i + 1] == openers[i + 2]:
                    sev, msg = SHAPE_RULES["repeated-opener"]
                    add("repeated-opener", sev, msg, first, 1, " ".join(sents[i:i + 3]))
                    break
            if previous_was_prose and len(sents) == 1 and counts[0] <= 6:
                sev, msg = SHAPE_RULES["short-paragraph"]
                add("short-paragraph", sev, msg, first, 1, sents[0])
        previous_was_prose = prose

    for n, line in enumerate(lines, 1):
        for m in re.finditer(r"\*\*[^*\n]+\*\*", line):
            prefix = line[:m.start()]
            label_position = re.fullmatch(r"\s*(?:[-*+]\s+|\d+[.)]\s+)?(?:.*\|\s*)?", prefix)
            is_label = m.group(0).endswith(":**") or line[m.end():m.end() + 1] == ":"
            if not label_position and not is_label:
                sev, msg = SHAPE_RULES["bold-emphasis"]
                add("bold-emphasis", sev, msg, n, m.start() + 1, m.group(0))

    findings.sort(key=lambda f: (f["line"], f["col"]))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Flag machine-writing patterns in Markdown or plain text.")
    parser.add_argument("files", nargs="*", help="files to check, or - for standard input")
    parser.add_argument("--strict", action="store_true", help="warnings also fail")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    parser.add_argument("--ignore", action="append", default=[], metavar="RULE",
                        help="skip a rule; may be repeated")
    parser.add_argument("--list-rules", action="store_true", help="print rule ids and exit")
    args = parser.parse_args(argv)

    if args.list_rules:
        for rule, severity, _, message in RULES:
            print(f"{rule:18} {severity:6} {message}")
        for rule, (severity, message) in SHAPE_RULES.items():
            print(f"{rule:18} {severity:6} {message}")
        return 0
    unknown = [r for r in args.ignore if r not in ALL_RULE_IDS]
    if unknown:
        print("unknown rule: " + ", ".join(unknown), file=sys.stderr)
        return 2
    if not args.files:
        parser.print_usage(sys.stderr)
        return 2

    results, errors, warnings = [], 0, 0
    for path in args.files:
        try:
            if path == "-":
                text = sys.stdin.read()
            else:
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
        except OSError as exc:
            print(f"{path}: {exc.strerror}", file=sys.stderr)
            return 2
        for f in check(text):
            if f["rule"] in args.ignore:
                continue
            f["file"] = "<stdin>" if path == "-" else path
            results.append(f)
            errors += f["severity"] == ERROR
            warnings += f["severity"] == WARN

    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "findings": results}, indent=2))
    else:
        for f in results:
            print(f'{f["file"]}:{f["line"]}:{f["col"]}: {f["severity"]} [{f["rule"]}] '
                  f'{f["message"]} "{f["text"]}"')
        print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
