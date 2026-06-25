#!/usr/bin/env python3
"""
step1.py - Transform CDSL and AB files to align them as closely as possible.
- CDSL: strip introduction before <L>1, consolidate multi-line entries,
  wrap refs in <ls>, wrap Latin abbrs in <ab>, match AB blank-line structure.
- AB: minimal cleanup (remove G/D/$ prefixes, fix <LEND?>).
Output: temp_cdsl_ieg1.txt, temp_ab_ieg1.txt
"""
import re

CDSL_IN = "temp_cdsl_ieg0.txt"
AB_IN = "temp_ab_ieg0.txt"
CDSL_OUT = "temp_cdsl_ieg1.txt"
AB_OUT = "temp_ab_ieg1.txt"

REF_ABBREVIATIONS = [
    "Select Inscriptions",
    "The Successors of the Sātavāhanas",
    "Wilson's Glossary",
    "Bhandarkar's List",
    "Hyderabad Archaeological Series",
    "Stud. Geog. Anc. Med. Ind.",
    "Viṣṇudharmottara",
    "Viṣṇu Dharmasūtra",
    "Yājñavalkyasmṛti",
    "Vyavahāra-kāṇḍa",
    "History of Kanauj",
    "Amarakośa, Kṣatriya-varga",
    "Ep. Ind.",
    "Ind. Ant.",
    "Ind. Ep.",
    "Sel. Ins.",
    "Hist. Dharm.",
    "Ant. Ch. St.",
    "A. R. Ep.",
    "Bomb. Gaz.",
    "H. Rev. Syst.",
    "Journ. Or. Inst.",
    "Journ. Mad. Univ.",
    "Pāli-Eng. Dict.",
    "Bṛhatsaṃhitā",
    "Kṛtyakalpataru",
    "Matsya Purāṇa",
    "Mahābhārata",
    "Harṣacarita",
    "Kādambarī",
    "Kāmasūtra",
    "Līlāvatī",
    "Manusmṛti",
    "Mitākṣarā",
    "Pāṇini",
    "Yaśastilaka",
    "Arthaśāstra",
    "Rājataraṅgiṇī",
    "Chamba",
    "SITI",
    "ASLV",
    "CITD",
    "HRS",
    "JNSI",
    "JBBRAS",
    "JBORS",
    "JAHRS",
    "IHQ",
    "JAS",
    "PTS",
    "P. T. S.",
    "Proc. IHC",
    "CII",
    "SII",
    "EI",
    "IE",
    "IA",
    "LP",
    "BL",
    "LL",
    "ML",
    "HD",
    "HA",
    "PJS",
    "ZDMG",
]
REF_ABBREVIATIONS.sort(key=len, reverse=True)

LATIN_ABBRS = [
    'cf.', 'etc.', 'i. e.', 'q. v.', 'e. g.', 'viz.', 's. v.',
    'Cf.', 'Etc.',
]
LATIN_ABBRS.sort(key=len, reverse=True)


def cleanup_ab_line(line: str) -> str:
    line = re.sub(r'(?<!\w)([GD])({%)', r'\2', line)
    line = re.sub(r'\$({%)', r'\1', line)
    line = line.replace('<LEND?', '<LEND>')
    line = line.rstrip()
    return line


def process_cdsl(lines):
    out = []
    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip('\n')
        if stripped.startswith('<L>'):
            l_tag = stripped
            i += 1
            # Collect entry: groups of text separated by <div n="P">
            text_groups = []  # list of (prefix, [content_parts])
            current_prefix = ''
            current_parts = []
            has_content = False

            def flush_group():
                nonlocal has_content
                if current_parts or has_content:
                    text_groups.append((current_prefix, list(current_parts)))
                current_parts.clear()
                has_content = False

            while i < len(lines):
                next_line = lines[i].rstrip('\n')
                if next_line.startswith('<L>'):
                    break
                if next_line.startswith('<LEND') or next_line.startswith('<LEND?'):
                    l_end = next_line
                    i += 1
                    break
                if next_line.startswith('%***') or next_line == '':
                    i += 1
                    continue
                if '<div n="P">' in next_line:
                    flush_group()
                    current_prefix = next_line.replace('<div n="P">', '    <P>¦ ', 1)
                    i += 1
                    continue
                current_parts.append(next_line)
                has_content = True
                i += 1
            else:
                l_end = '<LEND>'

            flush_group()

            # Process each group
            processed = []
            for prefix, parts in text_groups:
                joined = join_content(parts) if parts else ''
                text = prefix + (' ' + joined if prefix and joined else joined)
                text = unwrap_ref_abbrs_from_dev(text)
                text = wrap_refs(text)
                text = wrap_latin_abbrs(text)
                text = fix_punctuation_inside_dev(text)
                text = re.sub(r' +', ' ', text)
                text = text.strip()
                if text:
                    processed.append(text)

            out.append(l_tag)
            for line in processed:
                out.append(line)
            out.append(l_end)
            out.append('')
        else:
            i += 1
    return out


def join_content(parts):
    if not parts:
        return ''
    # First pass: merge {%...%} continuations across lines
    merged_parts = []
    i = 0
    while i < len(parts):
        part = parts[i]
        if part.endswith('%}') and i + 1 < len(parts) and parts[i + 1].startswith('{%'):
            merged = part[:-2] + parts[i + 1][2:]
            i += 2
            while i < len(parts) and merged.endswith('%}') and parts[i].startswith('{%'):
                merged = merged[:-2] + parts[i][2:]
                i += 1
            merged_parts.append(merged)
        else:
            merged_parts.append(part)
            i += 1
    # Second pass: handle hyphen at line end (soft hyphenation)
    # strip '-' and join tight only if next part starts with lowercase
    joined = []
    i = 0
    while i < len(merged_parts):
        part = merged_parts[i]
        if part.endswith('-') and i + 1 < len(merged_parts) and merged_parts[i + 1] and merged_parts[i + 1][0].islower():
            joined.append(part[:-1] + merged_parts[i + 1])
            i += 2
        else:
            joined.append(part)
            i += 1
    return ' '.join(joined)


def _norm(s):
    return s.lower().replace(' ', '').rstrip('.,;:!?()[]')


ALL_ABBRS = REF_ABBREVIATIONS + LATIN_ABBRS

def unwrap_ref_abbrs_from_dev(text):
    def replace_dev_wrapper(m):
        inner = m.group(1).strip()
        inner_norm = _norm(inner)
        for abbr in ALL_ABBRS:
            abbr_norm = _norm(abbr)
            if inner_norm == abbr_norm:
                return inner
        return m.group(0)
    return re.sub(r'\{%([^}%]+)%\}', replace_dev_wrapper, text)


def _wrap_abbr_inner(inner):
    for abbr in REF_ABBREVIATIONS:
        escaped = re.escape(abbr)
        inner = re.sub(
            r'(?<!<ls>)' + escaped + r'(?!</ls>)',
            f'<ls>{abbr}</ls>',
            inner
        )
        # Also try without spaces (for joined abbreviations like Ep.Ind.)
        abbr_nospace = abbr.replace(' ', r'\s*')
        if abbr_nospace != escaped:
            inner = re.sub(
                r'(?<!<ls>)' + abbr_nospace + r'(?!</ls>)',
                f'<ls>{abbr}</ls>',
                inner
            )
    return inner


def wrap_refs(text):
    text = re.sub(r'\(([^()]*)\)', lambda m: '(' + _wrap_abbr_inner(m.group(1)) + ')', text)
    text = _wrap_abbr_inner(text)
    return text


def wrap_latin_abbrs(text):
    for abbr in LATIN_ABBRS:
        escaped = re.escape(abbr)
        text = re.sub(
            r'(?<!<ab>)' + escaped + r'(?!</ls>)(?!</ab>)',
            f'<ab>{abbr}</ab>',
            text
        )
    return text


def fix_punctuation_inside_dev(text):
    text = re.sub(r'\{%([^}%]*?)([.,;:!?]+)%\}', r'{%\1%}\2', text)
    return text


def clean_whitespace(text):
    leading = len(text) - len(text.lstrip())
    indent = text[:leading]
    rest = re.sub(r' +', ' ', text[leading:].rstrip())
    return indent + rest


with open(AB_IN, 'r', encoding='utf-8') as f:
    ab_lines = f.readlines()

ab_out = [cleanup_ab_line(l) for l in ab_lines]

with open(AB_OUT, 'w', encoding='utf-8') as f:
    for line in ab_out:
        f.write(line + '\n')
print(f"Written {AB_OUT} ({len(ab_out)} lines)")

with open(CDSL_IN, 'r', encoding='utf-8') as f:
    cdsl_lines = f.readlines()

start_idx = 0
for i, line in enumerate(cdsl_lines):
    if line.startswith('<L>'):
        start_idx = i
        break

cdsl_body = cdsl_lines[start_idx:]
cdsl_out = process_cdsl(cdsl_body)
# Prepend AB-style header
cdsl_out[0:0] = [';', '; ENTRIES', ';']

with open(CDSL_OUT, 'w', encoding='utf-8') as f:
    for line in cdsl_out:
        f.write(line + '\n')
print(f"Written {CDSL_OUT} ({len(cdsl_out)} lines)")
print("Done.")
