#!/usr/bin/env python3
"""Tests for slopcheck. Run: python3 tools/test_slopcheck.py"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slopcheck  # noqa: E402

ROOT = os.path.dirname(HERE)


def rules(text):
    return {f["rule"] for f in slopcheck.check(text)}


def errors(text):
    return [f for f in slopcheck.check(text) if f["severity"] == "error"]


SLOP = {
    "dash": "The policy — announced Monday — affects thousands.",
    "contrast": "This isn't about money. It's about respect.",
    "negative-list": "Not a tax. Not a fee. A toll.",
    "closer": "The drug was approved in six months. Let that sink in.",
    "run-up": "Here's the thing about the stadium deal.",
    "deep-saying": "At its core, the dispute concerns land.",
    "no-one": "To be clear, the plan has flaws.",
    "question-answer": "The result? Chaos.",
    "residue": "I hope this helps with your project.",
    "importance": "The ruling marks a pivotal moment for tenants.",
    "ing-clause": "The airline cut 30 routes, highlighting the pressure on carriers.",
    "unnamed-authority": "Experts say the bridge is unsafe.",
    "sweeping": "Everyone knows the subway runs late.",
    "dodging-is": "The warehouse serves as a hub for the region.",
    "banned-word": "The team will leverage the new tool.",
    "filler-phrase": "It's worth noting that the vote was close.",
    "emoji": "Sales rose last quarter \U0001F680",
    "weak-word": "The changing landscape worries investors.",
    "adverb": "The plan is actually quite old.",
    "vague-link": "The senator is linked to the firm.",
    "colon-reveal": "The catch: none of it is refundable.",
    "stacked-qualifier": "The rule could potentially apply here.",
    "fragments": "The council met for an hour and adjourned. No warning. No hearing. No appeal.",
    "repeated-opener": "She opened the door slowly today. She looked at the lock twice. She walked away without a word.",
    "bold-emphasis": "The vote was **extremely** close this year.",
    "short-paragraph": "The agency approved the drug in six months, half the usual time.\n\nNobody asked why.",
}

CLEAN = """# Council ends free bus service

The city council voted 6 to 3 on Tuesday to end free bus service and bring
back a $1.50 fare on July 1. The transit agency told the council it faces a
$14 million shortfall next year and that fares would cover about half of it.

Council member Lee Park, who voted no, said riders in her district take the
bus twice as often as riders elsewhere in the city.

- **Fare:** $1.50 from July 1
- **Shortfall:** $14 million

| Year | Riders |
| --- | --- |
| 2024 | 1.2 million |

The pages 10–12 of the report cover ridership.
"""


class SlopcheckTests(unittest.TestCase):
    def test_each_rule_fires(self):
        for rule, text in SLOP.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, rules(text))

    def test_every_rule_has_a_case(self):
        self.assertEqual(set(SLOP), set(slopcheck.ALL_RULE_IDS))

    def test_clean_text_passes(self):
        self.assertEqual(slopcheck.check(CLEAN), [])

    def test_real_contrast_in_one_clause_passes(self):
        self.assertEqual(errors("The mayor did not attend the vote on Tuesday."), [])

    def test_instruction_followed_by_reason_passes(self):
        self.assertEqual(errors("Do not add jokes to the summaries. They are meant to be plain."), [])

    def test_separators_and_attributions_are_skipped(self):
        text = (
            "The council voted 6 to 3 on Tuesday.\n\n"
            "\u2014 Jane Doe\n\n"
            "\u2014 2026-11-18\n\n"
            "\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\n\n"
            "* **Politics:** [Council ends free buses](https://example.com/a) \u2014 The Associated Press\n\n"
            "[Fare rises to $1.50](https://example.com/b) \u2013 Reuters\n\n"
            "\u201c_**\"Print what others want hidden.\"**_\u201d \u2014\n"
        )
        self.assertEqual(errors(text), [])

    def test_dashes_in_prose_still_fail(self):
        for text in (
            "He had one goal \u2014 power over the board.",
            "\u2014 And then the council voted to end free service for every rider in the city.",
            "[The report](https://example.com) \u2014 released Monday. It found waste.",
            "Prices rose \u2014 sharply.",
        ):
            with self.subTest(text=text):
                self.assertIn("dash", {f["rule"] for f in errors(text)})

    def test_quotes_are_skipped(self):
        self.assertEqual(errors('The mayor said "let that sink in" twice.'), [])
        self.assertEqual(errors("The mayor said “make no mistake” twice."), [])

    def test_blockquotes_code_and_links_are_skipped(self):
        text = (
            "> Experts say this is a pivotal moment.\n\n"
            "```\nleverage — delve\n```\n\n"
            "Run `leverage --delve` now.\n\n"
            "See [the report](https://example.com/deep-dive-leverage) today.\n"
        )
        self.assertEqual(errors(text), [])

    def test_disable_comment(self):
        text = "<!-- slopcheck-disable -->\nExperts say so.\n<!-- slopcheck-enable -->\n\nExperts say so.\n"
        found = slopcheck.check(text)
        self.assertEqual([f["line"] for f in found], [5])

    def test_line_and_column(self):
        found = [f for f in slopcheck.check("A fine line.\n\nThe team will leverage it.\n")
                 if f["rule"] == "banned-word"]
        self.assertEqual((found[0]["line"], found[0]["col"]), (3, 15))

    def test_exit_codes(self):
        clean = os.path.join(ROOT, "README.md")
        self.assertEqual(slopcheck.main([clean]), 0)
        self.assertEqual(slopcheck.main(["no-such-file.md"]), 2)
        self.assertEqual(slopcheck.main(["--ignore", "no-such-rule", clean]), 2)

    def test_repo_documents_have_no_errors(self):
        for name in ("README.md", "ANTI-SLOP.md", os.path.join("examples", "before-after.md")):
            with self.subTest(file=name):
                with open(os.path.join(ROOT, name), encoding="utf-8") as handle:
                    text = handle.read()
                self.assertEqual(errors(text), [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
