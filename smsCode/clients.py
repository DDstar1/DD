from FiverrService import Check
from sms_inbip import SMS

# Stores all the client and their details details
clients = [
    {
        "name": "Abhuluimen Oseremen Destiny",
        "phone": "2348164078594",
        "sms_sender": "FIVERR",
        "srch_fr": "You've received messages from",
        "tkn_pth": "tokens/client1.json",
        "gmail": "oseseo9@gmail.com",
        "service": "fiverr",
    }
]


# This is the main function which runs the entire codebase
# it loops through all the clients and input their details into the Check function from the FiverService file
def main():
    for client in clients:
        name = client["name"]
        phone = client["phone"]
        sms_sender = client["sms_sender"]
        srch_fr = client["srch_fr"]
        CLIENT_SECRET_FILE = client["tkn_pth"]

        if client["service"] == "fiverr":
            try:
                # inputs clients details into the fiverr check file
                Check(
                    phone=phone,
                    srch_fr=srch_fr,
                    sms_sender=sms_sender,
                    CLIENT_SECRET_FILE=CLIENT_SECRET_FILE,
                )
            except Exception as e:
                # this send an sms msg to the developer when an error occurs during any clients process
                SMS(
                    MESSAGE_TEXT=f"An error occured during { name }'s gmail process... Error code = {e}",
                    RECIPIENT="2348164078594",
                    SENDER="ERROR",
                )


main()
