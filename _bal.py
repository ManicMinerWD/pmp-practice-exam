#!/usr/bin/env python3
"""Length-balancing helper for exam generators.

Goal: defeat the 'pick the longest answer' cheat by making all four options
similar length, so correctness cannot be inferred from length.

Approach: for each question, extend the three DISTRACTORS (never the correct
answer) with natural, truthful, WRONG-action qualifiers drawn from a bank,
until each distractor is within ~85-105% of the correct answer's length.
The correct answer stays correct; distractors stay wrong. We vary per option
so the correct one is sometimes shorter, sometimes longer, sometimes tied.
"""
import random

# Short natural qualifiers (wrong-action flavored) used to lengthen distractors
# finely. Kept brief so extension does not overshoot the target length.
QUAL = [
    " at once",
    " to save time",
    " without review",
    " to look decisive",
    " before checking",
    " and hope",
    " to avoid friction",
    " without telling them",
    " as a shortcut",
    " and move on",
    " to keep peace",
    " without analysis",
    " and assume",
    " to close it out",
    " and skip the step",
    " before confirming",
    " to reduce noise",
    " and defer it",
    " to stay safe",
    " and note it",
]

def _truncate(text, target):
    """Trim `text` to at most `target` chars, cutting at a space near target so the
    result stays a clean phrase. If already short, return as-is."""
    if len(text) <= target:
        return text
    cut = text.rfind(" ", 0, target)
    if cut > 15:
        return text[:cut].rstrip()
    return text[:target].rstrip()

def _extend(text, target):
    """Extend `text` with short qualifiers until its length is at least `target`."""
    t = text
    i = 0
    while len(t) < target and i < len(QUAL):
        q = QUAL[(i * 7 + len(t)) % len(QUAL)]
        t = t.rstrip() + q
        i += 1
    return t

def balance(Q_raw, seed=2026):
    """Balance option lengths so correctness cannot be inferred from length.
    Accepts two tuple shapes:
      - 8-tuple: (dom, q, o0, o1, o2, o3, ai, exp)
      - 5-tuple: (dom, q, [o0,o1,o2,o3], ai, exp)
    Returns the same shape with distractors extended (correct answer unchanged)."""
    out = []
    for idx_, item in enumerate(Q_raw):
        rnd = random.Random(seed + idx_)
        if len(item) == 8:
            dom, q, o0, o1, o2, o3, ai, exp = item
            opts = [o0, o1, o2, o3]
            new_opts = _balance_opts(opts, ai, rnd)
            out.append((dom, q, new_opts[0], new_opts[1], new_opts[2], new_opts[3], ai, exp))
        elif len(item) == 5:
            dom, q, opts, ai, exp = item
            new_opts = _balance_opts(list(opts), ai, rnd)
            out.append((dom, q, new_opts, ai, exp))
        else:
            out.append(item)
    return out

def _balance_opts(opts, ai, rnd):
    correct = opts[ai]
    clen = len(correct)
    new_opts = list(opts)
    for j in range(4):
        if j == ai:
            continue
        dist = new_opts[j]
        desired = int(clen * rnd.uniform(0.6, 1.3))
        if len(dist) < desired:
            new_opts[j] = _extend(dist, desired)
    return new_opts
