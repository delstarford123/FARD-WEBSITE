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
        
        # Switch to Production by default as requested
        self.env = os.getenv('MPESA_ENV', 'production').lower()
        if self.env == 'sandbox':
            self.base_url = "https://sandbox.safaricom.co.ke"
        else:
            self.base_url = "https://api.safaricom.co.ke"
        
        print(f"M-Pesa Service initialized in {self.env} mode.")

    def get_access_token(self):
        # Validation for missing credentials
        if not self.consumer_key or not self.consumer_secret:
            print(f"M-Pesa Config Error: Consumer Key ({'Set' if self.consumer_key else 'Missing'}) or Secret ({'Set' if self.consumer_secret else 'Missing'}) is missing.")
            return None
            
        # DIAGNOSTIC: Print masked keys to help user verify Render environment variables
        print(f"DEBUG: Using Consumer Key: {self.consumer_key[:4]}...{self.consumer_key[-4:]} (Length: {len(self.consumer_key)})")
        print(f"DEBUG: Using Consumer Secret: {self.consumer_secret[:4]}...{self.consumer_secret[-4:]} (Length: {len(self.consumer_secret)})")
            
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        
        try:
            print(f"Attempting M-Pesa token request to: {url}")
            # Use requests built-in auth for standard Basic Auth implementation
            response = requests.get(url, auth=(self.consumer_key, self.consumer_secret), timeout=30)
            
            if response.status_code == 200:
                token = response.json().get('access_token')
                if token:
                    print("M-Pesa Access Token retrieved successfully.")
                    return token
                else:
                    print("M-Pesa Error: access_token missing in 200 OK response.")
                    return None
            else:
                # Log full details to diagnose 400/401 errors
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
