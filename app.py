from flask import Flask, request, render_template, jsonify, session
import random
import smtplib
from email.mime.text import MIMEText
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def send_email(to_email, code):
    msg = MIMEText(f'Your verification code is: {code}')
    msg['Subject'] = 'Your Verification Code'
    msg['From'] = app.config['EMAIL_ADDRESS']
    msg['To'] = to_email

    with smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT']) as server:
        server.starttls()
        server.login(app.config['EMAIL_ADDRESS'], app.config['EMAIL_PASSWORD'])
        server.send_message(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = request.form['email']
    verification_code = ''.join(random.choices('0123456789', k=6))
    session['verification_code'] = verification_code  # 存储在会话中
    session['email'] = email

    send_email(email, verification_code)
    return jsonify({'message': 'Verification code sent!'})

@app.route('/verify_code', methods=['POST'])
def verify_code():
    code = request.form['code']
    if code == session.get('verification_code'):
        return jsonify({'message': 'Verification successful!'})
    else:
        return jsonify({'message': 'Invalid code!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
