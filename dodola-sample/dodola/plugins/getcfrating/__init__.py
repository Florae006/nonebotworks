from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg,ArgPlainText
from nonebot.matcher import Matcher

from .config import Config

getcfRating=on_command(
    "查询这个人的cfRating：",
    rule=to_me(),
    priority=10,
    block=True,
)
@getcfRating.handle()
async def handle_function(matcher:Matcher, args:Message=CommandArg()):
    try:
        if args.extract_plain_text():
            matcher.set_arg("id",args)
    except Exception:
        await getcfRating.finish()
@getcfRating.got("id",prompt="请输入cf昵称")
async def got_id(id:str=ArgPlainText()):
    try:
        import httpx
        from bs4 import BeautifulSoup
        headers = {
            "",
        }
        res=httpx.get(url='https://codeforces.com/profile/'+id,headers=headers, timeout=10, verify=False)
        if(res.status_code==200):
            html_doc=res.text
            soup = BeautifulSoup(html_doc,'lxml')
            box=soup.select("div.info")
            rating=box[0].select("ul li")[0].text.strip()
            rating=rating.split(":")[1].strip()
            rating=rating.split(" ")[0]
            await getcfRating.finish(f"{id}目前的cfRating为{rating}")
        elif(res.status_code==302):
            await getcfRating.finish("查无此人QwQ")
        else:
            await getcfRating.finish("查询失败了捏qwq")
    except Exception:
        await getcfRating.finish()

__plugin_meta__ = PluginMetadata(
    name="getCfRating",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

