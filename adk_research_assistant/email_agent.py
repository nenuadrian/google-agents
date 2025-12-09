import os
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SMTP_DEFAULT_PORT = int(os.getenv("SMTP_DEFAULT_PORT", 587))
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_ADDR = os.getenv("FROM_ADDR", "")
TO_ADDR = os.getenv("TO_ADDR", "")


@dataclass
class EmailConfig:
    smtp_host: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool = True


def _send_html_email(
    config: EmailConfig,
    *,
    subject: str,
    html_body: str,
) -> None:
    """Low-level helper to send an HTML email via SMTP."""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_ADDR
    msg["To"] = TO_ADDR

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(config.smtp_host, config.smtp_port) as server:
        if config.use_tls:
            server.starttls()
        if config.username and config.password:
            server.login(config.username, config.password)
        server.sendmail(FROM_ADDR, [TO_ADDR], msg.as_string())


def send_research_email(
    *,
    subject: str,
    html_body: str,
) -> str:
    """Sends an HTML email with the given subject and body."""

    if not SMTP_HOST:
        return (
            "Preview only; email not sent.\n"
            f"From: {FROM_ADDR}\n"
            f"To: {TO_ADDR}\n"
            f"Subject: {subject}\n"
            f"HTML Body:\n{html_body}"
        )

    config = EmailConfig(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_DEFAULT_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
    )

    _send_html_email(
        config,
        subject=subject,
        html_body=html_body,
    )

    return "Email sent successfully."


send_research_email_tool = FunctionTool(func=send_research_email)

# --------

email_agent = Agent(
    model=GEMINI_MODEL,
    name="email_body_generator",
    description="Generates clean, readable HTML emails from instructions.",
    instruction=(
        "You are an assistant that writes professional, accessible HTML "
        "emails. Given a set of instructions, produce a complete HTML "
        "document suitable for the email body. Use semantic tags (h1, h2, "
        "p, ul/li) and inline styles only where necessary. Do not include "
        "external CSS or scripts."
        "Create an HTML beautiful stylized email body with the following requirements. Ensure to add a frame, header, footer, relevant to the topic of the content."
        "Do not include the <html> or <body> tags, only the inner content. Use the send_research_email_tool tool to send the email."
    ),
    tools=[send_research_email_tool],
)
