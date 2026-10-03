from datetime import datetime
from email.mime.text import MIMEText
import smtplib
from flask import Flask, redirect, request
import requests

app = Flask(__name__)

# Cloud hosting ke liye hardcoded credentials
EMAIL_ADDRESS = 'jawadansari203@gmail.com'  
EMAIL_PASSWORD = 'tlxp gxic orth xtns' 
RECEIVER_EMAIL = EMAIL_ADDRESS

def send_email_notification(details):
    try:
        msg = MIMEText(details)
        msg['Subject'] = '🚨 New Link Click Alert!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
            print('Email notification successfully bhej di gayi')
    except Exception as e:
        print('Email error:', e)

@app.route('/go')
def track_and_redirect():
    target_url = request.args.get('url')
    if not target_url:
        return "Error: No target URL provided.", 400

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    time_clicked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    geo_info = "Location not found"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        if response['status'] == 'success':
            geo_info = f"{response['city']}, {response['country']} (ISP: {response['isp']})"
    except:
        pass

    details = f"""
New click detected!

Time: {time_clicked}
IP Address: {ip_address}
Location: {geo_info}
User Agent: {user_agent}
Target URL: {target_url}
"""

    send_email_notification(details)
    return redirect(target_url)

if __name__ == '__main__':
    app.run(debug=True)
