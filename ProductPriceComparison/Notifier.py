import env
import time
from getEbayPrice import getProductPrice
import requests
import bs4
import boto3
from plyer import notification

product_url = 'https://www.staples.com/Staples-Hyken-Technical-Mesh-Task-Chair-Black/product_990119'
html_selector = '#priceInfoContainer > div > div.price-info__final_price'
target_price = 170
'''
subject = '(IN STOCK!) ' + product_name[:20]+'...'
message = 'Price is $' + product_price + '\n'
    + 'Click here: ' + product_url
title = product_name,
message = 'PRICE IS: '+ product_price,
'''

def main():
    while True:
        product_price, product_name = getProductPrice(product_url)
        print(product_price)
        notifyDesktop(product_price, product_name)
        if float(product_price) <= target_price:
            notifyPhoneEmail(product_price, product_name)
        
        time.sleep(60*60)

def notifyDesktop(desktop_title, desktop_message):
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

def notifyPhoneEmail(aws_subject, aws_message):
    arn = 'arn:aws:sns:us-east-2:447523202168:ProductNotifier'
    sns_client = boto3.client(
        'sns',
        aws_access_key_id = env.accessKey,
        aws_secret_access_key = env.secretKey,
        region_name = 'us-east-2'
    )
    response = sns_client.publish(TopicArn=arn, Message=aws_message, Subject=aws_subject)
    print(response)

#def notifyOrderPlaced(product_price):