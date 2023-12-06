from nonebot import get_driver
from nonebot.plugin import PluginMetadata, on_message
from nonebot.adapters import Bot, Event

from .config import Config
reply_dic={
    "你好":"你好哇~",
    "早":"早上好~",
    "wq":"晚安~今天真是辛苦你啦~",
    "晚安":"晚安，祝您好梦哦~",
    "我爱你":"我也爱你~",
}
reply=on_message(
    priority=11
)
@reply.handle()
async def reply_handle(bot:Bot,event:Event):
    user_msg=str(event.get_message()).strip()
    try:
        reply_msg=reply_dic[user_msg]
        await reply.finish(reply_msg)
    except KeyError:
        await reply.finish()

__plugin_meta__ = PluginMetadata(
    name="simpleReply",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

