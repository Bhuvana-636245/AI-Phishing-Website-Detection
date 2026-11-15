from urllib.parse import urlparse
import re
import math
from collections import Counter


def extract_url_features(url):

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    features = {}

    # 1. URL length
    features["url_length"] = len(url)

    # 2. IP address detection
    features["has_ip_address"] = int(
        bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain))
    )

    # 3. Dot count
    features["dot_count"] = url.count(".")

    # 4. HTTPS flag
    features["https_flag"] = int(parsed.scheme == "https")

    # 5. URL entropy
    counts = Counter(url)

    features["url_entropy"] = -sum(
        (count / len(url)) * math.log2(count / len(url))
        for count in counts.values()
    ) if url else 0.0

    # 6. Token count
    features["token_count"] = len(
        re.findall(r"[a-zA-Z0-9]+", url)
    )

    # 7. Subdomain count
    features["subdomain_count"] = max(
        0, len(domain.split(".")) - 2
    )

    # 8. Query parameter count
    features["query_param_count"] = len(query.split("&"))

    # 9. TLD length
    features["tld_length"] = (
        len(domain.split(".")[-1]) if "." in domain else 0
    )

    # 10. Path length
    features["path_length"] = len(path)

    # 11. Hyphen in domain
    features["has_hyphen_in_domain"] = int("-" in domain)

    # 12. Number of digits
    features["number_of_digits"] = sum(
        char.isdigit() for char in url
    )

    # 13. TLD popularity
    popular_tlds = ["com", "net", "org", "edu", "gov"]
    tld = domain.split(".")[-1].lower() if domain else ""

    features["tld_popularity"] = int(tld in popular_tlds)

    # 14. Suspicious file extension
    features["suspicious_file_extension"] = int(
        bool(re.search(r"\.(exe|zip|scr|bat|php)$", path.lower()))
    )

    # 15. Domain name length
    features["domain_name_length"] = (
        len(domain.split(".")[0]) if domain else 0
    )

    # 16. Percentage of numeric characters
    features["percentage_numeric_chars"] = (
        sum(char.isdigit() for char in url) / len(url) * 100
        if url else 0
    )

    return features