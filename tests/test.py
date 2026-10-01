from html.parser import HTMLParser
from pathlib import Path
import sys


class ListParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.tags = []
        self.ol_attributes = []
        self.li_text = []
        self.current_li = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        self.tags.append(tag)

        if tag == "ol":
            self.ol_attributes.append(attrs)

        if tag == "li":
            self.current_li = ""

    def handle_data(self, data):
        text = data.strip()

        if self.current_li is not None and text:
            self.current_li += " " + text

    def handle_endtag(self, tag):

        if tag == "li" and self.current_li is not None:
            self.li_text.append(
                " ".join(self.current_li.split())
            )
            self.current_li = None

        if self.tags and self.tags[-1] == tag:
            self.tags.pop()


def fail(message):
    print("FAIL:", message)
    sys.exit(1)


def check(condition, message, points):
    if condition:
        print(f"PASS ({points}/50): {message}")
    else:
        fail(message)


# --------------------------------------------------
# Check file
# --------------------------------------------------

index = Path("index.html")

if not index.exists():
    fail("index.html was not found.")

html = index.read_text(encoding="utf-8")


# --------------------------------------------------
# Parse HTML
# --------------------------------------------------

parser = ListParser()

try:
    parser.feed(html)
except Exception as e:
    fail(f"HTML parsing failed: {e}")


# --------------------------------------------------
# 1. HTML document structure - 5 marks
# --------------------------------------------------

required_tags = [
    "<!DOCTYPE html>",
    "<html",
    "<head>",
    "<body>",
    "</html>"
]

for tag in required_tags:
    if tag.lower() not in html.lower():
        fail(f"Missing required document element: {tag}")

print("PASS (5/50): Correct HTML document structure")


# --------------------------------------------------
# 2. Heading - 5 marks
# --------------------------------------------------

expected_heading = "How to use the WinZip Self Extractor"

if expected_heading not in html:
    fail("Required h2 heading is missing.")

if "<h2>" not in html.lower():
    fail("The heading must use the h2 element.")

print("PASS (5/50): Correct h2 heading")


# --------------------------------------------------
# 3. Outer unordered list - 5 marks
# --------------------------------------------------

ul_count = html.lower().count("<ul")

check(
    ul_count == 1,
    "Exactly one outer unordered list is present.",
    5
)


# --------------------------------------------------
# 4. Main list items - 10 marks
# --------------------------------------------------

first_main = "Before you start the WinZip Self Extractor"
second_main = "How to create an executable file"

check(
    first_main in html,
    "First main list item is present.",
    5
)

check(
    second_main in html,
    "Second main list item is present.",
    5
)


# --------------------------------------------------
# 5. Nested ordered lists - 10 marks
# --------------------------------------------------

ol_count = html.lower().count("<ol")

check(
    ol_count == 2,
    "Two nested ordered lists are present.",
    5
)


# Find all <ol> opening tags
import re

ol_tags = re.findall(r"<ol\b([^>]*)>", html, re.IGNORECASE)

if len(ol_tags) != 2:
    fail("Expected exactly two ordered lists.")

first_ol_attributes = ol_tags[0]
second_ol_attributes = ol_tags[1]

# First ordered list should not specify start
if "start" in first_ol_attributes.lower():
    fail("The first ordered list should start normally at 1.")

print("PASS (2.5/50): First ordered list starts at 1.")


# Second ordered list must start at 4
if not re.search(
    r'\bstart\s*=\s*["\']?4["\']?',
    second_ol_attributes,
    re.IGNORECASE
):
    fail('Second ordered list must use start="4".')

print('PASS (2.5/50): Second ordered list uses start="4".')


# --------------------------------------------------
# 6. Required list content - 10 marks
# --------------------------------------------------

required_content = [
    "Create a text file that contains the message you want to be displayed when the executable starts.",
    "Create a batch file that copies the exercises, and store it in the main directory for the files to be zipped.",
    "Create the zip file.",
    "Run the WinZip Self Extractor program and click through the first three dialog boxes.",
    "Enter the name of the zip file in the fourth dialog box.",
    "Click the Next button to test the executable."
]

for content in required_content:
    if content not in " ".join(parser.li_text):
        fail(f"Missing required list content: {content}")

print("PASS (10/50): All six required list items are present.")


# --------------------------------------------------
# Final result
# --------------------------------------------------

print()
print("=" * 40)
print("ALL AUTOMATED TESTS PASSED")
print("SCORE: 50/50")
print("=" * 40)

sys.exit(0)
