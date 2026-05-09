import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from flask import Flask, request, jsonify
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
import asyncio
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# TELEGRAM BOT SETUP
TELEGRAM_BOT_TOKEN = " Thay token bot tellle"  # BotFather থেকে নেওয়া টোকেন দিন
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Encrypted Credit Info - DO NOT REMOVE
_Xk9mN3pL5vR8wQ2 = "e3tZWV1bR0dDWVlbWVhYWFlYWF1cW1tbX19fXFxZWkdHQ1lZW1lYWFhZWFldXFtbWV1ZXFxaWkdHQ1lZW1lb"
_Yt4jH7qW2sD6fB1 = "WFhYWkdGRFlYV1laR0Q="
_Zc8vN5mL4pR7wS3 = "WFdZWkdEWVhXWVpHRA=="
_A1bC3dE5fG7hI9k = "WFhYWFhYWFhYWEtHWFhYVkpFRFlYWFhYWFhYWFhZR0RYWFhYWEdEWA=="

def _dEcOdE_cReDiT():
    """Internal credit decoder - DO NOT MODIFY"""
    try:
        _key = "MaFuCrEdIt2024"
        _d1 = base64.b64decode(_Xk9mN3pL5vR8wQ2.encode()).decode()
        _d2 = base64.b64decode(_Yt4jH7qW2sD6fB1.encode()).decode()
        _d3 = base64.b64decode(_Zc8vN5mL4pR7wS3.encode()).decode()
        _d4 = base64.b64decode(_A1bC3dE5fG7hI9k.encode()).decode()
        
        _result = {}
        _result['developer'] = ''.join(chr(ord(c) ^ ord(_key[i % len(_key)])) for i, c in enumerate(_d1))
        _result['main_channel'] = ''.join(chr(ord(c) ^ ord(_key[i % len(_key)])) for i, c in enumerate(_d2))
        _result['api_channel'] = ''.join(chr(ord(c) ^ ord(_key[i % len(_key)])) for i, c in enumerate(_d3))
        _result['bot_channel'] = ''.join(chr(ord(c) ^ ord(_key[i % len(_key)])) for i, c in enumerate(_d4))
        return _result
    except:
        return {}

CREDIT_INFO = _dEcOdE_cReDiT()
# End of Encrypted Credit Info

# Variables
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
BOT_UID = None
key = None
iv = None
region = None
TarGeT = None
acc_name = None
#------------------------------------------#

app = Flask(__name__)

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB53"}

# ---- Random Colors ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

# ---- Telegram Bot Functions ----
async def send_telegram_message(chat_id, text):
    """টেলিগ্রামে মেসেজ পাঠানোর ফাংশন"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

async def send_telegram_buttons(chat_id, text, buttons):
    """বাটন সহ মেসেজ পাঠানোর ফাংশন"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    keyboard = {"inline_keyboard": buttons}
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": json.dumps(keyboard),
        "parse_mode": "HTML"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

async def process_telegram_command(update):
    """টেলিগ্রাম কমান্ড প্রসেস করার ফাংশন"""
    global online_writer, BOT_UID, key, iv, region, TarGeT, acc_name
    
    if "message" not in update:
        # Callback query (বাটন ক্লিক)
        if "callback_query" in update:
            callback = update["callback_query"]
            chat_id = callback["message"]["chat"]["id"]
            data = callback["data"]
            
            # বাটন ক্লিকের জবাব
            await answer_callback(callback["id"])
            
            if data == "status":
                status = "🟢 Online" if online_writer else "🔴 Connecting"
                await send_telegram_message(chat_id, f"<b>🤖 Bot Status</b>\n\n"
                                                     f"Status: {status}\n"
                                                     f"Target UID: {TarGeT}\n"
                                                     f"Bot Name: {acc_name}\n"
                                                     f"Region: {region}\n"
                                                     f"Bot UID: {BOT_UID}")
            
            elif data == "invite_5":
                await send_telegram_message(chat_id, "<b>5️⃣ Player Invite</b>\n\n"
                                                     "Send UID using:\n"
                                                     "<code>/5 UID</code>")
            
            elif data == "invite_6":
                await send_telegram_message(chat_id, "<b>6️⃣ Player Invite</b>\n\n"
                                                     "Send UID using:\n"
                                                     "<code>/6 UID</code>")
            
            elif data == "menu":
                await send_main_menu(chat_id)
        return
    
    message = update["message"]
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    
    # টেক্সট মেসেজ চেক
    text = message.get("text", "")
    
    if text.startswith("/start"):
        await send_main_menu(chat_id)
    
    elif text.startswith("/status"):
        status = "🟢 Online" if online_writer else "🔴 Connecting"
        await send_telegram_message(chat_id, f"<b>🤖 Bot Status</b>\n\n"
                                             f"Status: {status}\n"
                                             f"Target UID: {TarGeT}\n"
                                             f"Bot Name: {acc_name}\n"
                                             f"Region: {region}\n"
                                             f"Bot UID: {BOT_UID}")
    
    elif text.startswith("/5"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message(chat_id, "❌ <b>Usage:</b> <code>/5 UID</code>")
            return
        
        target_uid = parts[1]
        try:
            target_uid = int(target_uid)
        except:
            await send_telegram_message(chat_id, "❌ Invalid UID format")
            return
        
        if online_writer is None:
            await send_telegram_message(chat_id, "❌ Bot is not connected yet!")
            return
        
        await send_telegram_message(chat_id, f"⏳ <b>Sending 5-Player Invite to {target_uid}...</b>")
        try:
            await perform_invite_5(target_uid)
            await send_telegram_message(chat_id, f"✅ <b>5-Player Invite Sent to {target_uid}!</b>")
        except Exception as e:
            await send_telegram_message(chat_id, f"❌ Error: {str(e)}")
    
    elif text.startswith("/6"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message(chat_id, "❌ <b>Usage:</b> <code>/6 UID</code>")
            return
        
        target_uid = parts[1]
        try:
            target_uid = int(target_uid)
        except:
            await send_telegram_message(chat_id, "❌ Invalid UID format")
            return
        
        if online_writer is None:
            await send_telegram_message(chat_id, "❌ Bot is not connected yet!")
            return
        
        await send_telegram_message(chat_id, f"⏳ <b>Sending 6-Player Invite to {target_uid}...</b>")
        try:
            await perform_invite_6(target_uid)
            await send_telegram_message(chat_id, f"✅ <b>6-Player Invite Sent to {target_uid}!</b>")
        except Exception as e:
            await send_telegram_message(chat_id, f"❌ Error: {str(e)}")
    
    elif text.startswith("/help"):
        await send_telegram_message(chat_id, "<b>📚 Available Commands:</b>\n\n"
                                             "/start - Show Main Menu\n"
                                             "/status - Check Bot Status\n"
                                             "/5 UID - Send 5-Player Invite\n"
                                             "/6 UID - Send 6-Player Invite\n"
                                             "/help - Show This Help")

async def send_main_menu(chat_id):
    """মেইন মেনু পাঠানোর ফাংশন"""
    await send_telegram_message(chat_id, 
        f"<b>🤖 Bot By Mafu - Control Panel</b>\n\n"
        f"Bot Name: {acc_name}\n"
        f"Target: {TarGeT}\n"
        f"Status: {'🟢 Online' if online_writer else '🔴 Connecting'}\n\n"
        f"<b>📚 Available Commands:</b>\n\n"
        f"/start - Show Main Menu\n"
        f"/status - Check Bot Status\n"
        f"/5 UID - Send 5-Player Invite\n"
        f"/6 UID - Send 6-Player Invite\n"
        f"/help - Show This Help")

async def answer_callback(callback_id):
    """কলব্যাকের জবাব দেয়া"""
    url = f"{TELEGRAM_API_URL}/answerCallbackQuery"
    payload = {"callback_query_id": callback_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

async def telegram_polling():
    """টেলিগ্রাম থেকে আপডেট নেওয়ার ফাংশন (লং পোলিং)"""
    offset = 0
    print("🤖 Telegram Bot Started - Polling for updates...")
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                url = f"{TELEGRAM_API_URL}/getUpdates"
                params = {"offset": offset, "timeout": 30}
                
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    
                    if data.get("ok") and data.get("result"):
                        for update in data["result"]:
                            offset = update["update_id"] + 1
                            await process_telegram_command(update)
                            
            except Exception as e:
                print(f"Telegram polling error: {e}")
                await asyncio.sleep(5)

# Original encrypted_proto and other functions remain the same
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 4
    major_login.client_version = "1.123.2"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "vn"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHT1r9GNgPJ0nDb82dJ+mJ4wwzqfR9fk7HviQ+4tx58ObceZuLaFrmk9qaVIP+qB3CV0DG40yTeS+2h1GA1rqKtMVPLfDUz7rIThfm4ZKedCh3="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggpolarbear.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 
           
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        print(data2.hex()[10:])
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        print(packet)
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)

                        message = f'[B][C]{get_random_color()}\n- WeLComE To Bot ! '
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)

                    except:
                        if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                            try:
                                print(data2.hex()[10:])
                                packet = await DeCode_PackEt(data2.hex()[10:])
                                print(packet)
                                packet = json.loads(packet)
                                OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                                JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)

                                message = f'[B][C]{get_random_color()}\n- WeLComE To Bot ! \n\n[00FF00]Dev : @{xMsGFixinG("DEVXTLIVE")}'
                                P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                            except:
                                pass

            online_writer.close() ; await online_writer.wait_closed() ; online_writer = None

        except Exception as e: print(f"- ErroR With {ip}:{port} - {e}") ; online_writer = None
        await asyncio.sleep(reconnect_delay)
                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                # Chat reading only - no command processing
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# ---------------------- FLASK ROUTES ----------------------

loop = None

async def perform_invite_5(target_uid: int):
    global key, iv, region, online_writer, BOT_UID
    
    if online_writer is None:
        raise Exception("Bot not connected")
    
    try:
        # Open Squad
        PAc = await OpEnSq(key, iv, region)
        await SEndPacKeT(None, online_writer, 'OnLine', PAc)
        
        # Change Squad to 5-player mode
        C = await cHSq(5, target_uid, key, iv, region)
        await asyncio.sleep(0.3)
        await SEndPacKeT(None, online_writer, 'OnLine', C)
        
        # Send Invite
        V = await SEnd_InV(5, target_uid, key, iv, region)
        await asyncio.sleep(0.3)
        await SEndPacKeT(None, online_writer, 'OnLine', V)
        
        # Exit Squad after delay
        await asyncio.sleep(5)
        E = await ExiT(BOT_UID, key, iv)
        await SEndPacKeT(None, online_writer, 'OnLine', E)
        
        return {"status": "success", "message": f"5-Player invite sent to {target_uid}"}
        
    except Exception as e:
        raise Exception(f"Failed to send 5-player invite: {str(e)}")

async def perform_invite_6(target_uid: int):
    global key, iv, region, online_writer, BOT_UID
    
    if online_writer is None:
        raise Exception("Bot not connected")
    
    try:
        # Open Squad
        PAc = await OpEnSq(key, iv, region)
        await SEndPacKeT(None, online_writer, 'OnLine', PAc)
        
        # Change Squad to 6-player mode
        C = await cHSq(6, target_uid, key, iv, region)
        await asyncio.sleep(0.3)
        await SEndPacKeT(None, online_writer, 'OnLine', C)
        
        # Send Invite
        V = await SEnd_InV(6, target_uid, key, iv, region)
        await asyncio.sleep(0.3)
        await SEndPacKeT(None, online_writer, 'OnLine', V)
        
        # Exit Squad after delay
        await asyncio.sleep(5)
        E = await ExiT(BOT_UID, key, iv)
        await SEndPacKeT(None, online_writer, 'OnLine', E)
        
        return {"status": "success", "message": f"6-Player invite sent to {target_uid}"}
        
    except Exception as e:
        raise Exception(f"Failed to send 6-player invite: {str(e)}")

@app.route('/5')
def invite_5_player():
    global loop
    target_uid_str = request.args.get('uid')

    if not target_uid_str:
        return jsonify({"status": "error", "message": "Missing uid"}), 400

    try:
        target_uid = int(target_uid_str)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid UID format"}), 400

    asyncio.run_coroutine_threadsafe(
        perform_invite_5(target_uid), loop
    )

    return jsonify({
        "status": "bot by mafu success",
        "target_uid": target_uid,
        "message": "5-Player Invite Sent!"
    })

@app.route('/6')
def invite_6_player():
    global loop
    target_uid_str = request.args.get('uid')

    if not target_uid_str:
        return jsonify({"status": "error", "message": "Missing uid"}), 400

    try:
        target_uid = int(target_uid_str)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid UID format"}), 400

    asyncio.run_coroutine_threadsafe(
        perform_invite_6(target_uid), loop
    )

    return jsonify({
        "status": "bot by mafu success",
        "target_uid": target_uid,
        "message": "6-Player Invite Sent!"
    })

@app.route('/')
def health_check():
    return jsonify({
        "status": "bot by mafu alive",
        "bot": "online" if online_writer else "connecting",
        "service": "bot by mafu Free Fire Bot API - 5/6 Player Invite",
        "timestamp": str(datetime.now())
    })

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ---------------------- MAIN BOT SYSTEM ----------------------

async def MaiiiinE():
    global loop, key, iv, region, BOT_UID, TarGeT, acc_name

    # BOT LOGIN UID
    BOT_UID = int('15509918760')

    Uid, Pw = '4748733430', 'm4statusdevBYSTARGMRYa56kJNI'

    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token:
        print("ErroR - InvaLid AccounT")
        return None

    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE:
        print("TarGeT AccounT => BannEd / NoT ReGisTeReD !")
        return None

    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    print(UrL)
    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp

    loop = asyncio.get_running_loop()

    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa:
        print("ErroR - GeTinG PorTs From LoGin DaTa !")
        return None

    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port

    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")

    acc_name = LoGinDaTaUncRypTinG.AccountName
    print(ToKen)

    equie_emote(ToKen, UrL)

    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()

    task1 = asyncio.create_task(
        TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv,
                LoGinDaTaUncRypTinG, ready_event, region)
    )

    await ready_event.wait()
    await asyncio.sleep(1)

    task2 = asyncio.create_task(
        TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen)
    )

    os.system('clear')
    print(render('DEV', colors=['white', 'green'], align='center'))
    print(f"\n - BoT STarTinG And OnLine on TarGet : {TarGeT} | BOT NAME : {acc_name}")
    print(" - BoT sTaTus > GooD | OnLinE ! (: \n")
    print(" - API Routes: /5?uid=UID  |  /6?uid=UID")
    print(" - Telegram Bot: Active!")

    await asyncio.gather(task1, task2)

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("Token ExpiRed ! , ResTartinG")
        except Exception as e:
            print(f"ErroR TcP - {e} => ResTarTinG ...")

async def main():
    """Main function to run everything together"""
    # Start Flask in a thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start Telegram bot polling as a task
    telegram_task = asyncio.create_task(telegram_polling())
    
    # Start the bot system
    bot_task = asyncio.create_task(StarTinG())
    
    # Wait for both tasks
    await asyncio.gather(telegram_task, bot_task)

if __name__ == '__main__':
    print("🤖 bot by mafu starting...")
    print("📡 Starting Flask API Server...")
    print("📱 Starting Telegram Bot...")
    print("🎮 Starting Free Fire Bot...")
    
    asyncio.run(main())