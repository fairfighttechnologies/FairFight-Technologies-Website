import os

import requests

from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)

from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "fairfight-development-secret"
)


# ==========================================
# EMAIL CONFIGURATION
# ==========================================

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

MAIL_TO = os.getenv(
    "MAIL_TO",
    "fairfight.technologies@gmail.com"
)


# ==========================================
# WEBSITE ROUTES
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/joymouse")
def joymouse():
    return render_template("joymouse.html")


@app.route("/technology")
def technology():
    return render_template("technology.html")


@app.route("/impact")
def impact():
    return render_template("impact.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ==========================================
# CONTACT FORM
# ==========================================

@app.route("/send-message", methods=["POST"])
def send_message():

    name = request.form.get("name", "").strip()

    email = request.form.get("email", "").strip()

    organization = request.form.get(
        "organization",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    message = request.form.get(
        "message",
        ""
    ).strip()


    # ======================================
    # VALIDATION
    # ======================================

    if not name or not email or not message:

        flash(
            "Please fill in all required fields.",
            "error"
        )

        return redirect(url_for("contact"))


    # ======================================
    # CHECK RESEND API KEY
    # ======================================

    if not RESEND_API_KEY:

        print("ERROR: RESEND_API_KEY is missing.")

        flash(
            "Email service is not configured.",
            "error"
        )

        return redirect(url_for("contact"))


    # ======================================
    # EMAIL CONTENT
    # ======================================

    subject = (
        f"New FairFight Website Enquiry - {name}"
    )


    email_text = f"""
New enquiry received from the
FairFight Technologies website.

========================================

CONTACT DETAILS

Name:
{name}

Email:
{email}

Organization:
{organization if organization else "Not provided"}

Phone:
{phone if phone else "Not provided"}

========================================

MESSAGE

{message}

========================================

Sent through:
FairFight Technologies Website
"""


    # ======================================
    # SEND EMAIL THROUGH RESEND
    # ======================================

    try:

        response = requests.post(
            "https://api.resend.com/emails",

            headers={
                "Authorization":
                    f"Bearer {RESEND_API_KEY}",

                "Content-Type":
                    "application/json"
            },

            json={
                "from": "FairFight Website <onboarding@resend.dev>",

                "to": [MAIL_TO],

                "subject": subject,

                "text": email_text,

                "reply_to": email
            },

            timeout=15
        )


        # ==================================
        # SUCCESS
        # ==================================

        if response.status_code in (200, 201):

            flash(
                "Your message has been sent successfully. "
                "The FairFight Technologies team will "
                "get back to you.",
                "success"
            )


        # ==================================
        # RESEND ERROR
        # ==================================

        else:

            print(
                "RESEND ERROR:",
                response.status_code,
                response.text
            )

            flash(
                "We couldn't send your message right now. "
                "Please try again later.",
                "error"
            )


    # ======================================
    # CONNECTION ERROR
    # ======================================

    except requests.RequestException as error:

        print(
            "EMAIL CONNECTION ERROR:",
            error
        )

        flash(
            "We couldn't connect to the email service. "
            "Please try again later.",
            "error"
        )


    return redirect(url_for("contact"))


# ==========================================
# RUN LOCALLY
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )