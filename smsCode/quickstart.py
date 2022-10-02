# Quickstart file is directly from google gmail api
# it builds the client gmail objects when the token is found or created
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES):

    # If modifying these scopes, delete the file token.json.

    SCOPES = SCOPES

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(CLIENT_SECRET_FILE):
        creds = Credentials.from_authorized_user_file(CLIENT_SECRET_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # with open(CLIENT_SECRET_FILE, "w") as token:
        #     token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build(API_NAME, API_VERSION, credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        print("Labels:")
        for label in labels:
            print(label["name"])

        print(service)
        return service

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
