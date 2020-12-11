from fbchat import Client, log
from fbchat.models import *
import apiai, codecs, json

class chatS(Client):
    
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "Access token code"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'en'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
        
    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None, **kwargs):
        
        # self.markAsRead(author_id)

        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))

        self.apiaiCon()

        msgText = message_object.text

        self.request.query = msgText

        response = self.request.getresponse()

        obj = json.load(response)

        reply = obj['result']['fulfillment']['speech']

        if author_id != self.uid:
             self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

        self.markAsDelivered(author_id, thread_id)

Client = chatS("email", "password")
Client.listen()