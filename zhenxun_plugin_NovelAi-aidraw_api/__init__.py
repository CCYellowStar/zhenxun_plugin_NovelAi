#真屎山代码
from urllib.parse import urljoin
from PIL import Image as Img
from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent, Event, ActionFailed, PrivateMessageEvent
from utils.message_builder import image
from services.log import logger
from nonebot import on_command
from nonebot.rule import to_me
import ujson as json
from utils.utils import scheduler
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg, ArgStr
from configs.path_config import IMAGE_PATH, DATA_PATH
from configs.config import NICKNAME, Config
from utils.manager import withdraw_message_manager
import aiohttp
import time
from base64 import b64decode, b64encode
import aiofiles
import httpx
import hashlib
import random
import os
import asyncio
import io
from io import BytesIO



__zx_plugin_name__ = "NovelAi作图"
__plugin_usage__ = """
usage：
    使用NovelAi根据关键词作图
    指令：
        na作图 关键字(可选长图、横图最好英文，用英文逗号隔开,也带词库翻译和机翻) (可选带一张图片，带了就是图生图)
        如: na作图 loli,hentai,girl
            na作长图 loli,hentai,girl
            na作横图 loli,hentai,girl [图片]
        
        设置token token(仅主人使用)
        如：设置token X0enPiTDR1145141919810kEhF8pMAgVu4N
        在http://lulu.uedbq.xyz/token获取
        
        需要指定seed请在关键词前面加seed=******,
        
        @机器人发送“更新词库文件”可以更新
     
""".strip()
__plugin_des__ = "使用NovelAi 发送na作图 关键字(最好英文，用英文逗号隔开)来作图"
__plugin_cmd__ = ["NovelAi作图","na作图","作图"]
__plugin_type__ = ("来点好康的",)
__plugin_version__ = 1.0
__plugin_author__ = "CCYellowStar"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__
}

__plugin_cd_limit__ = {
    "cd": 10,
    "rst": "冲慢点..."
}
__plugin_block_limit__ = {"rst": "冲慢点..."}

__plugin_configs__ = {
    "WITHDRAW_nai_MESSAGE": {
        "value": (60, 1),
        "help": "自动撤回，参1：延迟撤回时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (60, 1),
    },
    "DOWNLOAD_nai": {
        "value": True,
        "help": "是否存储下载的图",
        "default_value": True,
    },
    "appid": {
        "value": None,
        "help": "你的 APP ID，在百度翻译的开发者中心里可以找到",
        "default_value": None,
    },
    "key": {
        "value": None,
        "help": "你的密钥，在百度翻译的开发者中心里可以找到",
        "default_value": None,
    },
    "salt": {
        "value": "abc123",
        "help": "随机字符串",
        "default_value": "abc123",
    },
}
URL = ""

i = 0
uTag = "lowres, bad anatomy, bad hands, text, error, missing fingers, multiple legs, leg up, missing leg, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"
json_url = "https://github.com/EhTagTranslation/Database/releases/latest/download/db.text.json"
renshu = 0
tokenpath = f"{DATA_PATH}/NovelAi_token.txt"
filepath = f"{DATA_PATH}/NovelAi_URL.txt"
jsonpath = f"{DATA_PATH}/db.text.json"
api = "http://91.217.139.190:5010"
token = ""
q = asyncio.Queue()
init = True
iniit = False
processing = False

up = on_command("更新词库文件", block=True, priority=5, rule=to_me())
can = on_command("na作图", aliases={"NovelAi作图","novelai作图","na作方图"}, block=True, priority=5)
canH = on_command("na作长图", aliases={"NovelAi作长图","novelai作长图"}, block=True, priority=5)
canW = on_command("na作横图", aliases={"NovelAi作横图","novelai作横图"}, block=True, priority=5)
set_url = on_command("设置token", block=True, permission=SUPERUSER, priority=5)

@can.handle()
async def _(state: T_State, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if msg:
        state["keyword"] = text
        
@can.got("keyword", prompt="请输入关键词！(最好英文，用英文逗号隔开)")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    keyword: str = ArgStr("keyword"),
):
    ss = await img(event)
    W = 512
    H = 512
    S = "Square"
    global q
    global renshu   
    a=[bot,keyword, S, event, ss]
    await q.put(a)
    renshu=renshu+1

    if renshu == 1:
        await asyncio.gather(run())
    else:
        await can.send(f"已为你加入队列，后面还有{renshu-1}人")
    
@canH.handle()
async def _(state: T_State, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if msg:
        state["keyword"] = text
        
@canH.got("keyword", prompt="请输入关键词！(最好英文，用英文逗号隔开)")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    keyword: str = ArgStr("keyword"),
):
    ss = await img(event)
    W = 512
    H = 768
    S = "Portrait"
    global q
    global renshu   
    a=[bot,keyword, S, event, ss]
    await q.put(a)
    renshu=renshu+1

    if renshu == 1:
        await asyncio.gather(run())
    else:
        await can.send(f"已为你加入队列，后面还有{renshu-1}人")

@canW.handle()
async def _(state: T_State, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if msg:
        state["keyword"] = text
        
@canW.got("keyword", prompt="请输入关键词！(最好英文，用英文逗号隔开)")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    keyword: str = ArgStr("keyword"),
):
    ss = await img(event)
    W = 768
    H = 512
    S = "Landscape"
    global q
    global renshu   
    a=[bot,keyword, S, event, ss]
    await q.put(a)
    renshu=renshu+1

    if renshu == 1:
        await asyncio.gather(run())
    else:
        await can.send(f"已为你加入队列，后面还有{renshu-1}人")
    
async def _run(bot, keyword, S, event, imgs):
    global iniit
    global processing

 
    if processing:
        await bot.finish("有图片正在生成，请稍等...")
    try:
        await bot.send_msg(
            user_id=event.user_id if isinstance(event, PrivateMessageEvent) else 0,
            group_id=event.group_id if isinstance(event, GroupMessageEvent) else 0,
            message="开始生成",
        )
        tag = await translate(keyword)
        #tag = keyword
        processing = True 
        try:
            if imgs != []:
                img, seed = await runpicapi(tag, S, imgs)   
            else:
                img, seed = await runapi(tag, S)
        except Exception as e:
            await bot.send_msg(
                user_id=event.user_id if isinstance(event, PrivateMessageEvent) else 0,
                group_id=event.group_id if isinstance(event, GroupMessageEvent) else 0,
                message=f"出错了！ {type(e)}：{e}",
            )
            processing = False
            iniit = True
            return
        for i in range(0,len(img)): 
            Seed ="Seed:"+ str(seed[i])
            msg = image(img[i]) + Seed
            try:
                msg_id = await bot.send_msg(
                    user_id=event.user_id if isinstance(event, PrivateMessageEvent) else 0,
                    group_id=event.group_id if isinstance(event, GroupMessageEvent) else 0,
                    message=msg,
                )
            except ActionFailed:
                await bot.send_msg(
                    user_id=event.user_id if isinstance(event, PrivateMessageEvent) else 0,
                    group_id=event.group_id if isinstance(event, GroupMessageEvent) else 0,
                    message="坏了，这张图色过头了，没发出去！",
                )
                if i==len(img)-1:
                    processing = False
                else:
                    pass
                
            if msg_id:
                withdraw_message_manager.withdraw_message(
                    event,
                    msg_id["message_id"],
                    Config.get_config("zhenxun_plugin_NovelAi-aidraw_api", "WITHDRAW_nai_MESSAGE"),
                )
        processing = False
    except Exception as e:
        await bot.send_msg(
            user_id=event.user_id if isinstance(event, PrivateMessageEvent) else 0,
            group_id=event.group_id if isinstance(event, GroupMessageEvent) else 0,
            message=f"出错了！ {type(e)}：{e}",
        )
        logger.error(f"NovelAi 发送了未知错误 {type(e)}：{e}")
        processing = False
        iniit = True
 
@set_url.handle()
async def _(state: T_State, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if msg:
        state["url"] = text
        
@set_url.got("url", prompt="请输入要设定的token")
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    keyword: str = ArgStr("url"),
):  
    global token
    global iniit
    global tokenpath
    _url = keyword

    async with aiofiles.open(tokenpath, mode='w', encoding='utf-8', errors="ignore") as f:
        await f.write(_url)
    token = _url
    iniit = True
    await set_url.send(f"已设置token为{token}")
    
async def runapi(tag, S):   
    global token
    global init
    if init:
        if os.path.exists(tokenpath):
            async with aiofiles.open(tokenpath, mode='r', encoding='utf-8', errors="ignore") as f:
                token = await f.read()
            init = False
    if token == "":
        raise Exception("请先设置token！") 
    tag = tag + "masterpiece,best quality"
    seed = "-1"
    params = {
        "token": token,
        "tags": tag,
        "shape": S,
        "strength": 0.69,
    }
    if tag[:5] == "Seed:" or tag[:5] == "seed:" or tag[:5] == "Seed=" or tag[:5] == "seed=":
        [str1, str2] = tag.split(",",1)
        params = {
            "token": token,
            "tags": str2,
            "shape": S,
            "strength": 0.69,
            "seed": str1[5:],
        }
    

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(urljoin(api, "got_image"), params=params) as resp:
                response = await resp.read()

    except Exception as e:
        raise Exception("请求错误！请再试一次")   
    img = Img.open(io.BytesIO(response))
    info=img.info
    comment = json.loads(info["Comment"])
    img_data = response
    seed = comment["seed"]
    print(seed)
    if Config.get_config("zhenxun_plugin_NovelAi-aidraw_api", "DOWNLOAD_nai"):
        async with aiofiles.open(f"{IMAGE_PATH}/temp/NovelAi_{time.time()}.png", 'wb') as fout:
            await fout.write(img_data)
    imggs=[]
    imggs.append(img_data)
    seees=[]
    seees.append(str(seed))
    return imggs, seees

async def runpicapi(tag, S, imgs):   
    global token
    global init
    if init:
        if os.path.exists(tokenpath):
            async with aiofiles.open(tokenpath, mode='r', encoding='utf-8', errors="ignore") as f:
                token = await f.read()
            init = False
    if token == "":
        raise Exception("请先设置token！") 
    tag = tag + "masterpiece,best quality"
    seed = "-1"
    if tag[:5] == "Seed:" or tag[:5] == "seed:" or tag[:5] == "Seed=" or tag[:5] == "seed=":
        [str1, str2] = tag.split(",",1)
         
        params = {
            "token": token,
            "tags": str2,
            "shape": S,
            "strength": 0.69,
            "seed": str1[5:],
        }

    else:


        params = {
            "token": token,
            "tags": tag,
            "shape": S,
            "strength": 0.69,
        }


    
    try:
        responses=[]
        async with aiohttp.ClientSession() as session:
            for j in imgs:
                async with session.post(urljoin(api, "got_image2image"),data=j, params=params) as resp:
                    response = await resp.read()
                    responses.append(response)
    except Exception as e:
        raise Exception("请求错误！请再试一次") 
    imggs=[]    
    seees=[]   
    for ii in responses:  
        img = Img.open(io.BytesIO(ii))
        info=img.info
        comment = json.loads(info["Comment"])
        img_data = ii
        seed = comment["seed"]
        imggs.append(img_data)
        seees.append(str(seed))
        print(seed)
        if Config.get_config("zhenxun_plugin_NovelAi-aidraw_api", "DOWNLOAD_nai"):
            async with aiofiles.open(f"{IMAGE_PATH}/temp/NovelAi_{time.time()}.png", 'wb') as fout:
                await fout.write(img_data)
    
    return imggs, seees
    
async def translate(_query):
    global i
    lang = "en"
    _to = lang
    a = _query.replace("，",",")
    _query = a.replace("：",":")
    if os.path.exists(jsonpath):
        _query = await ETtranslate(_query)
    elif i < 3:
        await can.send("未检测到词库文件，开始下载文件...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(json_url) as resp:
                    async with aiofiles.open(jsonpath,"wb") as code:
                        await code.write(await resp.content.read())  
            await can.send(f"下载完成，开始生成图片")
        except Exception as e:
            i = i + 1
            await can.send(f"下载失败，最多尝试3次，当前第{i}次，本次跳过词库翻译.{type(e)}：{e}")
            pass
    _appid = Config.get_config("zhenxun_plugin_NovelAi-aidraw_api", "appid")
    if not _appid:
        logger.info(f"没有appid")
        return _query
    if not await is_Chinese(_query):
        logger.info(f"没有包含中文，不翻译")
        return _query
    _salt = Config.get_config("zhenxun_plugin_NovelAi-aidraw_api", "salt")
    _key = Config.get_config("zhenxun_plugin_NovelAi-aidraw_api", "key")
    _sign = f"{_appid}{_query}{_salt}{_key}"
    _sign = hashlib.md5(bytes(_sign, 'utf-8')).hexdigest()

    async with httpx.AsyncClient() as client:
        success = False
        for times in range(5):
            try:
                url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
                params = {
                    "q": _query,
                    "from": "zh",
                    "to": _to,
                    "appid": _appid,
                    "salt": _salt,
                    "sign": _sign,
                }

                json_data = await client.post(url, params=params)
            except Exception as e:
                logger.warning(f"第{times+1}次连接失败... {type(e)}: {e}")
                continue
            else:
                success = True
                break
    if not success:
        await can.send("翻译失败！将使用原文")
        return _query.replace(" ","%20")

    json_data = json_data.json()
    logger.debug(f"结果: {json_data}")
    if "error_code" not in json_data.keys():
        _result = json_data['trans_result'][0]
        logger.info(f"翻译完成")
        return _result['dst']

    if json_data['error_code'] != "52000":
        await can.send("翻译失败！将使用原文")
        raise _query.replace(" ","%20")

async def ETtranslate(_query):
    json_info = json.load(open(jsonpath, "r", encoding="utf8"))
    sstr = _query.split(",")
    text = ""
    outt = ""
    try:
        for sst in sstr:
            sst1 = sst.strip()
            text = sst1
            for dictt in json_info["data"]:
                for key, info in dictt.items():
                    if key == "data" and isinstance(dictt, dict):
                        for key1, dt in info.items():
                            for key11, dt1 in dt.items():
                                if dt1 == sst1:
                                    text = key1
            outt = outt + text + ","   
    except Exception as e:
        logger.info(f"EhTag翻译失败{type(e)}: {e}")
        return _query
    logger.info(f"EhTag翻译完成"+outt)        
    return outt

async def img(event: MessageEvent):
    img_url=[]
    for seg in event.message['image']:
        img_url.append(seg.data["url"])
    imgbytes:list[str]=[]
    if img_url:
        async with aiohttp.ClientSession() as session:
            logger.info(f"正在获取图片")
            for i in img_url:
                async with session.get(i) as resp:
                    pic = str(b64encode(await resp.read()).decode('utf-8'))
                    imgbytes.append(pic)
    return imgbytes
        
@up.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, msg: Message = CommandArg()):
    try:
        await can.send(f"开始更新词库文件")
        async with aiohttp.ClientSession() as session:
            async with session.get(json_url) as resp:
                async with aiofiles.open(jsonpath,"wb") as code:
                    await code.write(await resp.content.read())       
        await can.send(f"更新完成")    
    except Exception as e:
        await can.send(f"下载失败{type(e)}：{e}")
        
@scheduler.scheduled_job(
    "cron",
    hour=12,
    minute=0,
)       
async def Autoup():
    try:
        logger.info(f"开始更新词库文件")
        async with aiohttp.ClientSession() as session:
            async with session.get(json_url) as resp:
                async with aiofiles.open(jsonpath,"wb") as code:
                    await code.write(await resp.content.read())       
        logger.info(f"更新完成")    
    except Exception as e:
        logger.info(f"下载失败{type(e)}：{e}")

async def run():
    global q
    global renshu
    while q.qsize() > 0:
        bot, keyword, S, event, ss = await q.get()
        try:
            await _run(bot, keyword, S, event, ss)
        except Exception as e:
            pass
        renshu=renshu-1
            

async def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
