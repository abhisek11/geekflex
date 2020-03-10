from django.shortcuts import render

from notifiyapp.models import *
from urllib.request import Request, urlopen
import urllib
import json
from django.conf import settings
import requests

from django.template import Context,Template

class GlobleNotifiyFCM(object):
    def __init__(self,code,recipient_list:list):
        super(GlobleNotifiyFCM, self).__init__()
        self.code = code
        self.recipient_list = recipient_list

    def sendSMS(self,notify_data:dict,type):
        notify_content = NotifyTemplet.objects.get(code = self.code)
        contain_variable = notify_content.contain_variable.split(",")
        txt_content = Template(notify_content.txt_content)
        match_data_dict = {}
        for data in contain_variable:
            if data.strip() in notify_data:
                match_data_dict[data.strip()] = notify_data[data.strip()]

        if match_data_dict:
            context_data = Context(match_data_dict)
            txt_content = txt_content.render(context_data)

        
        data =  urllib.parse.urlencode({
                "name": "my_notification",
                "notification":{
                    "title":"Notification title 11",
                    "body":"Notification body 11",
                    "sound":"default",
                    "click_action":"FCM_PLUGIN_ACTIVITY",
                    "icon":"fcm_push_icon"
                },
                "data":{
                    "param1":"Check the discount price",
                    "param2":"12.00",
                    "notification_foreground": "true"
                },
                "to":"eVSChYlsiRU:APA91bHABMiX1nPH_1lsjFCz74pABu5JiOjCct8uAd1m3L7NvtfUpdVeOsBrGueGybTtzl41i_FNbWiyBGZsQ4w65ppN3xSdAaPWxfj3XbwSAaIXhWxc0gcParJ_JZvckOwWiZzUKtRK",
                "priority":"high",
                "restricted_package_name":""
                }
            )
        data = data.encode('utf-8')
        request = urllib.request.Request("https://fcm.googleapis.com/fcm/send")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        print('fr',fr)



#######################3
message_data = {
                "title":"Notification title 11",
                "body":"Notification body 11",
                "to":"eVSChYlsiRU:APA91bHABMiX1nPH_1lsjFCz74pABu5JiOjCct8uAd1m3L7NvtfUpdVeOsBrGueGybTtzl41i_FNbWiyBGZsQ4w65ppN3xSdAaPWxfj3XbwSAaIXhWxc0gcParJ_JZvckOwWiZzUKtRK",
                }
sms_class = GlobleNotifiyFCM('OTP-V',[mobile_number])
sms_thread = Thread(target = sms_class.sendSMS, args = (message_data,'sms'))
sms_thread.start()