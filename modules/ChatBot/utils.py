from aiohttp import ClientSession
import json


def load_config(config_file: str = "./modules/ChatBot/config.json") -> dict:
    with open(config_file, 'r', encoding='utf-8') as f:  # 从json读配置
        config = json.loads(f.read())
    for key in config.keys():
        config[key] = config[key].strip() if isinstance(config[key], str) else config[key]
    return config


config = load_config()
print(config)
bot = config['bot']


async def get_reply(msg):
    if bot == 'qingyunke':
        return await get_qingyunke_reply(msg)
    elif bot == 'ruyi':
        return await get_ruyi_reply(msg)


# 青云客机器人，https://api.qingyunke.com
async def get_qingyunke_reply(msg):
    reply = ''
    img_path = None
    voice_path = None

    key = config['qingyunke']['key']
    url= f'http://api.qingyunke.com/api.php?key={ key }&appid=0&msg={ msg }'
    async with ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            reply = json.loads(content.decode('utf-8'))['content'].replace('{br}', '\n')
    
    return ' ' + reply, img_path, voice_path


# 如意机器人，https://ruyi.ai/
async def get_ruyi_reply(msg):
    reply = ''
    img_path = None
    voice_path = None

    appKey = config['ruyi']['appKey']
    userID = config['ruyi']['userID']
    url = f"http://api.ruyi.ai/v1/message?q={ msg }&app_key={ appKey }&user_id={ userID }"
    replys = []
    async with ClientSession() as session:
        async with session.get(url) as response:
            content = await response.json()
            if content['code'] == 0:
                replys = content['result']['intents'][0]['outputs']
    for r in replys:
        if r['type'] == 'dialog':
            reply = r['property']['text']
    
    return ' ' + reply, img_path, voice_path