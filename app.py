from flask import Flask, request, jsonify, send_file
import smtplib
import ssl
from email.message import EmailMessage

# Initialize Flask
# static_folder='.' tells Flask that index.html is in the current directory
app = Flask(__name__, static_folder='.')

# --- CONFIGURATION (FILL THESE IN FOR LOCAL TESTING) ---
# Since we are running locally, we can't use Vercel environment variables.
# Put your credentials directly here for testing.
SENDER_EMAIL = "hos.secretsanta.2025@gmail.com"
APP_PASSWORD = "nhympayuazvnzuih" 

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

    subject = "🎅 Secret Santa Mission Assignment"
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    
    body = f"""
    Ho Ho Ho!
    
    You have been assigned a Secret Santa task.
    
    YOUR MISSION:
    {task_message}
    
    Good luck!
    - The Secret Santa Bot
    """
    msg.set_content(body)

    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return jsonify({"message": "Sent successfully"}), 200
    except Exception as e:
        print(f"Error: {e}") # Print error to terminal so you can see it
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🎅 Secret Santa App is running!")
    print("👉 Go to: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)