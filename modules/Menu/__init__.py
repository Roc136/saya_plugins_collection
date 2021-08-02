from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import *
from graia.application.event.mirai import *
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import Plain
from graia.application.message.elements.internal import MessageChain
from .config import menus


# 插件信息
__name__ = "DrawSomething"
__description__ = "自定义菜单"
__author__ = "Roc"
__usage__ = "群内发送“菜单”或“功能”获取机器人全部功能指令"


saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_message_listener(app:GraiaMiraiApplication, message: MessageChain, group: Group):
    if menus.has_key(message.asDisplay()):
        msg = MessageChain.create([Plain(menus[message.asDisplay()])])
        await app.sendGroupMessage(
            group, msg
        )
    return
