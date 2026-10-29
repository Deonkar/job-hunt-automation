"""Build a tailored resume by applying a small JSON patch to a copy of the master .docx.

The patch can only re-order and select content that already exists: bullet text comes
from the bullet bank, skills must be a permutation of the master's skill lines. Formatting
is never generated, only cloned from the master, so every output looks identical to it.

Usage: py -3 build_resume.py PATCH.json OUT.docx [--country countries/<code>.json]
       [--master data/master.docx] [--bank data/bullets.json] [--profile data/profile.json]
"""
import argparse
import copy
import json
import os
import re

import docx
from docx.oxml.ns import qn
from docx.shared import Emu, Inches, Mm
from docx.text.run import Run

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
PATCH_KEYS = {"title", "summary", "skills_order", "skills_items", "experience",
              "projects", "projects_order", "internships"}
HEADINGS = ("Summary", "Skills", "Experience", "Internships", "Projects", "Education")


def load_bank(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_markup(text):
    """'a **b** c' -> [('a ', False), ('b', True), (' c', False)]"""
    parts = text.split("**")
    return [(s, i % 2 == 1) for i, s in enumerate(parts) if s]


def resolve(entries, where, ref):
    key, _, alt = ref.partition(".")
    entry = entries.get(key)
    if entry is None or (alt or "base") not in entry:
        raise ValueError(f"unknown bullet {where}:{ref}")
    return entry[alt or "base"]


def _is_numbered(p):
    return p._p.find(".//" + W + "numPr") is not None


def _heading_index(doc, name):
    for i, p in enumerate(doc.paragraphs):
        if p.text == name and p.runs and all(r.bold for r in p.runs):
            return i
    raise ValueError(f"heading {name!r} not found in master")


def _is_heading(p):
    return p.text in HEADINGS and p.runs and all(r.bold for r in p.runs)


def _section(doc, name):
    ps = doc.paragraphs
    start = _heading_index(doc, name)
    end = next((i for i in range(start + 1, len(ps)) if _is_heading(ps[i])), len(ps))
    return ps[start + 1:end]


def blocks(doc, heading, keys):
    """One block per role/project (header lines, then its bullets), matched to keys in master order."""
    groups = []
    for p in _section(doc, heading):
        if not groups or (not _is_numbered(p) and _is_numbered(groups[-1][-1])):
            groups.append([])
        groups[-1].append(p)
    if len(groups) != len(keys):
        raise ValueError(f"{heading}: master has {len(groups)} blocks but bullets.json lists {len(keys)}; "
                         "re-run make_master.py")
    return dict(zip(keys, groups))


def _new_run(p, rpr, text, bold):
    r = p._p.makeelement(qn("w:r"), {})
    if rpr is not None:
        rpr = copy.deepcopy(rpr)
        for tag in ("w:b", "w:bCs"):
            for el in rpr.findall(qn(tag)):
                rpr.remove(el)
        if bold:
            # w:b must follow w:rStyle/w:rFonts to keep the schema order Word expects
            pos = sum(1 for c in rpr if c.tag in (qn("w:rStyle"), qn("w:rFonts")))
            rpr.insert(pos, rpr.makeelement(qn("w:b"), {}))
        r.append(rpr)
    elif bold:
        rp = r.makeelement(qn("w:rPr"), {})
        rp.append(rp.makeelement(qn("w:b"), {}))
        r.append(rp)
    Run(r, p).text = text
    return r


def _rpr(run):
    return run._r.find(qn("w:rPr"))


def set_markup(p, markup):
    """Replace a paragraph's runs with markup, cloning the master's plain-run formatting."""
    runs = p.runs
    template = next((r for r in runs if not r.bold), runs[0]) if runs else None
    rpr = _rpr(template) if template is not None else None
    for r in runs:
        p._p.remove(r._r)
    for text, bold in parse_markup(markup):
        p._p.append(_new_run(p, rpr, text, bold))


def set_tabbed(p, left_markup, right_text):
    """Role line: left markup, a tab, then right-aligned text in the master's right-run style."""
    runs = p.runs
    left, tab, right = _rpr(runs[0]), _rpr(runs[1]), _rpr(runs[-1])
    for r in runs:
        p._p.remove(r._r)
    for text, bold in parse_markup(left_markup):
        p._p.append(_new_run(p, left, text, bold))
    p._p.append(_new_run(p, tab, "\t", False))
    p._p.append(_new_run(p, right, right_text, False))


def _split_top_level(s):
    items, depth, cur = [], 0, ""
    for ch in s:
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            items.append(cur.strip())
            cur = ""
        else:
            cur += ch
    items.append(cur.strip())
    return items


def _replace_bullets(doc, old, markups):
    if not old:
        raise ValueError("no bullets to use as a template")
    template = old[0]._p
    for m in markups:
        el = copy.deepcopy(template)
        template.addprevious(el)
        set_markup(docx.text.paragraph.Paragraph(el, old[0]._parent), m)
    for p in old:
        p._p.getparent().remove(p._p)


def _visible_contact_links(doc):
    end = _heading_index(doc, "Summary")
    for p in doc.paragraphs[:end]:
        for h in p._p.iter(W + "hyperlink"):
            rid = h.get(qn("r:id"))
            if not rid:
                continue
            url = doc.part.rels[rid].target_ref
            label = re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
            ts = list(h.iter(W + "t"))
            if ts:
                ts[0].text = label
                for t in ts[1:]:
                    t.text = ""


def _apply_skills(doc, order, items):
    start, end = _heading_index(doc, "Skills"), _heading_index(doc, "Experience")
    lines = {}
    for p in doc.paragraphs[start + 1:end]:
        label, _, rest = p.text.partition(": ")
        lines[label] = (p, _split_top_level(rest))
    for label, new in (items or {}).items():
        if label not in lines:
            raise ValueError(f"unknown skills line {label!r}")
        old = lines[label][1]
        if sorted(new) != sorted(old):
            raise ValueError(f"skills {label!r} must re-order the master's items exactly: "
                             f"extra={sorted(set(new) - set(old))} missing={sorted(set(old) - set(new))}")
        set_markup(lines[label][0], f"**{label}: **" + ", ".join(new))
    if order:
        unknown = [l for l in order if l not in lines]
        if unknown:
            raise ValueError(f"unknown skills lines {unknown}")
        ordered = list(order) + [l for l in lines if l not in order]
        anchor = doc.paragraphs[start]._p
        for label in ordered:
            el = lines[label][0]._p
            anchor.addnext(el)
            anchor = el


def _add_internships(doc, bank):
    exp = doc.paragraphs[_heading_index(doc, "Experience")]
    role_line = next(p for p in doc.paragraphs[_heading_index(doc, "Experience") + 1:]
                     if "\t" in p.text and not any(r.bold for r in p.runs))
    after = "Projects" if any(_is_heading(p) and p.text == "Projects" for p in doc.paragraphs) else "Education"
    projects = doc.paragraphs[_heading_index(doc, after)]._p
    head = copy.deepcopy(exp._p)
    projects.addprevious(head)
    hp = docx.text.paragraph.Paragraph(head, exp._parent)
    hp.runs[0].text = "Internships"
    for r in hp.runs[1:]:
        head.remove(r._r)
    for it in bank["internships"]:
        el = copy.deepcopy(role_line._p)
        projects.addprevious(el)
        left = f"**{it['title']}**, {it['company']}" + (f" – {it['note']}" if it.get("note") else "")
        set_tabbed(docx.text.paragraph.Paragraph(el, exp._parent), left, it["dates"])


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MM_YYYY = [[rf"\b{m} (\d{{4}})\b", rf"{i:02d}/\1"] for i, m in enumerate(MONTHS, 1)]
COUNTRY_KEYS = {"page", "replace", "replace_regex", "location_suffix", "work_auth",
                "spoken_languages", "closing_line", "base_variant", "name"}
PAGES = {"A4": (Mm(210), Mm(297)), "Letter": (Inches(8.5), Inches(11))}


def _replace_in_runs(doc, pairs, regex):
    for p in doc.paragraphs:
        for old, new in pairs:
            for r in p.runs:
                if regex:
                    r.text = re.sub(old, new, r.text)
                elif old in r.text:
                    r.text = r.text.replace(old, new)
            if re.search(old, p.text) if regex else old in p.text:
                raise ValueError(f"{old!r} spans formatting runs in {p.text[:60]!r}; "
                                 "replace a shorter phrase that sits inside one run")


def _clone_after(anchor, source, markup):
    el = copy.deepcopy(source._p)
    anchor._p.addnext(el)
    p = docx.text.paragraph.Paragraph(el, source._parent)
    set_markup(p, markup)
    return p


def apply_country(doc, country, spoken=None, location=None):
    """Format layer for a target country: page size, spelling/currency/date wording,
    relocation and work-permit lines, spoken languages, closing line."""
    unknown = {k for k in country if not k.startswith("_")} - COUNTRY_KEYS
    if unknown:
        raise ValueError(f"unknown country keys {sorted(unknown)}")
    if "page" in country:
        # keep the master's text width so line breaks (and the one-page fit) don't shift
        s = doc.sections[0]
        text_width = s.page_width - s.left_margin - s.right_margin
        s.page_width, s.page_height = PAGES[country["page"]]
        s.left_margin = s.right_margin = Emu((s.page_width - text_width) // 2)
    _replace_in_runs(doc, country.get("replace", []), regex=False)
    _replace_in_runs(doc, country.get("replace_regex", []), regex=True)
    summary = _heading_index(doc, "Summary")
    if "location_suffix" in country:
        contact = doc.paragraphs[2]
        run = next((r for r in contact.runs if location and r.text.strip() == location), None)
        if run is None:
            raise ValueError(f"location {location!r} (profile.json) not found as its own run in the contact line")
        run.text += country["location_suffix"]
    if "work_auth" in country:
        last = doc.paragraphs[summary - 1]
        line = _clone_after(last, doc.paragraphs[2], country["work_auth"])
        # the header's gap belongs below the header block, i.e. below the new line
        line.paragraph_format.space_after = last.paragraph_format.space_after
        last.paragraph_format.space_after = Emu(0)
    if country.get("spoken_languages"):
        if spoken:
            exp = _heading_index(doc, "Experience")
            _clone_after(doc.paragraphs[exp - 1], doc.paragraphs[exp - 1],
                         "**Spoken languages: **" + ", ".join(spoken))
        else:
            print("warning: country wants spoken languages but profile.json has none")
    if "closing_line" in country:
        _clone_after(doc.paragraphs[-1], doc.paragraphs[-1], country["closing_line"])


def _plain_punctuation(doc):
    """No em/en dashes or arrows (they parse badly in ATS); hyphen and 'to' instead."""
    for p in doc.paragraphs:
        for r in p.runs:
            if re.search("[–—→]", r.text):
                r.text = re.sub(r"\s*→\s*", " to ", r.text).replace("–", "-").replace("—", "-")


def build(master, bank, patch, out, country=None, spoken=None, location=None):
    unknown = {k for k in patch if not k.startswith("_")} - PATCH_KEYS
    if unknown:
        raise ValueError(f"unknown patch keys {sorted(unknown)}")
    doc = docx.Document(master)
    _visible_contact_links(doc)
    if "title" in patch:
        set_markup(doc.paragraphs[1], patch["title"])
    if "summary" in patch:
        set_markup(doc.paragraphs[_heading_index(doc, "Summary") + 1], patch["summary"])
    if "skills_order" in patch or "skills_items" in patch:
        _apply_skills(doc, patch.get("skills_order"), patch.get("skills_items"))
    for section, heading in (("experience", "Experience"), ("projects", "Projects")):
        if patch.get(section):
            found = blocks(doc, heading, list(bank[section]))
            for key, refs in patch[section].items():
                if key not in found:
                    raise ValueError(f"unknown {section} key {key!r}; known: {sorted(found)}")
                markups = [resolve(bank[section][key], f"{section}.{key}", ref) for ref in refs]
                _replace_bullets(doc, [p for p in found[key] if _is_numbered(p)], markups)
    if "projects_order" in patch:
        found = blocks(doc, "Projects", list(bank["projects"]))
        if sorted(patch["projects_order"]) != sorted(found):
            raise ValueError(f"projects_order must list {sorted(found)}")
        edu = doc.paragraphs[_heading_index(doc, "Education")]._p
        for key in patch["projects_order"]:
            for p in found[key]:
                edu.addprevious(p._p)
    if patch.get("internships"):
        _add_internships(doc, bank)
    if country:
        apply_country(doc, country, spoken, location)
    _plain_punctuation(doc)
    doc.save(out)
    return out


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("patch")
    ap.add_argument("out")
    ap.add_argument("--master", default=os.path.join(root, "data", "master.docx"))
    ap.add_argument("--bank", default=os.path.join(root, "data", "bullets.json"))
    ap.add_argument("--country", help="countries/<code>.json format layer")
    ap.add_argument("--profile", default=os.path.join(root, "data", "profile.json"))
    a = ap.parse_args()
    profile = load_bank(a.profile)
    country = load_bank(a.country) if a.country else None
    print(build(a.master, load_bank(a.bank), load_bank(a.patch), a.out, country=country,
                spoken=profile.get("spoken_languages"), location=profile.get("location")))


if __name__ == "__main__":
    main()
