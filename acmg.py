"""ACMG/AMP 2015 combination logic for research/demo use.

This module combines *already assessed* evidence criteria. It does not decide
whether a biological observation satisfies a criterion. That assessment must be
made by a qualified user or a separately validated evidence rule.
"""
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List, Dict

PATHOGENIC_PREFIXES = {"PVS", "PS", "PM", "PP"}
BENIGN_PREFIXES = {"BA", "BS", "BP"}


def strength(code: str) -> str:
    code = code.strip().upper()
    if code.startswith("PVS"):
        return "very_strong"
    if code.startswith("PS"):
        return "strong_pathogenic"
    if code.startswith("PM"):
        return "moderate_pathogenic"
    if code.startswith("PP"):
        return "supporting_pathogenic"
    if code.startswith("BA"):
        return "standalone_benign"
    if code.startswith("BS"):
        return "strong_benign"
    if code.startswith("BP"):
        return "supporting_benign"
    return "unknown"


def _has_pathogenic(codes: Iterable[str]) -> bool:
    return any(c.startswith(tuple(PATHOGENIC_PREFIXES)) for c in codes)


def _has_benign(codes: Iterable[str]) -> bool:
    return any(c.startswith(tuple(BENIGN_PREFIXES)) for c in codes)


def classify(codes: Iterable[str]) -> Dict:
    """Combine assessed ACMG/AMP criteria using the 2015 categorical rules."""
    codes = sorted({c.strip().upper() for c in codes if c and c.strip()})
    counts = Counter(strength(c) for c in codes)
    pvs = counts["very_strong"]
    ps = counts["strong_pathogenic"]
    pm = counts["moderate_pathogenic"]
    pp = counts["supporting_pathogenic"]
    ba = counts["standalone_benign"]
    bs = counts["strong_benign"]
    bp = counts["supporting_benign"]

    conflicting = _has_pathogenic(codes) and _has_benign(codes)
    if conflicting:
        return {
            "classification": "Variant of uncertain significance",
            "reason": "Conflicting pathogenic and benign evidence is present.",
            "codes": codes,
            "counts": dict(counts),
        }

    # Benign combinations
    if ba >= 1:
        result = "Benign"
        reason = "At least one stand-alone benign criterion (BA) is present."
    elif bs >= 2:
        result = "Benign"
        reason = "At least two strong benign criteria (BS) are present."
    elif (bs >= 1 and bp >= 1) or bp >= 2:
        result = "Likely benign"
        reason = "The ACMG/AMP likely-benign evidence combination is satisfied."
    # Pathogenic combinations
    elif pvs >= 1 and (ps >= 1 or pm >= 2 or (pm >= 1 and pp >= 1) or pp >= 2):
        result = "Pathogenic"
        reason = "A very-strong pathogenic criterion plus a pathogenic supporting combination is present."
    elif ps >= 2:
        result = "Pathogenic"
        reason = "At least two strong pathogenic criteria are present."
    elif ps >= 1 and pm >= 3:
        result = "Pathogenic"
        reason = "One strong plus at least three moderate pathogenic criteria are present."
    elif ps >= 1 and pm >= 2 and pp >= 2:
        result = "Pathogenic"
        reason = "One strong, at least two moderate, and at least two supporting pathogenic criteria are present."
    elif ps >= 1 and pm >= 1 and pp >= 4:
        result = "Pathogenic"
        reason = "One strong, one moderate, and at least four supporting pathogenic criteria are present."
    elif pvs >= 1 and pm >= 1:
        result = "Likely pathogenic"
        reason = "One very-strong and one moderate pathogenic criterion are present."
    elif ps >= 1 and 1 <= pm <= 2:
        result = "Likely pathogenic"
        reason = "One strong plus one or two moderate pathogenic criteria are present."
    elif ps >= 1 and pp >= 2:
        result = "Likely pathogenic"
        reason = "One strong plus at least two supporting pathogenic criteria are present."
    elif pm >= 3:
        result = "Likely pathogenic"
        reason = "At least three moderate pathogenic criteria are present."
    elif pm >= 2 and pp >= 2:
        result = "Likely pathogenic"
        reason = "At least two moderate plus at least two supporting pathogenic criteria are present."
    elif pm >= 1 and pp >= 4:
        result = "Likely pathogenic"
        reason = "One moderate plus at least four supporting pathogenic criteria are present."
    else:
        result = "Variant of uncertain significance"
        reason = "The evidence combination does not satisfy a pathogenic, likely pathogenic, benign, or likely benign rule."

    return {"classification": result, "reason": reason, "codes": codes, "counts": dict(counts)}
