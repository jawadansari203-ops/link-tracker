from datetime import datetime
from email.mime.text import MIMEText
import smtplib
from flask import Flask, redirect, request
import requests

app = Flask(__name__)

# Email credentials (apni details yahan check kar lein)
EMAIL_ADDRESS = "jawadansari203@gmail.com"
EMAIL_PASSWORD = "iwbf guab qbid ktul"
RECEIVER_EMAIL = "ReceiverEmail@gmail.com"


def send_email(ip, city, country, isp, user_agent, target_url):
  try:
    body = (
        f"--- New Link Clicked ---\nTime: {datetime.now()}\nIP Address:"
        f" {ip}\nLocation: {city}, {country}\nISP: {isp}\nTarget URL:"
        f" {target_url}\nUser-Agent: {user_agent}"
    )
    msg = MIMEText(body)
    msg["Subject"] = "🚨 Link Clicked Alert!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
      server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
  except Exception as e:
    print("Email error:", e)


# 1. Root Route (Ab yahan 404 nahi aayega)
@app.route("/")
def home():
  return "Link Tracker is Live and Running!"


# 2. Tracking Route
@app.route("/go")
def track_and_redirect():
  target_url = request.args.get("url", "https://www.google.com")
  if not target_url:
    return "Error: No target URL provided.", 400

  # IP nikalna
  ip = request.headers.get("X-Forwarded-For", request.remote_addr)
  if ip and "," in ip:
    ip = ip.split(",")[0].strip()

  user_agent = request.headers.get("User-Agent")

  # Geolocation API
  try:
    geo_res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
    city = geo_res.get("city", "Unknown")
    country = geo_res.get("country", "Unknown")
    isp = geo_res.get("isp", "Unknown")
  except:
    city, country, isp = "Unknown", "Unknown", "Unknown"

  # Email bhejna
  send_email(ip, city, country, isp, user_agent, target_url)

  return redirect(target_url)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
