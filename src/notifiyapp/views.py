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

    def sendSMS(self,sms_data:dict,type):
        sms_content = SmsContain.objects.get(code = self.code)
        contain_variable = sms_content.contain_variable.split(",")
        txt_content = Template(sms_content.txt_content)
        match_data_dict = {}
        for data in contain_variable:
            if data.strip() in sms_data:
                match_data_dict[data.strip()] = sms_data[data.strip()]

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
        request = urllib.request.Request("https://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        print('fr',fr)



#######################3
message_data = {
                        'otp':generate_otp,
                        'phone':mobile_number,

                    }
                    sms_class = GlobleSmsSendTxtLocal('OTP-V',[mobile_number])
                    sms_thread = Thread(target = sms_class.sendSMS, args = (message_data,'sms'))
                    sms_thread.start()