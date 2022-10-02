from quickstart import main
import re
from sms_inbip import SMS

import smtplib
from email.message import EmailMessage


API_VERSION = "v1"
API_NAME = "gmail"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://mail.google.com/"]
sentSmsId = ""


# this function houses the other functions for the cause of avoiding being run when imported to another file
def Check(
    phone=None, srch_fr=None, tkn_pth=None, sms_sender=None, CLIENT_SECRET_FILE=None
):

    # this connects with the client gmail account with the details from the client file
    service = main(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # this is the list of mesgs to be sent when the gmail crawling is done
    toBeSent = []

    # this function checks the gmail account for the sms_already_sent tag(label)
    def check_fr_sentsms_label():

        global sentSmsId
        check = False
        msg = service.users().labels().list(userId="me").execute()
        all_labels = msg["labels"]

        for labels in all_labels:
            # checks if we already have sent_sms label in person email labels
            if labels["name"] == "sent_sms":
                check = True

        if check == False:
            # creates label if we don't
            label = {
                "labelListVisibility": "labelShow",
                "messageListVisibility": "hide",
                "name": "sent_sms",
            }
            msg = service.users().labels().create(userId="me", body=label).execute()
            print(label)

        # get label_id for sent_sms
        msg = service.users().labels().list(userId="me").execute()
        all_label = msg["labels"]

        # this gets the sms_sent label id
        for label in all_label:
            if label["name"] == "sent_sms":
                sentSmsId = label["id"]
                print(sentSmsId)
                break

    # this function checks for the text the client is looking for in their gmail
    def has_headers_fiverr2(id):
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=id, format="metadata")
            .execute()
        )
        headers_list = msg["payload"]["headers"]
        to_match = [i["value"] for i in headers_list if i["name"] == "From"]
        to_match = to_match[0]

        pattern = re.compile(r"fiverr")
        match = pattern.search(to_match)

        if match != None:
            return True

    # this function checks whether the email already has the already sent_sms label
    def check_msg_labels(id):
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=id, format="minimal")
            .execute()
        )
        headers_list = msg["labelIds"]
        print(headers_list)
        for headers in headers_list:
            if headers == sentSmsId:
                print(sentSmsId)
                return True

    # this function checks whether the main text is among the headers of the email
    def read_headers_fiverr(id):
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=id, format="metadata")
            .execute()
        )
        headers_list = msg["payload"]["headers"]
        subject = [i["value"] for i in headers_list if i["name"] == "Subject"]
        date = [i["value"] for i in headers_list if i["name"] == "Date"]
        msg = subject[0] + " on " + date[0]
        toBeSent.append(msg)

    # this function adds the already sent_sms label to sent msg that havent being sent before
    def add_smssent_tag(id):
        post_data = {"addLabelIds": [sentSmsId]}
        service.users().messages().modify(
            userId="me",
            id=id,
            body=post_data,
        ).execute()
        print("DONE")
        print(id)

    # this is the main function that processes each mails
    def process_mails():
        check_fr_sentsms_label()
        msg = service.users().messages().list(userId="me", q=srch_fr).execute()
        msg = msg["messages"]

        id_list = [i["id"] for i in msg]
        id_list_1 = []
        id_list_2 = []

        # this checks all the gotten mails and put those that have the important headers in a new list
        for c in id_list:
            if has_headers_fiverr2(c):
                id_list_1.append(c)

        print(id_list_1)

        # this checks the new list and put those that dont have the sent_sms label in a new list
        for c in id_list_1:
            if not check_msg_labels(c):
                id_list_2.append(c)

        print(id_list_2)

        if id_list_2 != []:
            # this reads all the mails that passed all the test
            for id in id_list_2:
                read_headers_fiverr(id)

            # this sends the sms to the clients
            for msg in toBeSent:
                SMS(MESSAGE_TEXT=msg, RECIPIENT=phone, SENDER=sms_sender)

            print(toBeSent)

            # then this adds the sent_sms label so they wont be sent again when the code is run
            for id in id_list_2:
                add_smssent_tag(id)

            print(f"THERE WERE {len(id_list_2)} ID found")

        else:
            print("THERE WERE NO IDs FOUND")

    process_mails()


if __name__ == "__main__":
    Check()
