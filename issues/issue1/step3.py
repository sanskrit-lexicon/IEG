#!/usr/bin/env python3
"""
step3.py - Merge CDSL corrections into AB base text.
Takes CDSL {{...}} printchange annotations and inserts them at the
corresponding positions in the AB text.

Reads temp_cdsl_ieg2.txt and temp_ab_ieg2.txt.
Writes merged_ieg3.txt.
"""
import re

CDSL_IN = "temp_cdsl_ieg2.txt"
AB_IN = "temp_ab_ieg2.txt"
OUT = "merged_ieg3.txt"


def parse_blocks(lines):
    """Parse file into ordered list of (key, tag, content) tuples."""
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        if line.startswith('<L>'):
            l_tag = line
            m = re.match(r'<L>(\d+)', l_tag)
            key = m.group(1) if m else l_tag
            i += 1
            content = []
            while i < len(lines) and not lines[i].startswith('<L>'):
                content.append(lines[i].rstrip('\n'))
                i += 1
            blocks.append((key, l_tag, content))
        else:
            i += 1
    return blocks


def extract_corrections(text):
    """
    Extract all {{...}} corrections from text.
    Returns list of dicts with keys:
      full, wrong, right, metadata, start, end, dev_wrapped
    Handles:
      - {{wrong->right||metadata}}
      - {%{{wrong->right||metadata}}%}
      - {%{{wrong->right||metadata}},%}
      - Adjacent {{...}}{{...}}
    """
    corrections = []
    pos = 0
    while pos < len(text):
        # Find the next {{...}} segment
        curly_start = text.find('{{', pos)
        if curly_start < 0:
            break
        curly_end = text.find('}}', curly_start + 2)
        if curly_end < 0:
            break

        # Check if this is wrapped in {% ... %}
        dev_wrapped = False
        # See if there's a {% just before {{
        if curly_start >= 2 and text[curly_start-2:curly_start] == '{%':
            between = text[curly_start-2:curly_start]
            dev_wrapped = True
        elif curly_start >= 1 and curly_start - 1 >= 0:
            # Check: some lines have {% at start, {{ immediately after
            pre = text[max(0, curly_start-5):curly_start]
            brace_idx = pre.rfind('{%')
            if brace_idx >= 0:
                between = pre[brace_idx+2:].strip()
                if not between or between == '%':
                    dev_wrapped = True

        # Determine what comes after }}
        if dev_wrapped:
            # The %} or ,%} follows the }}
            if curly_end + 2 < len(text) and text[curly_end+2:curly_end+4] == '%}':
                pass  # standard case
            elif curly_end + 3 < len(text) and text[curly_end+2:curly_end+5] == ',%}':
                pass  # trailing comma before %}

        # Extract just the {{...}} part (without any {% %} wrapping)
        full = text[curly_start:curly_end + 2]
        correction_start = curly_start
        correction_end = curly_end + 2

        # Parse inner content
        inner = text[curly_start + 2:curly_end]
        wrong = ''
        right = ''
        metadata = ''
        if '->' in inner:
            parts = inner.split('->', 1)
            wrong = parts[0]
            rest = parts[1]
            if '||' in rest:
                right = rest.split('||')[0]
                metadata = rest[len(right) + 2:]
            else:
                right = rest
        else:
            # No ->: the whole inner is context, no wrong->right
            wrong = inner

        corrections.append({
            'full': full,
            'wrong': wrong,
            'right': right,
            'metadata': metadata,
            'start': correction_start,
            'end': correction_end,
            'dev_wrapped': dev_wrapped,
        })

        # Advance past the %} or ,%} wrapper if dev_wrapped
        if dev_wrapped:
            if curly_end + 2 < len(text) and text[curly_end+2:curly_end+4] == '%}':
                pos = curly_end + 4
            elif curly_end + 3 < len(text) and text[curly_end+2:curly_end+5] == ',%}':
                pos = curly_end + 5
            else:
                pos = curly_end + 2
        else:
            pos = curly_end + 2

    return corrections


def insert_correction_in_ab(ab_text, correction):
    """
    Insert a single correction into AB text at the appropriate position.
    Returns modified ab_text.
    """
    full = correction['full']
    wrong = correction['wrong']
    right = correction['right']
    metadata = correction['metadata']
    dev_wrapped = correction['dev_wrapped']

    if not right and not wrong:
        return ab_text

    if dev_wrapped:
        # Replace the content of {%...%} with the correction
        m = re.search(r'\{%([^}]*?)%\}', ab_text)
        if m:
            ab_text = ab_text[:m.start()] + '{%' + full + '%}' + ab_text[m.end():]
        return ab_text

    # Plain correction: replace 'right' with the correction text
    if not right:
        return ab_text

    pos = ab_text.find(right)
    if pos >= 0:
        ab_text = ab_text[:pos] + full + ab_text[pos + len(right):]
    else:
        # Fallback: try to find 'wrong' in AB
        if wrong:
            pos = ab_text.find(wrong)
            if pos >= 0:
                ab_text = ab_text[:pos] + full + ab_text[pos + len(wrong):]

    return ab_text


def merge_block(cdsl_content, ab_content):
    """
    Merge a single CDSL block (with potential {{...}} corrections)
    into the corresponding AB block.
    """
    cdsl_text = '\n'.join(cdsl_content)
    ab_text = '\n'.join(ab_content)

    corrections = extract_corrections(cdsl_text)

    if not corrections:
        # No corrections: just use AB as-is
        return ab_content

    # Apply each correction left-to-right, updating positions
    current_ab = ab_text
    for corr in corrections:
        current_ab = insert_correction_in_ab(current_ab, corr)

    return current_ab.split('\n')


# Read files
with open(CDSL_IN, 'r', encoding='utf-8') as f:
    cdsl_lines = f.readlines()
with open(AB_IN, 'r', encoding='utf-8') as f:
    ab_lines = f.readlines()

cdsl_blocks = parse_blocks(cdsl_lines)
ab_blocks = parse_blocks(ab_lines)

# Build per-key queues for CDSL blocks (preserving order)
cdsl_by_key = {}
for key, tag, content in cdsl_blocks:
    cdsl_by_key.setdefault(key, []).append((tag, content))

merged_lines = []

# Process AB blocks in order, matching with CDSL blocks by key
for ab_key, ab_tag, ab_content in ab_blocks:
    # Use AB's tag text
    tag_line = ab_tag

    # Pop the next CDSL block with the same key (if any)
    cdsl_queue = cdsl_by_key.get(ab_key, [])
    if cdsl_queue:
        cdsl_tag, cdsl_content = cdsl_queue.pop(0)
        # Check if CDSL has {{...}} corrections in this block
        cdsl_text = '\n'.join(cdsl_content)
        if '{{' in cdsl_text:
            merged_content = merge_block(cdsl_content, ab_content)
        else:
            merged_content = ab_content
    else:
        merged_content = ab_content

    merged_lines.append(tag_line)
    merged_lines.extend(merged_content)

# Append any remaining CDSL blocks (not matched to AB)
remaining = []
for key, queue in cdsl_by_key.items():
    for tag, content in queue:
        remaining.append((key, tag, content))
remaining.sort(key=lambda x: (int(x[0]) if x[0].isdigit() else 0))
for key, tag, content in remaining:
    merged_lines.append(tag)
    merged_lines.extend(content)

# Ensure every <L> block has a matching <LEND>
final = []
pending_l = False
for line in merged_lines:
    if line.startswith('<LEND'):
        pending_l = False
        final.append(line)
    elif line.startswith('<L>'):
        if pending_l:
            final.append('<LEND>')
        pending_l = True
        final.append(line)
    else:
        final.append(line)
if pending_l:
    final.append('<LEND>')

with open(OUT, 'w', encoding='utf-8') as f:
    for line in final:
        f.write(line + '\n')

print(f"Written {OUT} ({len(merged_lines)} lines)")
print("Done.")
