import os
import requests
import base64
from datetime import datetime

class MpesaService:
    def __init__(self):
        # Strip any accidental quotes or whitespace from environment variables
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY', '').strip(' "\'')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET', '').strip(' "\'')
        self.shortcode = os.getenv('MPESA_SHORTCODE', '').strip(' "\'')
        self.passkey = os.getenv('MPESA_PASSKEY', '').strip(' "\'')
        self.base_url = "https://sandbox.safaricom.co.ke" # Change to production URL when ready

    def get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        try:
            response = requests.get(url, auth=(self.consumer_key, self.consumer_secret), timeout=30)
            if response.status_code == 200:
                return response.json()['access_token']
            print(f"M-Pesa Token Error ({response.status_code}): {response.text}")
            return None
        except Exception as e:
            print(f"M-Pesa Token Exception: {str(e)}")
            return None

    def stk_push(self, phone_number, amount, callback_url):
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "Failed to get access token"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": "FARD Donation",
            "TransactionDesc": "Support Community Development"
        }

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "CustomerMessage": "Connection to M-Pesa timed out."}
