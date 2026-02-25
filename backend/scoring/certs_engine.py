from __future__ import annotations
"""
Certifications Scoring Engine
Evaluates certifications based on tier ranking, relevance, quantity, and diversity.
Uses a pre-trained database of 200+ certifications ranked into tiers.
"""

import json
import os
import io
import re
from difflib import SequenceMatcher

try:
    from pdfminer.high_level import extract_text
    from pdfminer.layout import LAParams
    PDF_OK = True
except ImportError:
    PDF_OK = False

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_certs_database():
    with open(os.path.join(DATA_DIR, "certs_database.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def _fuzzy_match_cert(cert_name: str, db: dict):
    """Find the best matching certification in the database using fuzzy matching."""
    cert_lower = cert_name.lower().strip()
    best_match = None
    best_score = 0
    best_tier = None

    for tier_name, tier_info in db["tiers"].items():
        for known_cert in tier_info["certifications"]:
            # Exact match
            if known_cert.lower() == cert_lower:
                return {
                    "matched_name": known_cert,
                    "tier": tier_name,
                    "tier_label": tier_info["label"],
                    "tier_value": tier_info["value"],
                    "match_confidence": 1.0
                }
            # Fuzzy match
            ratio = SequenceMatcher(None, cert_lower, known_cert.lower()).ratio()
            # Also check if the cert name is contained in the known cert
            if cert_lower in known_cert.lower() or known_cert.lower() in cert_lower:
                ratio = max(ratio, 0.85)
            if ratio > best_score:
                best_score = ratio
                best_match = known_cert
                best_tier = tier_name

    if best_score >= 0.6:
        tier_info = db["tiers"][best_tier]
        return {
            "matched_name": best_match,
            "tier": best_tier,
            "tier_label": tier_info["label"],
            "tier_value": tier_info["value"],
            "match_confidence": round(best_score, 2)
        }

    # Unknown cert defaults to bronze tier
    return {
        "matched_name": cert_name,
        "tier": "bronze",
        "tier_label": "Bronze - Entry Level / MOOC",
        "tier_value": 3,
        "match_confidence": 0
    }


def get_all_certifications():
    """Return all certifications organized by tier for reference."""
    db = load_certs_database()
    result = {}
    for tier_name, tier_info in db["tiers"].items():
        result[tier_name] = {
            "label": tier_info["label"],
            "value": tier_info["value"],
            "certifications": tier_info["certifications"]
        }
    return result


def scan_certificate_file(file_bytes: bytes, filename: str = "") -> dict:
    """Extract text from an uploaded certificate file (PDF) and identify the certification."""
    text = ""
    if PDF_OK:
        try:
            text = extract_text(io.BytesIO(file_bytes), laparams=LAParams())
        except Exception:
            pass

    if not text.strip():
        return {
            "identified": False,
            "cert_name": "",
            "error": "Could not extract text from file. Ensure it is a text-based PDF.",
            "match": None,
        }

    db = load_certs_database()
    text_lower = text.lower()

    # Try to match against all known certifications
    best_match = None
    best_score = 0
    for tier_name, tier_info in db["tiers"].items():
        for cert_name in tier_info["certifications"]:
            cert_lower = cert_name.lower()
            # Check if cert name keywords appear in extracted text
            words = [w for w in cert_lower.split() if len(w) > 2]
            matches = sum(1 for w in words if w in text_lower)
            ratio = matches / max(len(words), 1)
            # Also try full string matching
            seq_ratio = SequenceMatcher(None, cert_lower, text_lower[:500]).ratio()
            score = max(ratio, seq_ratio * 1.5)
            if score > best_score:
                best_score = score
                best_match = {
                    "cert_name": cert_name,
                    "tier": tier_name,
                    "tier_label": tier_info["label"],
                    "tier_value": tier_info["value"],
                    "confidence": round(min(score, 1.0), 2),
                }

    if best_match and best_score >= 0.3:
        return {"identified": True, "cert_name": best_match["cert_name"],
                "match": best_match, "extracted_text_preview": text[:300].strip()}
    else:
        # Try to extract a likely cert name from the text
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 5]
        likely_name = lines[0] if lines else filename
        match = _fuzzy_match_cert(likely_name, db)
        return {"identified": True, "cert_name": likely_name, "match": match,
                "extracted_text_preview": text[:300].strip(), "auto_detected": True}


def calculate_certs_score(certifications: list[dict]) -> dict:
    """
    Calculate certifications score based on:
    1. Tier quality - weighted average of certification tiers (50%)
    2. Quantity bonus - having multiple certifications (20%)
    3. Tier diversity - having certs across different tiers (15%)
    4. Premium cert bonus - having platinum/gold certs (15%)

    Each cert is: {"name": "AWS Solutions Architect", "issuer": "Amazon", "year": 2024}
    """
    if not certifications:
        return {
            "score": 0,
            "breakdown": {
                "tier_quality": 0,
                "quantity_bonus": 0,
                "tier_diversity": 0,
                "premium_bonus": 0
            },
            "cert_details": [],
            "suggestions": ["Obtain industry-recognized certifications to boost your score."]
        }

    db = load_certs_database()

    cert_details = []
    tier_values = []
    tiers_found = set()
    premium_count = 0

    for cert in certifications:
        cert_name = cert.get("name", "")
        if not cert_name:
            continue
        match = _fuzzy_match_cert(cert_name, db)
        cert_details.append({
            "input_name": cert_name,
            "issuer": cert.get("issuer", ""),
            "year": cert.get("year", ""),
            **match
        })
        tier_values.append(match["tier_value"])
        tiers_found.add(match["tier"])
        if match["tier"] in ("platinum", "gold"):
            premium_count += 1

    if not tier_values:
        return {
            "score": 0,
            "breakdown": {"tier_quality": 0, "quantity_bonus": 0, "tier_diversity": 0, "premium_bonus": 0},
            "cert_details": [],
            "suggestions": ["Add valid certification names to get scored."]
        }

    # 1. Tier Quality Score (avg tier value normalized to 100)
    avg_tier = sum(tier_values) / len(tier_values)
    tier_quality = min(100, (avg_tier / 10.0) * 100)

    # 2. Quantity Bonus (logarithmic, optimal around 5-8 certs)
    qty = len(tier_values)
    if qty >= 8:
        quantity_bonus = 100
    elif qty >= 5:
        quantity_bonus = 85
    elif qty >= 3:
        quantity_bonus = 70
    elif qty >= 2:
        quantity_bonus = 55
    else:
        quantity_bonus = 35

    # 3. Tier Diversity
    diversity = (len(tiers_found) / 4.0) * 100  # 4 possible tiers
    tier_diversity = min(100, diversity)

    # 4. Premium Certification Bonus
    if premium_count >= 3:
        premium_bonus = 100
    elif premium_count >= 2:
        premium_bonus = 80
    elif premium_count >= 1:
        premium_bonus = 55
    else:
        premium_bonus = 15

    # Weighted final score
    final_score = (
        tier_quality * 0.50 +
        quantity_bonus * 0.20 +
        tier_diversity * 0.15 +
        premium_bonus * 0.15
    )
    final_score = min(100, round(final_score, 1))

    # Generate suggestions
    suggestions = []
    if premium_count == 0:
        suggestions.append("Pursue a Gold or Platinum-tier certification like AWS Solutions Architect or Google Cloud Professional.")
    if qty < 3:
        suggestions.append("Aim for at least 3-5 certifications to demonstrate commitment to learning.")
    if "platinum" not in tiers_found:
        suggestions.append("A Platinum-tier certification (e.g., AWS Pro, CISSP, CKA) would significantly boost your profile.")
    if avg_tier < 6:
        suggestions.append("Focus on higher-tier certifications rather than accumulating entry-level ones.")
    if len(tiers_found) < 2:
        suggestions.append("Diversify your certifications across different tiers and domains.")

    return {
        "score": final_score,
        "breakdown": {
            "tier_quality": round(tier_quality, 1),
            "quantity_bonus": round(quantity_bonus, 1),
            "tier_diversity": round(tier_diversity, 1),
            "premium_bonus": round(premium_bonus, 1)
        },
        "cert_details": cert_details,
        "total_certs": len(tier_values),
        "suggestions": suggestions
    }
