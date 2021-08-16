# https://github.com/KimigaiiWuyi/GenshinUID

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import *
from graia.application.event.mirai import *
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import RegexMatch
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import Plain, Image
from graia.application.message.elements.internal import MessageChain
import re
import base64
from .getImg import draw_pic, draw_char_pic


# 插件信息
__name__ = "GenshinUID"
__description__ = "原神UID查询"
__author__ = "Wuyi无疑(由Roc迁移至saya)"
__usage__ = (
    "发送 “uid”+9位UID 即可，如 “uid188448501”"
)


saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


def gen_messageChain(content):
    msg = []
    b64 = re.findall(r'base64://(.*?)$', content)
    if b64:
        imgdata=base64.b64decode(b64[0])
        msg.append(Image.fromUnsafeBytes(imgdata))
    else:
        msg.append(Plain(content))
    return MessageChain.create(msg)


@channel.use(ListenerSchema(listening_events=[GroupMessage], inline_dispatchers=[Kanata([RegexMatch('uid.*')])]))
async def group_message_listener(app: GraiaMiraiApplication, message: MessageChain, member: Member, group: Group):
    plain = message.getFirst(Plain) if message.has(Plain) else ""
    plain = plain.asDisplay().replace('uid', '')
    uid = re.findall(r"\d+", plain)[0]  # str
    m = ''.join(re.findall('[\u4e00-\u9fa5]', plain))

    try:
        if m == "角色":
            content = await draw_char_pic(uid, member.name)
        else:
            content = await draw_pic(uid, member.name)
    except:
        content = '输入错误！'

    msg = gen_messageChain(content)
    try:
        await app.sendGroupMessage(group, msg)
    except:
        pass
