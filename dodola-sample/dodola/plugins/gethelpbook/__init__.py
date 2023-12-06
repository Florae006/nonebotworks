from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from nonebot import on_command
from nonebot.rule import to_me
from .config import Config

getHelp=on_command(
    "help",
    aliases={"Help", "HELP","使用手册"}, 
    rule=to_me(),
    priority=10,
    block=True,
)

@getHelp.handle()
async def handle_function():
    try:
        reply=''
        reply+="小机器人DODOLA的使用指令设置如下：\n"
        reply+="需要@我的指令：\n"
        reply+="@+Help/help/HELP/使用手册->调出使用手册\n"
        reply+="@+查询外榜->获得xcpc外榜\n"
        reply+="@+查询这个人的cfRating：+cf昵称->获得某人当前rating\n"
        reply+="@+帮我push+@某人->给某人发送随机一道算法题(待开发)\n"
        reply+="直接指令：\n"
        reply+="today/contest/查询今日比赛->获得今日牛客/cf/Atcoder比赛信息\n"
        reply+="tomorrow/Tomorrow/next/查询明日比赛->获得明日牛客/cf/Atcoder比赛信息\n"
        reply+="随机一题->获得一道随机算法题\n"
        reply+="谢谢使用~"
        
        await getHelp.finish(reply)
    except Exception:
        await getHelp.finish()

__plugin_meta__ = PluginMetadata(
    name="getHelpBook",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

