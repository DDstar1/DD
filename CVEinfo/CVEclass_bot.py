import requests
from smsEmail import SMS ,sendMeMail
from people import recipients

chatID = ''

def Main():
    data_url = 'https://api.telegram.org/bot5411267100:AAEUk5WnaL5nLaAa9I2JPxcZZhWYfY-KPk4/getUpdates'
    sendMsg = 'https://api.telegram.org/bot5411267100:AAEUk5WnaL5nLaAa9I2JPxcZZhWYfY-KPk4/sendMessage'
    parameters = {
        'limit': '100',
    }

    def get_gc_id():
        global chatID
        msg = requests.get(data_url, data=parameters).json()
        id = msg['result'][-1]['message']['chat']['id']
        chatID = id
        print(id)

    def get_last_update():
        msg = requests.get(data_url, data=parameters).json()
        msg = msg['result'][-1]['message']['text']
        return msg

    def send_message(id):
        parameters = {'chat_id': id,
                    'text': "This message has being sent to all members.\n\nPlease type '/stop so it won't be sent again"}
        msg = requests.get(sendMsg, data=parameters)
        return msg

   
    get_gc_id()
    update = 'FROM CVE INFO GROUP\n\n' + get_last_update()
    
    if ('stop' or '/stop@cveclass_bot') not in update.lower():
        send_message(id='-833108561')
        #or u can make the id dynamic
        SMS().send(msg=update, sender=None, recipients=recipients)
   

try:     
    Main()
except Exception as e:
    sendMeMail(body = f"FROM--CVE INFO BOT \n\n EXCEPTION--{e}")