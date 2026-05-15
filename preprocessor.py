"""
preprocessor.py – Email Preprocessing Pipeline
  - HTML stripping
  - URL extraction
  - Tokenisation, lowercasing, stopword removal
  - Header parsing (From, Reply-To, Subject)
  - Obfuscation detection (unicode tricks, zero-width chars)
"""

import re
import email
from email import policy
from typing import Dict, List

try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

try:
    import nltk
    _stopwords = set()
    try:
        from nltk.corpus import stopwords as _sw_corpus
        from nltk.stem import PorterStemmer
        try:
            _stopwords = set(_sw_corpus.words("english"))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            _stopwords = set(_sw_corpus.words("english"))
    except Exception:
        pass
    _stemmer = PorterStemmer()
    _HAS_NLTK = True
except ImportError:
    _HAS_NLTK = False
    _stemmer = None
    _stopwords = set()

# ── Regex patterns ────────────────────────────────────────────────────────────
URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", re.IGNORECASE)
ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\ufeff\u00ad]")
HTML_TAG_RE = re.compile(r"<[^>]+>")


# ── Core functions ────────────────────────────────────────────────────────────

def strip_html(raw: str) -> str:
    """Remove HTML tags; use BeautifulSoup if available."""
    if _HAS_BS4:
        soup = BeautifulSoup(raw, "html.parser")
        return soup.get_text(separator=" ")
    return HTML_TAG_RE.sub(" ", raw)


def extract_urls(text: str) -> List[str]:
    """Return all URLs found in *text*."""
    return URL_RE.findall(text)


def detect_obfuscation(text: str) -> bool:
    """Return True if zero-width / invisible characters are present."""
    return bool(ZERO_WIDTH_RE.search(text))


def tokenise(text: str) -> List[str]:
    """Lowercase, remove punctuation, split into tokens, remove stopwords."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    if _stopwords:
        tokens = [t for t in tokens if t not in _stopwords]
    if _HAS_NLTK and _stemmer:
        tokens = [_stemmer.stem(t) for t in tokens]
    return tokens


def parse_eml_headers(raw_email: str) -> Dict[str, str]:
    """Parse From, Reply-To, Subject from a raw .eml string."""
    headers: Dict[str, str] = {}
    try:
        msg = email.message_from_string(raw_email, policy=policy.default)
        for key in ("From", "Reply-To", "Subject", "To", "Date", "Return-Path"):
            val = msg.get(key, "")
            if val:
                headers[key] = str(val)
    except Exception:
        pass
    return headers


def get_body(raw_email: str) -> str:
    """Extract plain-text body from a raw .eml string."""
    try:
        msg = email.message_from_string(raw_email, policy=policy.default)
        body_parts = []
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                body_parts.append(part.get_content())
            elif ct == "text/html":
                body_parts.append(strip_html(part.get_content()))
        return "\n".join(body_parts)
    except Exception:
        return raw_email


def preprocess(raw_email: str) -> Dict:
    """
    Full preprocessing pipeline.
    Accepts either raw .eml or plain-text email content.
    Returns a dict with all extracted features for downstream analysis.
    """
    headers = parse_eml_headers(raw_email)
    body = get_body(raw_email)
    full_text = (headers.get("Subject", "") + " " + body)

    urls = extract_urls(full_text)
    tokens = tokenise(full_text)
    obfuscated = detect_obfuscation(full_text)

    # Detect sender ↔ reply-to mismatch
    sender = headers.get("From", "")
    reply_to = headers.get("Reply-To", "")
    sender_mismatch = bool(reply_to and reply_to.strip() != sender.strip())

    return {
        "headers": headers,
        "body": body,
        "urls": urls,
        "tokens": tokens,
        "token_count": len(tokens),
        "url_count": len(urls),
        "obfuscated": obfuscated,
        "sender_mismatch": sender_mismatch,
        "subject": headers.get("Subject", ""),
        "from": sender,
    }


if __name__ == "__main__":
    sample = """From: security@paypa1.com
Reply-To: attacker@evil.com
Subject: URGENT: Verify your account now!

Dear Customer,
Your account has been compromised. Click here immediately:
https://paypa1.com/login?redirect=http://evil.com/steal
"""
    import pprint
    pprint.pprint(preprocess(sample))
