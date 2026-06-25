#!/usr/bin/env python3
"""
step2.py - Post-process step1 output: apply targeted formatting fixes.
Reads temp_cdsl_ieg1.txt and temp_ab_ieg1.txt, writes temp_cdsl_ieg2.txt and temp_ab_ieg2.txt.

CDSL fixes:
  (1) Change ',¦' to '¦,' (comma-danda order)
  (2) Change ' = ' to '=' (remove spaces around equals)
  (3) Change 'ĕ' to 'ě' (Unicode normalization)
  (4) Change ';%}' to '%};' (semicolon before %} moved after)
AB fixes:
  (1) Change '    <P>¦' to '<P>¦' (remove 4-space indent on paragraph lines)
  (2) Change '°' to '˚' (degree sign to ring above, for transliteration)
  (3) Change 'Chhid' to 'Chid' (word fix)
"""
import re

CDSL_IN = "temp_cdsl_ieg1.txt"
AB_IN = "temp_ab_ieg1.txt"
CDSL_OUT = "temp_cdsl_ieg2.txt"
AB_OUT = "temp_ab_ieg2.txt"

COMMA_DANDA_RE = re.compile(r',\u00a6')
SPACED_EQ_RE = re.compile(r' = ')
P_INDENT_RE = re.compile(r'    <P>¦')
E_RE = re.compile(r'\u0115')


def fix_cdsl_text(text: str) -> str:
    text = COMMA_DANDA_RE.sub('\u00a6,', text)
    text = SPACED_EQ_RE.sub('=', text)
    text = E_RE.sub('e\u030c', text)
    text = text.replace(';%}', '%};')
    return text


def fix_ab_line(line: str) -> str:
    line = P_INDENT_RE.sub('<P>¦', line)
    line = line.replace('\u00b0', '\u02da')
    line = line.replace('Chhid', 'Chid')
    return line


with open(AB_IN, 'r', encoding='utf-8') as f:
    ab_lines = f.readlines()

with open(AB_OUT, 'w', encoding='utf-8') as f:
    for line in ab_lines:
        f.write(fix_ab_line(line))
print(f"Written {AB_OUT} ({len(ab_lines)} lines)")

with open(CDSL_IN, 'r', encoding='utf-8') as f:
    cdsl_text = f.read()

cdsl_text = fix_cdsl_text(cdsl_text)

with open(CDSL_OUT, 'w', encoding='utf-8') as f:
    f.write(cdsl_text)
cdsl_lines = cdsl_text.splitlines()
print(f"Written {CDSL_OUT} ({len(cdsl_lines)} lines)")
print("Done.")
