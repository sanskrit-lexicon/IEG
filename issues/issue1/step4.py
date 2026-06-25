#!/usr/bin/env python3
"""
step4.py - Concatenate preface, merged entries, and endmatter into a single file.
Reads temp_ieg_preface.txt, temp_merged_ieg3.txt, temp_ieg_endmatter.txt.
Writes temp_merged_ieg4.txt.
"""

PREFACE = "temp_ieg_preface.txt"
BODY = "temp_merged_ieg3.txt"
ENDMATTER = "temp_ieg_endmatter.txt"
OUT = "temp_merged_ieg4.txt"

with open(PREFACE, 'r', encoding='utf-8') as f:
    preface = f.read()
with open(BODY, 'r', encoding='utf-8') as f:
    body = f.read()
with open(ENDMATTER, 'r', encoding='utf-8') as f:
    endmatter = f.read()

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(preface)
    f.write('\n')
    f.write(body)
    f.write('\n')
    f.write(endmatter)

# Count lines
total_lines = preface.count('\n') + body.count('\n') + endmatter.count('\n')
print(f"Written {OUT} ({total_lines} lines total)")
print("Done.")
