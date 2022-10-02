HOW THE PROGRAM WORKS
1) the client.py file is run
2) it then imports the FiverrService.py file and then passes values to it
3) the FiverrService.py file then imports the quickstart file and also passes authentication values to it
4) the quickstart.py file then checks for the gmail tokens in the tokens folder


5) the sms-inbip.py file is imported by both the clients and FiverrService files to send sms messages when an email wants to be sent or an error occurs