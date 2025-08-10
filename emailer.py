import os, smtplib
from email.mime.text import MIMEText

SMTP_HOST=os.getenv("SMTP_HOST"); SMTP_PORT=int(os.getenv("SMTP_PORT","587"))
SMTP_USER=os.getenv("SMTP_USER"); SMTP_PASS=os.getenv("SMTP_PASS")
EMAIL_FROM=os.getenv("EMAIL_FROM"); BASE_URL=os.getenv("BASE_URL")

def send_text_email(to_email: str, subject: str, html: str):
    msg = MIMEText(html, "html")
    msg["Subject"]=subject; msg["From"]=EMAIL_FROM; msg["To"]=to_email
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(EMAIL_FROM, [to_email], msg.as_string())

def send_verify_link(email: str, token: str):
    link=f"{BASE_URL}/auth/set-password?token={token}"
    html=f"""<p>Welcome to the Community Champions Circle!</p>
             <p>Click to set your password and continue: <a href="{link}">Set Password</a></p>"""
    send_text_email(email, "Verify your email & set your password", html)
