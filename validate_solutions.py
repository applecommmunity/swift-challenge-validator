import os
import json
import gspread
import requests
import subprocess
from google.oauth2.service_account import Credentials

# Load Google API credentials
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict)
client = gspread.authorize(creds)

# Google Sheet and Drive IDs
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

# Open the submission sheet
sheet = client.open_by_key(SHEET_ID).worksheet("Form Responses 1")
submissions = sheet.get_all_values()

# Process each submission
for i, row in enumerate(submissions[1:], start=2):
    file_url = row[4]  # Column E - File URL
    challenge_day = f"test_day{i}.swift"
    
    if "drive.google.com" in file_url:
        # Extract file ID from URL
        file_id = file_url.split("id=")[-1]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        response = requests.get(download_url)
        if response.status_code == 200:
            with open("submission.swift", "wb") as f:
                f.write(response.content)

            # Run Swift test case
            test_file = os.path.join(os.getcwd(), "test_cases", challenge_day)
            result = subprocess.run(["swift", test_file, "submission.swift"], capture_output=True, text=True)
            
            # Determine pass/fail
            status = "Pass" if "Test Passed" in result.stdout else "Fail"
            sheet.update_cell(i, 7, status)  # Update Column G

