from flask import Flask, request, jsonify, send_file
import requests
import json
from dotenv import load_dotenv

# Initialize Flask
app = Flask(__name__, static_folder='.')

# --- CONFIGURATION (BREVO) ---
# 1. Go to Brevo.com -> Settings -> SMTP & API -> Generate API Key
# 2. Paste the key below (starts with xkeysib-...)
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

# You can set this to anything you want!
SENDER_NAME = "🎅 Secret Santa Bot"
SENDER_EMAIL = "santa@highonswift.com" 

# 1. Route to serve the HTML Page (Frontend)
@app.route('/')
def home():
    return send_file('index.html')

# 2. Route to handle the Email Sending (Backend)
@app.route('/api/index', methods=['POST'])
def send_mail():
    data = request.json
    recipient_email = data.get('email')
    task_message = data.get('task')

    if not recipient_email or not task_message:
        return jsonify({"error": "Missing email or task"}), 400

    # --- BREVO API LOGIC ---
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    # HTML Email Body
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #d42426;">Ho Ho Ho! 🎅</h2>
            <p>You have been assigned a Secret Santa task.</p>
            <div style="background-color: #f9f9f9; padding: 15px; border-left: 5px solid #d42426; margin: 20px 0;">
                <strong>YOUR MISSION:</strong><br>
                {task_message}
            </div>
            <p>Good luck!</p>
            <p><em>- The Secret Santa Bot</em></p>
        </body>
    </html>
    """

    payload = {
        "sender": {
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },
        "to": [
            {
                "email": recipient_email
            }
        ],
        "subject": "🎅 Secret Santa Mission Assignment",
        "htmlContent": html_content
    }

    try:
        # Send POST request to Brevo
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Status 201 means "Created" (Email Sent Successfully)
        if response.status_code == 201:
            return jsonify({"message": "Sent successfully"}), 200
        else:
            print(f"❌ Brevo Error: {response.text}")
            return jsonify({"error": "Failed to send email via Brevo"}), 500
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🎅 Secret Santa App is running!")
    print("👉 Go to: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
