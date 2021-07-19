import aiohttp

from graia.application.message.elements.internal import Plain
from utils import messagechain_to_img
from graia.application import GraiaMiraiApplication
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import RegexMatch
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import *
from graia.application.event.mirai import *
from graia.application.exceptions import AccountMuted
from graia.application.message.elements.internal import MessageChain
from urllib.request import quote
import re

# 插件信息
__name__ = "WeiboHotSearch"
__description__ = "获取当前微博热搜"
__author__ = "SAGIRI-kawaii"
__usage__ = "在群内发送 微博热搜 即可"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


@channel.use(ListenerSchema(listening_events=[GroupMessage], inline_dispatchers=[Kanata([RegexMatch('微博热搜([0-9]*)$')])]))
async def group_message_listener(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    re_res = re.match("微博热搜([0-9]*)$", message.asDisplay())
    num = 0
    if re_res and re_res.group(1) != "":
        num = int(re_res.group(1))
    try:
        await app.sendGroupMessage(
            group,
            await get_weibo_hot(num, "text" if num > 0 else "img")
        )
    except AccountMuted:
        print("passed")
        pass
    except Exception as e:
        print(e)


async def get_weibo_hot(num: int = 0, display: str = "img") -> MessageChain:
    url = "http://api.weibo.cn/2/guest/search/hot/word"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            data = await resp.json()
    data = data["data"]
    text_list = ["微博实时热榜:"]
    index = 0
    for i in data:
        index += 1
        text_list.append(i["word"].strip())
    if num == 0:
        text = "微博实时热榜:"
        for i, v in enumerate(text_list[1:]):
            text += "\n%d. %s" % (i + 1, v.replace("#", ""))
    elif num < len(text_list):
        text = "\n%d. %s" % (num, text_list[num].replace("#", ""))
        url_tmp = f"https://weibo.com/search?containerid=100103type%3D1%26q%3D%23{ text_list[num] }%23%26t%3D3"
        text += "\n" + quote(url_tmp, safe=";/?:@&=+$,", encoding="utf-8")
    else:
        text = "数字超出范围"
    msg = MessageChain.create([
        Plain(text=text)
    ])
    if display == "img":
        return await messagechain_to_img(msg)
    elif display == "text":
        return msg
    else:
        raise ValueError("Invalid display value!")
