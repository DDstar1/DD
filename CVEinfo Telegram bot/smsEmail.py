import africastalking
import smtplib
from email.message import EmailMessage

class SMS:
    def __init__(self):
		# Set your app credentials
        self.username = "CVEapp"
        self.api_key = "aacf4cf246e4aa97e1e8ae6c5df704ddd21503336f22444652a2804256c4e23c"

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, msg, sender, recipients):
            # Set the numbers you want to send to in international format
            # Recipients musts be a list
            recipients = recipients

            # Set your message
            message = msg;

            # Set your shortCode or senderId
            sender = sender
            try:
				# Thats it, hit send and we'll take care of the rest.
                response = self.sms.send(message, recipients, sender)
                print (response)
                sendMeMail(response.json)
            except Exception as e:
                print ('Encountered an error while sending: %s' % str(e))


def sendMeMail(body):
    # set your email and password
    # please use App Password
    email_address = "oseseo9@gmail.com"
    email_password = "zdctsqyoxxeqzcrx"

    # create email
    msg = EmailMessage()
    msg["Subject"] = "Email subject"
    msg["From"] = email_address
    msg["To"] = "oseseo9@gmail.com"
    msg.set_content(body)

    # send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
        
        
if __name__ == '__main__':
    SMS().send()
    sendMeMail()