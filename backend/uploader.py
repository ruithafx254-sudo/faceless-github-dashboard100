import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(file_path, client_secret_file):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret_file, SCOPES)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Viral Fact! 🤯",
                "description": "Subscribe for more faceless content!",
                "tags": ["viral", "facts", "shorts"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=file_path
    )
    request.execute()
    print(f"✅ Uploaded {file_path}")
