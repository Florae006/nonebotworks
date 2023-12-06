from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from nonebot import on_command
from nonebot.rule import startswith
from .config import Config


import time
import httpx
from bs4 import BeautifulSoup
import pytz
import datetime
from datetime import date

contestinfo=on_command(
    "today",
    aliases={"contest", "查询今日比赛"}, 
    priority=9,
    block=True,
)

@contestinfo.handle()
async def handle_function():
    try:
        headers = {
            "",
        }
        reply=f"今日比赛:\n"
        replync=''
        replycf=''
        replyatr=''
        flagr=0

        resnc=httpx.get(url='https://ac.nowcoder.com/acm/contest/vip-index',headers=headers, timeout=10, verify=False)
        if(resnc.status_code==200):
            html_doc=resnc.text
            soup = BeautifulSoup(html_doc,'lxml')
            contestLists=soup.select("div.platform-item-cont")
            today=date.today()
            today=str(today)
            urlpre="https://ac.nowcoder.com"
            todaync=[]
            for contest in contestLists:
                rt=contest.findAll("li")
                rtList=rt[1].text.split()
                if(rtList[1]==today):
                    ncname=contest.select_one("h4")
                    nclink=ncname.select_one("a")['href']
                    ncname=ncname.select_one("a").text
                    dict={
                        "比赛名称":ncname,
                        "开始时间":rtList[2],
                        "比赛链接":urlpre+nclink,
                    }
                    todaync.append(dict)
            if(len(todaync)!=0):
                if(flagr==0):
                    flagr=1
                replync+="🎈牛客竞赛：\n"
                for i in todaync:
                    replync+="比赛名称："+i["比赛名称"]+"\n"
                    replync+="开始时间："+i["开始时间"]+"\n"
                    replync+="比赛链接："+i["比赛链接"]+"\n"
        
        # 获得cf今日比赛信息
        rescf=httpx.get(url='https://codeforces.com/contests',headers=headers, timeout=10, verify=False)
        if(rescf.status_code==200):
            html_doc=rescf.text
            soup = BeautifulSoup(html_doc,'lxml')
            contestLists=soup.find_all("table")
            todaycf=[]
            todaytime=time.strftime('%b/%d/%Y',time.localtime())
            flag=0
            urlpre="https://codeforces.com/contests/"
            for contest in contestLists[0]:
                if(flag==1):
                    rt=contest.findAll('td')
                    contestid=contest.get("data-contestid")
                    if(len(rt)==6):
                        cfname=rt[0].text.strip()
                        tm=rt[2].text.strip()
                        time_format="%b/%d/%Y %H:%M"
                        tm=time.strptime(tm,time_format)
                        rstz=pytz.timezone('Europe/Moscow')
                        cntz=pytz.timezone('Asia/Shanghai')
                        tm_str=time.strftime(time_format,tm)
                        dt=datetime.datetime.strptime(tm_str,time_format)
                        local_dt=rstz.localize(dt,is_dst=None)
                        tm=local_dt.astimezone(cntz)
                        tm=tm.strftime(time_format)
                        rtsp=tm.split(" ")
                        cfdate=rtsp[0].replace("\n","")
                        cftime=rtsp[1].replace("\n","")
                        if(cfdate==todaytime):
                            dict={
                                "比赛名称":cfname,
                                "开始时间":cftime,
                                "比赛链接":urlpre+contestid,
                            }
                            todaycf.append(dict)
                    flag=0
                else:
                    flag=1
            if(len(todaycf)!=0):
                if(flagr==0):
                    flagr=1
                replycf+="🎈cf比赛：\n"
                for i in todaycf:
                    replycf+="比赛名称："+i["比赛名称"]+"\n"
                    replycf+="开始时间："+i["开始时间"]+"\n"
                    replycf+="比赛链接："+i["比赛链接"]+"\n"
        
        # 获得AtCoder今日比赛信息
        resat=httpx.get(url="https://atcoder.jp/contests/",headers=headers, timeout=10, verify=False)
        if(resat.status_code==200):
            html_doc=resat.text
            soup = BeautifulSoup(html_doc,'lxml')
            contestLists=soup.select_one("div#contest-table-upcoming").select("tr")
            today=date.today()
            today=str(today)
            urlpre="https://atcoder.jp"
            todayatr=[]
            for contest in contestLists:
                rt=contest.findAll('td')
                if(len(rt)==4):
                    tm=rt[0].text[:19]
                    time_format="%Y-%m-%d %H:%M:%S"
                    tm=time.strptime(tm,time_format)
                    rstz=pytz.timezone('Asia/Tokyo')
                    cntz=pytz.timezone('Asia/Shanghai')
                    tm_str=time.strftime(time_format,tm)
                    dt=datetime.datetime.strptime(tm_str,time_format)
                    local_dt=rstz.localize(dt,is_dst=None)
                    tm=local_dt.astimezone(cntz)
                    tm=tm.strftime(time_format)
                    rtsp=tm.split(" ")
                    atrdate=rtsp[0]
                    atrtime=rtsp[1]
                    atrlink=rt[1].select_one("a")["href"]
                    if(atrdate==today):
                        atrname=rt[1].text
                        atrname=atrname.replace("Ⓐ","")
                        atrname=atrname.replace("◉","")
                        atrname=atrname.strip()
                        dict={
                            "比赛名称":atrname,
                            "开始时间":atrtime,
                            "比赛链接":urlpre+atrlink
                        }
                        todayatr.append(dict)
            if(len(todayatr)!=0):
                if(flagr==0):
                    flagr=1
                replyatr+="🎈Atcoder比赛：\n"
                for i in todayatr:
                    replyatr+="比赛名称："+i["比赛名称"]+"\n"
                    replyatr+="开始时间："+i["开始时间"]+"\n"
                    replyatr+="比赛链接："+i["比赛链接"]+"\n"
        if(flagr==0):
            reply+="今天没有比赛哦，但是也要好好加训补题哦🧐🧐~"
        else:
            reply+=replycf+replync+replyatr
            reply+="今天的cf/牛客/Atcoder比赛如上！今天也要加油哦😉😉~"
        await contestinfo.finish(str(reply))
    except Exception:
        await contestinfo.finish()


__plugin_meta__ = PluginMetadata(
    name="getContestInfo",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

