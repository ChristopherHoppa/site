from html import escape

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# =========================================================
# ASENTRION COURIER
# =========================================================

BRAND_NAME = "Asentrion"
COURIER_NAME = "Asentrion Courier"


SERVICE_LABELS = {
    "website": "Website project",
    "software": "Custom software",
    "branding": "Branding & digital presence",
    "technical": "Technical help",
    "other": "Something else",
}


CONTACT_LABELS = {
    "email": "Email",
    "phone": "Phone",
}


EXPERIENCE_LABELS = {
    "student": "Student / Learning",
    "junior": "Early career",
    "mid": "Mid-level",
    "senior": "Senior",
    "specialist": "Specialist / Consultant",
}


INTEREST_LABELS = {
    "software_engineering": "Software Engineering",
    "web_development": "Web Development",
    "cybersecurity": "Cybersecurity",
    "infrastructure_devops": "Infrastructure / DevOps",
    "design": "UI / UX / Design",
    "technical_support": "Technical Support / Operations",
}


# =========================================================
# HELPERS
# =========================================================

def clean(value, fallback="Not provided"):
    """
    Safely convert form input to text for use inside HTML email.
    """
    if value is None:
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    return escape(value)


def display_value(mapping, value):
    """
    Convert stored/select values into their readable labels.
    """
    if not value:
        return "Not provided"

    return escape(mapping.get(value, value))


def render_row(label, value):
    return f"""
        <tr>
            <td
                style="
                    width: 170px;
                    padding: 11px 0;
                    border-bottom: 1px solid #294052;
                    color: #8294a3;
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 12px;
                    vertical-align: top;
                "
            >
                {escape(label)}
            </td>

            <td
                style="
                    padding: 11px 0;
                    border-bottom: 1px solid #294052;
                    color: #dce4eb;
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 13px;
                    line-height: 1.6;
                    vertical-align: top;
                "
            >
                {value}
            </td>
        </tr>
    """


def wrap_email(*, eyebrow, title, intro, body_html, footer_note):
    """
    Shared Asentrion email shell.

    Styles are inline because many email clients strip or ignore
    external stylesheets and <style> blocks.
    """

    return f"""
    <!doctype html>

    <html lang="en">

    <body
        style="
            margin: 0;
            padding: 0;
            background: #07131f;
        "
    >

        <table
            role="presentation"
            width="100%"
            cellspacing="0"
            cellpadding="0"
            border="0"
            style="
                width: 100%;
                background: #07131f;
                margin: 0;
                padding: 0;
            "
        >

            <tr>

                <td
                    align="center"
                    style="
                        padding: 38px 16px;
                    "
                >

                    <table
                        role="presentation"
                        width="100%"
                        cellspacing="0"
                        cellpadding="0"
                        border="0"
                        style="
                            width: 100%;
                            max-width: 680px;
                            background: #0a1928;
                            border: 1px solid #294052;
                            border-collapse: separate;
                        "
                    >


                        <!-- HEADER -->

                        <tr>

                            <td
                                style="
                                    padding: 24px 28px;
                                    border-bottom: 1px solid #294052;
                                    background: #081623;
                                "
                            >

                                <table
                                    role="presentation"
                                    width="100%"
                                    cellspacing="0"
                                    cellpadding="0"
                                    border="0"
                                >

                                    <tr>

                                        <td
                                            style="
                                                color: #ffffff;
                                                font-family: Arial, Helvetica, sans-serif;
                                                font-size: 17px;
                                                font-weight: 700;
                                                letter-spacing: .02em;
                                            "
                                        >
                                            ASENTRION
                                        </td>


                                        <td
                                            align="right"
                                            style="
                                                color: #61798a;
                                                font-family: 'Courier New', monospace;
                                                font-size: 10px;
                                                letter-spacing: .10em;
                                            "
                                        >
                                            COURIER / TRANSMISSION
                                        </td>

                                    </tr>

                                </table>

                            </td>

                        </tr>



                        <!-- MESSAGE -->

                        <tr>

                            <td
                                style="
                                    padding: 38px 28px 18px;
                                "
                            >

                                <div
                                    style="
                                        margin-bottom: 13px;
                                        color: #ffffff;
                                        font-family: 'Courier New', monospace;
                                        font-size: 10px;
                                        font-weight: 700;
                                        letter-spacing: .14em;
                                        text-transform: uppercase;
                                    "
                                >
                                    {escape(eyebrow)}
                                </div>


                                <h1
                                    style="
                                        margin: 0 0 20px;
                                        color: #ffffff;
                                        font-family: Arial, Helvetica, sans-serif;
                                        font-size: 30px;
                                        line-height: 1.15;
                                        font-weight: 600;
                                    "
                                >
                                    {escape(title)}
                                </h1>


                                <p
                                    style="
                                        margin: 0;
                                        color: #9aacba;
                                        font-family: Arial, Helvetica, sans-serif;
                                        font-size: 15px;
                                        line-height: 1.75;
                                    "
                                >
                                    {intro}
                                </p>

                            </td>

                        </tr>



                        <!-- SIGNAL DIVIDER -->

                        <tr>

                            <td
                                style="
                                    padding: 10px 28px 8px;
                                "
                            >

                                <table
                                    role="presentation"
                                    width="100%"
                                    cellspacing="0"
                                    cellpadding="0"
                                    border="0"
                                >

                                    <tr>

                                        <td
                                            style="
                                                width: 12px;
                                                height: 12px;
                                                border: 1px solid #ffffff;
                                                font-size: 0;
                                                line-height: 0;
                                            "
                                        >
                                            &nbsp;
                                        </td>


                                        <td
                                            style="
                                                height: 1px;
                                                background: #ffffff;
                                                font-size: 0;
                                                line-height: 0;
                                            "
                                        >
                                            &nbsp;
                                        </td>


                                        <td
                                            style="
                                                width: 58px;
                                                padding-left: 10px;
                                                color: #718696;
                                                font-family: 'Courier New', monospace;
                                                font-size: 9px;
                                                letter-spacing: .08em;
                                            "
                                        >
                                            RECEIVED
                                        </td>

                                    </tr>

                                </table>

                            </td>

                        </tr>



                        <!-- BODY -->

                        <tr>

                            <td
                                style="
                                    padding: 22px 28px 34px;
                                "
                            >

                                {body_html}

                            </td>

                        </tr>



                        <!-- FOOTER -->

                        <tr>

                            <td
                                style="
                                    padding: 24px 28px;
                                    border-top: 1px solid #294052;
                                    background: #06111c;
                                "
                            >

                                <p
                                    style="
                                        margin: 0 0 8px;
                                        color: #91a1af;
                                        font-family: Arial, Helvetica, sans-serif;
                                        font-size: 12px;
                                        line-height: 1.6;
                                    "
                                >
                                    {footer_note}
                                </p>


                                <p
                                    style="
                                        margin: 0;
                                        color: #526b7d;
                                        font-family: 'Courier New', monospace;
                                        font-size: 9px;
                                        line-height: 1.7;
                                        letter-spacing: .08em;
                                    "
                                >
                                    ASENTRION COURIER
                                    <br>
                                    Technology · Design · Innovation
                                </p>

                            </td>

                        </tr>


                    </table>

                </td>

            </tr>

        </table>

    </body>

    </html>
    """


# =========================================================
# PROJECT REQUEST CONFIRMATION
# =========================================================

def send_project_confirmation(data):
    """
    Confirmation email sent to someone who submits
    the Get Started / project request form.
    """

    recipient_email = data.get("email")

    if not recipient_email:
        raise ValueError(
            "Project confirmation requires an email address."
        )


    first_name = clean(
        data.get("full_name"),
        "there",
    ).split()[0]


    service = display_value(
        SERVICE_LABELS,
        data.get("service"),
    )


    preferred_contact = display_value(
        CONTACT_LABELS,
        data.get("preferred_contact"),
    )


    rows = "".join(
        [
            render_row(
                "Name",
                clean(data.get("full_name")),
            ),

            render_row(
                "Organization",
                clean(data.get("organization")),
            ),

            render_row(
                "Service",
                service,
            ),

            render_row(
                "Preferred contact",
                preferred_contact,
            ),

            render_row(
                "Phone",
                clean(data.get("phone")),
            ),

            render_row(
                "Timeline",
                clean(data.get("timeline")),
            ),

            render_row(
                "Budget",
                clean(data.get("budget")),
            ),
        ]
    )


    details = clean(
        data.get("details")
    ).replace(
        "\n",
        "<br>",
    )


    body_html = f"""

        <p
            style="
                margin: 0 0 22px;
                color: #dce4eb;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px;
                line-height: 1.7;
            "
        >
            Your project request made it through.
            Below is the information Asentrion received.
        </p>


        <table
            role="presentation"
            width="100%"
            cellspacing="0"
            cellpadding="0"
            border="0"
            style="
                width: 100%;
                border-top: 1px solid #294052;
            "
        >
            {rows}
        </table>


        <div
            style="
                margin-top: 28px;
                padding: 18px;
                border: 1px solid #294052;
                background: #07131f;
            "
        >

            <div
                style="
                    margin-bottom: 10px;
                    color: #718696;
                    font-family: 'Courier New', monospace;
                    font-size: 9px;
                    letter-spacing: .10em;
                    text-transform: uppercase;
                "
            >
                PROJECT DETAILS
            </div>


            <div
                style="
                    color: #dce4eb;
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 13px;
                    line-height: 1.7;
                "
            >
                {details}
            </div>

        </div>


        <div
            style="
                margin-top: 26px;
                padding-left: 15px;
                border-left: 2px solid #ffffff;
            "
        >

            <strong
                style="
                    display: block;
                    margin-bottom: 7px;
                    color: #ffffff;
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 13px;
                "
            >
                What happens next
            </strong>


            <span
                style="
                    color: #91a1af;
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 13px;
                    line-height: 1.7;
                "
            >
                The request will be reviewed and the next step
                will be based on the scope, timing and technical
                requirements you provided.
            </span>

        </div>

    """


    html_body = wrap_email(
        eyebrow="Project request received",
        title=f"Thanks, {first_name}",
        intro=(
            "Your request has been received by Asentrion. "
            "This message confirms that the information you "
            "submitted reached us successfully."
        ),
        body_html=body_html,
        footer_note=(
            "This is an automated confirmation from Asentrion Courier. "
            "You do not need to submit the form again."
        ),
    )


    text_body = f"""
Asentrion

Project request received

Thanks, {first_name}.

Your project request has been received successfully.

Service:
{service}

Organization:
{clean(data.get("organization"))}
Preferred contact:
{preferred_contact}

Timeline:
{clean(data.get("timeline"))}

Budget:
{clean(data.get("budget"))}

Project details:
{clean(data.get("details"))}

The request will be reviewed and the next step will be based
on the scope, timing and technical requirements you provided.

Asentrion Courier
Technology · Design · Innovation
""".strip()


    email = EmailMultiAlternatives(
        subject="Asentrion | Project request received",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
        reply_to=["courier@asentrion.com"],
    )


    email.attach_alternative(
        html_body,
        "text/html",
    )


    return email.send(fail_silently=False)


# =========================================================
# COLLABORATION CONFIRMATION
# =========================================================

def send_collaboration_confirmation(data):
    """Send the collaboration confirmation to the email entered on the form."""
    recipient_email = str(data.get("email") or "").strip()
    if not recipient_email:
        raise ValueError("Collaboration confirmation requires an email address.")

    full_name = str(data.get("full_name") or "").strip()
    first_name = full_name.split()[0] if full_name else "there"

    experience_value = data.get("experience_level") or ""
    experience_label = EXPERIENCE_LABELS.get(
        experience_value, experience_value or "Not provided"
    )

    raw_interests = data.get("areas_of_interest") or []
    if isinstance(raw_interests, str):
        raw_interests = [raw_interests]
    interest_labels = [INTEREST_LABELS.get(item, item) for item in raw_interests]

    # Django escapes form values when rendering this HTML template.
    html_body = render_to_string(
        "emails/collaborate.html",
        {
            **data,
            "logo_url": "https://asentrion.com/logo.png",
            "experience_label": experience_label,
            "interest_labels": interest_labels,
        },
    )

    def value(key):
        return str(data.get(key) or "").strip() or "Not provided"

    text_body = f"""Asentrion | Collaboration received

Thanks for reaching out, {first_name}.

We have received your collaboration submission. Below is a copy of your information.

Name: {value('full_name')}
Email: {recipient_email}
Phone: {value('phone')}
Location: {value('location')}
Current role: {value('current_role')}
Experience: {experience_label}
Primary technical focus: {value('primary_focus')}
Areas of interest: {', '.join(interest_labels) or 'Not provided'}
Availability: {value('availability')}
GitHub: {value('github')}
Portfolio: {value('portfolio_url')}
Résumé: {value('resume_url')}

Introduction:
{value('introduction')}

Why you want to collaborate:
{value('collaboration_fit')}

Your information will be reviewed against current and future Asentrion projects.
If there is a potential fit, we will reach out.

Asentrion Courier
Technology · Design · Innovation"""

    email = EmailMultiAlternatives(
        subject="Asentrion | Collaboration received",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
        reply_to=["courier@asentrion.com"],
    )
    email.attach_alternative(html_body, "text/html")
    # Django 6.1: use the configured MAILERS["default"] SMTP backend.
    return email.send(using="default")
