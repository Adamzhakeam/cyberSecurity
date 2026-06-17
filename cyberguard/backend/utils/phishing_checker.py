import re
from urllib.parse import urlparse
from utils.risk_calculator import build_scan_item

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "bank",
    "update",
    "secure",
    "account",
    "signin",
    "password",
    "wallet",
    "payment",
]


def analyze_url(url):
    """Analyze the provided URL and return a structured scan item.

    The function applies a series of heuristic checks to compute a
    risk score and returns a dict created by `build_scan_item`.

    Checks applied:
    - IP address used instead of hostname (+25)
    - No HTTPS (+20)
    - Suspicious keywords (+10 each)
    - Excessive hyphens in hostname (+15)
    - URL length > 75 (+10)

    Args:
        url (str): URL string provided by user

    Returns:
        dict: scan item with `id`, `url`, `riskScore`, `status`, `reasons`
    """
    normalized_url = url.strip()
    if not normalized_url.startswith(("http://", "https://")):
        normalized_url = f"http://{normalized_url}"

    parsed = urlparse(normalized_url)
    hostname = parsed.hostname or ""
    score = 0
    reasons = []

    if is_ip_address(hostname):
        score += 25
        reasons.append("Uses IP address instead of domain")

    if parsed.scheme != "https":
        score += 20
        reasons.append("No HTTPS")

    suspicious_reasons = collect_keyword_reasons(normalized_url)
    score += suspicious_reasons["score"]
    reasons.extend(suspicious_reasons["reasons"])

    if hostname.count("-") >= 2:
        score += 15
        reasons.append("Excessive hyphens in hostname")

    if len(normalized_url) > 75:
        score += 10
        reasons.append("URL is too long")

    score = min(score, 100)
    status = classify_risk(score)

    return build_scan_item(normalized_url, score, status, reasons)


def is_ip_address(hostname):
    """Return True if the hostname is an IPv4 literal.

    Args:
        hostname (str): hostname extracted from a URL

    Returns:
        bool: True when hostname matches IPv4 pattern
    """
    ip_pattern = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
    return bool(ip_pattern.match(hostname))


def collect_keyword_reasons(url):
    """Scan the URL for known suspicious keywords.

    Returns a dict with cumulative score contributions and reason strings.
    """
    total = 0
    reasons = []
    lower_url = url.lower()
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in lower_url:
            total += 10
            reasons.append(f"Contains suspicious keyword: {keyword}")
    return {"score": total, "reasons": reasons}


def classify_risk(score):
    """Classify a numeric risk score into a textual risk level.

    Args:
        score (int): aggregated risk score (0-100)

    Returns:
        str: one of "SAFE", "SUSPICIOUS", or "DANGEROUS"
    """
    if score <= 30:
        return "SAFE"
    if score <= 60:
        return "SUSPICIOUS"
    return "DANGEROUS"
