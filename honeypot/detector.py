from collections import defaultdict

SQL_PATTERNS = [

    "' OR '1'='1",

    "' OR 1=1 --",

    "UNION SELECT",

    "DROP TABLE",

    "--",

    ";"

]

SCANNER_SIGNATURES = [

    "curl",

    "wget",

    "nikto",

    "nmap",

    "sqlmap",

    "python-requests",

    "postman",

    "masscan",

    "zgrab"

]

# Store login attempts

login_attempts = defaultdict(int)


def detect_attack(
    ip_address,
    username,
    password,
    user_agent
):

    data = (
        username + " " + password
    ).lower()

    user_agent = (
        user_agent or ""
    ).lower()

    # Scanner detection

    for scanner in SCANNER_SIGNATURES:

        if scanner in user_agent:

            return (
                "Scanner Detected",
                "High"
            )

    # SQL injection detection

    for pattern in SQL_PATTERNS:

        if pattern.lower() in data:

            return (
                "SQL Injection",
                "High"
            )

    # Brute force detection

    login_attempts[ip_address] += 1

    if login_attempts[ip_address] >= 5:

        return (
            "Brute Force",
            "Medium"
        )

    return (
        "Credential Harvesting",
        "Low"
    )
