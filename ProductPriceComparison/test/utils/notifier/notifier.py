import data_decryption as DD
import time
from getEbayPrice import getProductPrice
import requests
import bs4
import boto3
from plyer import notification

product_url = 'https://www.staples.com/Staples-Hyken-Technical-Mesh-Task-Chair-Black/product_990119'
html_selector = '#priceInfoContainer > div > div.price-info__final_price'
target_price = 170

NATIVE_MTD = 'native'
AWS_MTD = 'aws'

'''
subject = '(IN STOCK!) ' + product_name[:20]+'...'
message = 'Price is $' + product_price + '\n'
    + 'Click here: ' + product_url
title = product_name,
message = 'PRICE IS: '+ product_price,
'''
'''
def main():
    while True:
        product_price, product_name = getProductPrice(product_url)
        print(product_price)
        notifyDesktop(product_price, product_name)
        if float(product_price) <= target_price:
            notifyPhoneEmail(product_price, product_name)
        
        time.sleep(60*60)
'''

def notify_desktop(desktop_title, desktop_message):
    notification.notify(title = desktop_title,
        message = desktop_message,
        app_icon = "Alecive-Flatwoken-Apps-Notifications.ico",
        # the notification stays for 50sec
        timeout  = 50
    )

'''
def notifyPhoneEmail(product_price, product_name):
    arn = 'arn:aws:sns:us-east-2:447523202168:ProductNotifier'
    subject = '(IN STOCK!) ' + product_name[:20]+'...'
    message = 'Price is $' + product_price + '\n'
    + 'Click here: ' + product_url

    sns_client = boto3.client(
        'sns',
        aws_access_key_id = env.accessKey,
        aws_secret_access_key = env.secretKey,
        region_name = 'us-east-2'
    )
    response = sns_client.publish(TopicArn=arn, Message=message, Subject=subject)
    print(response)
'''

def notify_aws_sns(aws_subject, aws_message):
    arn = 'arn:aws:sns:us-east-2:447523202168:ProductNotifier'
    sns_client = boto3.client(
        'sns',
        aws_access_key_id = DD.aws_data.accessKey,
        aws_secret_access_key = DD.aws_data.secretKey,
        region_name = 'us-east-2'
    )
    response = sns_client.publish(TopicArn=arn, Message=aws_message, Subject=aws_subject)
    print(response)


class prodNotification:
    def __init__(self, title, message):
        self.title = title
        self.message = message
        self.notify_method = [NATIVE_MTD, 'test']
        #prodNotification.notify(self)

    @staticmethod
    def notify(self):
        print(self.notify_method)
        print('Testing')
        for method in self.notify_method:
            if 'native' in method:
                print('desktop baby!')
                notify_desktop(self.title, self.message)
            elif 'aws' in method:
                notify_aws_sns(self.title, self.message)
            else:
                print('No method detected!')
        
class notifyNative(prodNotification):
    def __init__(self, title, message):
        super().__init__(title, message)
        self.notify_method = [NATIVE_MTD]

class notifyAWS(prodNotification):
    def __init__(self, title, message):
        super().__init__(title, message)
        self.notify_method = [AWS_MTD]

class notifyCustom(prodNotification):
    def __init__(self, title, message, notify_method):
        super().__init__(title, message)
        if isinstance(notify_method, str):
            self.notify_method = [notify_method]
        else:
            self.notify_method = notify_method


#prodNotification('bitch', 'nigga').notify()
notifyNative('native notification', 'test')
#notifyCustom('desktop class','testing', ['aws','native'])



'''
def testNotifyAll():
    subject = 'Testing'
    message = 'Product 123'
    notifyDesktop(subject, message)
    notifyPhoneEmail(subject, message)

testNotifyAll()
'''

#def notifyOrderPlaced(product_price):