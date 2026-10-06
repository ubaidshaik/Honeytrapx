from flask import Flask, render_template, request

from database import init_db, log_attack
from detector import detect_attack

app = Flask(
    __name__,
    template_folder="../templates"
)

# Initialize the database

init_db()


# Detect scanners on every request

@app.before_request
def detect_scanners():

    user_agent = (
        request.headers.get("User-Agent") or ""
    ).lower()

    scanner_signatures = [

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

    for scanner in scanner_signatures:

     if scanner in user_agent:

        log_attack(

            ip_address=request.remote_addr,

            username="N/A",

            password="N/A",

            user_agent=user_agent,

            attack_type=f"Scanner ({scanner})",

            severity="High"
        )

        print(
            "\n========== SCANNER ALERT =========="
        )

        print(
            f"IP Address : {request.remote_addr}"
        )

        print(
            f"Tool       : {scanner}"
        )

        print(
            f"Path       : {request.path}"
        )

        print(
            "===================================\n"
        )

        break


@app.route("/")
def home():

    return render_template(
        "login.html"
    )


@app.route(
    "/login",
    methods=["POST"]
)
def login():

    username = request.form.get(
        "username"
    )

    password = request.form.get(
        "password"
    )

    ip_address = request.remote_addr

    user_agent = request.headers.get(
        "User-Agent"
    )

    attack_type, severity = detect_attack(

        ip_address,

        username,

        password,

        user_agent
    )

    log_attack(

        ip_address,

        username,

        password,

        user_agent,

        attack_type,

        severity
    )

    print(
        "\n========== ATTACK LOG =========="
    )

    print(
        f"IP Address : {ip_address}"
    )

    print(
        f"Username   : {username}"
    )

    print(
        f"Password   : {password}"
    )

    print(
        f"Browser    : {user_agent}"
    )

    print(
        f"Attack Type: {attack_type}"
    )

    print(
        f"Severity   : {severity}"
    )

    print(
        "================================\n"
    )

    return """
    <h2>Login failed!</h2>
    <p>Invalid username or password.</p>
    <a href="/">Go back</a>
    """


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5002,

        debug=True
    )
