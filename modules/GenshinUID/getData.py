# https://github.com/Womsxd/YuanShen_User_Info

from httpx import AsyncClient
import json
import requests,random,json
import time
import string
import random
import hashlib
import requests
from .config import *


def cache_Cookie():
    return random.choice(cookie_list)


def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def DSGet():
    n = "fd3ykrh7o1j54g581upo1tvpam0dsgtf"
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return (i + "," + r + "," + c)

async def GetInfo(Uid, ServerID="cn_gf01",Schedule_type="1"):
    if Uid[0] == '5':
        ServerID = "cn_qd01"
    try:
        async with AsyncClient() as client:
            req = await client.get(
                url="https://api-takumi.mihoyo.com/game_record/genshin/api/index?server=" + ServerID + "&role_id=" + Uid,
                headers={
                    'Accept': 'application/json, text/plain, */*',
                    'DS': DSGet(),
                    'Origin': 'https://webstatic.mihoyo.com',
                    'x-rpc-app_version': mhyVersion,
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                    'x-rpc-client_type': '2',
                    'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'X-Requested-With': 'com.mihoyo.hyperion',
                    "Cookie": cache_Cookie()})
            data1 = json.loads(req.text)
        async with AsyncClient() as client:
            req = await client.get(
                url="https://api-takumi.mihoyo.com/game_record/genshin/api/spiralAbyss?schedule_type=" + Schedule_type + "&server="+ ServerID +"&role_id=" + Uid,
                headers={
                    'Accept': 'application/json, text/plain, */*',
                    'DS': DSGet(),
                    'Origin': 'https://webstatic.mihoyo.com',
                    'Cookie': cache_Cookie(),               
                    'x-rpc-app_version': mhyVersion,
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                    'x-rpc-client_type': '2',
                    'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'X-Requested-With': 'com.mihoyo.hyperion'
                    }
                )
            data2 = json.loads(req.text)
        data = data1
        #f=open("/root/hoshino/HoshinoBot/hoshino/modules/GenshinUID/mys/chars/666.txt",'w') 
        #f.write(str(data))
        return data

    except:
        print("访问失败，请重试！")
        # sys.exit(1)
        return None

async def GetCharacter(Uid,Character_ids, ServerID="cn_gf01"):
    if Uid[0] == '5':
        ServerID = "cn_qd01"
    try:
        req = requests.post(
            url = "https://api-takumi.mihoyo.com/game_record/genshin/api/character",
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'DS': DSGet(),
                'Origin': 'https://webstatic.mihoyo.com',
                'Cookie': cache_Cookie(),
                'x-rpc-app_version': mhyVersion,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                'x-rpc-client_type': '2',
                'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'X-Requested-With': 'com.mihoyo.hyperion'
            },
            json = {"character_ids": Character_ids ,"role_id": Uid ,"server": ServerID }
        )
        data2 = json.loads(req.text)
        #f=open("/root/hoshino/HoshinoBot/hoshino/modules/GenshinUID/mys/chars/555.txt",'w') 
        #f.write(str(data2))
        return data2

    except:
        print ("访问失败，请重试！")
        #sys.exit (1)
        return None