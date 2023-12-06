from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot import on_command

from .config import Config

getRandomProblem=on_command(
    "随机一题",
    aliases={"contest", "查询今日比赛"}, 
    priority=9,
    block=True,
)
@getRandomProblem.handle()
async def handle_function():
    try:
        import httpx
        from bs4 import BeautifulSoup
        import random
        headers = {
            "",
        }
        page=random.randint(1,90)
        res=httpx.get(url='https://codeforces.com/problemset/page/'+str(page),headers=headers, timeout=10, verify=False)

        if(res.status_code==200):
            html_doc=res.text
            soup = BeautifulSoup(html_doc,'lxml')
            box=soup.select("table.problems tr")

            preurl="https://codeforces.com/problemset"
            rd=random.randint(1,100)
            problem=box[rd]
            url=problem.select("td a")[0].get("href")
            url=preurl+url
            tds=problem.select("td")
            name=tds[1].select("div")
            pname=name[0].select("a")[0].text.strip()
            tags=name[1].select("a")
            ptags=[]
            for ti in tags:
                ptags.append(ti.text)
            rating=tds[3].text.strip()

            reply="获得随机一道cf题：\n"
            reply+="标题："+pname+'\n'
            reply+="题目链接："+url+'\n'
            reply+="题目标签："
            for i in ptags:
                reply+=i+" "
            reply+="\n"
            reply+=f"这是一道Rating{rating}分的题目，相信你今天一定可以解决它~"
            await getRandomProblem.finish(reply)
        else:
            await getRandomProblem.finish("OwO好像访问出错了捏")
    except Exception:
        await getRandomProblem.finish()

__plugin_meta__ = PluginMetadata(
    name="randomProblem",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

