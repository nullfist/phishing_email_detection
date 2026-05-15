"""
analyzer.py – Phishing Detection Intelligence Engine
  Integrates preprocessing, heuristic scoring, and simulated ML verdict.
"""

import math
from typing import Dict, List
from preprocessor import preprocess

# ── Keywords frequently used in phishing ─────────────────────────────────────
URGENCY_KEYWORDS = ["urgent", "immediately", "action required", "suspended", "compromised", "verify"]
FINANCIAL_KEYWORDS = ["payment", "invoice", "bank", "transfer", "refund", "paypal", "bitcoin"]
THREAT_KEYWORDS = ["illegal", "lawsuit", "police", "court", "unauthorized"]

class PhishingAnalyzer:
    def __init__(self):
        self.version = "1.0.0"

    def calculate_score(self, data: Dict) -> Dict:
        """
        Calculates a weighted threat score based on extracted features.
        Score range: 0 - 100
        """
        score = 0
        indicators = []

        # 1. URL Analysis
        url_count = data.get("url_count", 0)
        if url_count > 0:
            score += min(url_count * 10, 30)
            indicators.append(f"Contains {url_count} URL(s)")
            
            # Check for suspicious TLDs or patterns in URLs (simulated)
            for url in data.get("urls", []):
                if any(x in url for x in ["bit.ly", "tinyurl", ".xyz", ".top"]):
                    score += 15
                    indicators.append("Shortened or suspicious URL detected")
                    break

        # 2. Text Analysis (Urgency/Threat)
        tokens = data.get("tokens", [])
        urgency_hits = sum(1 for t in tokens if t in URGENCY_KEYWORDS)
        if urgency_hits > 0:
            score += min(urgency_hits * 10, 20)
            indicators.append("Urgent language detected")

        financial_hits = sum(1 for t in tokens if t in FINANCIAL_KEYWORDS)
        if financial_hits > 0:
            score += 10
            indicators.append("Financial bait keywords detected")

        # 3. Behavioral / Header Indicators
        if data.get("sender_mismatch"):
            score += 25
            indicators.append("Sender / Reply-To mismatch (potential spoofing)")

        if data.get("obfuscated"):
            score += 20
            indicators.append("Invisible/Obfuscated characters detected")

        # 4. CAP the score
        score = min(score, 100)

        # 5. Determine Verdict
        if score >= 75:
            verdict = "CRITICAL PHISHING"
        elif score >= 50:
            verdict = "HIGH RISK"
        elif score >= 25:
            verdict = "SUSPICIOUS"
        else:
            verdict = "SAFE"

        return {
            "score": score,
            "verdict": verdict,
            "indicators": indicators,
            "confidence": f"{max(score, 20)}%"
        }

    def analyze_email(self, raw_content: str) -> Dict:
        """Full analysis pipeline."""
        extracted = preprocess(raw_content)
        intelligence = self.calculate_score(extracted)
        
        return {
            "analysis": intelligence,
            "metadata": extracted
        }

if __name__ == "__main__":
    test_email = "Subject: Urgent Security Alert\n\nYour account was accessed from a new device. Please verify your identity immediately at http://bit.ly/fake-login"
    engine = PhishingAnalyzer()
    result = engine.analyze_email(test_email)
    print(f"Verdict: {result['analysis']['verdict']}")
    print(f"Score: {result['analysis']['score']}")
    print(f"Indicators: {result['analysis']['indicators']}")
