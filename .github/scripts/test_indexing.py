import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Read JSON string from the GitHub secret
google_json = os.environ.get("GOOGLE_JSON")

if not google_json:
    raise ValueError("❌ GOOGLE_JSON secret is missing!")

try:
    # Convert string to dict
    service_account_info = json.loads(google_json)
except json.JSONDecodeError as e:
    raise ValueError(f"❌ GOOGLE_JSON is not valid JSON: {e}")

# Create credentials
try:
    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/indexing"]
    )
    print("✅ Google credentials loaded successfully")
except Exception as e:
    raise RuntimeError(f"❌ Failed to initialize Google API client: {e}")

# Build the Indexing API service
service = build("indexing", "v3", credentials=creds)

# Test URL
url = "https://aymansalem.github.io/"  # Replace with any test URL
response = service.urlNotifications().publish(
    body={"url": url, "type": "URL_UPDATED"}
).execute()

print("📢 Indexing API response:", response)
