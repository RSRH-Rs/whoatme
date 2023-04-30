import json
import os
from nonebot import MessageSegment
import re
from sqlitedict import SqliteDict
from hoshino.typing import CQEvent, Dict, Any, HoshinoBot
import time
from datetime import datetime, timedelta
from .config import expire_time

def get_now_time() -> int:
    return int(datetime.timestamp(datetime.now()))

def convert_stamp_time_to_date(stamp_time:int) -> str:
    return datetime.fromtimestamp(stamp_time).strftime("%m-%d %H:%M")

def get_future_time(day: int) -> int:
    return int(datetime.timestamp(datetime.now() + timedelta(day)))


def get_reminder_expire_time() -> int:
    return expire_time * 24 * 3600 if expire_time else 3 * 24 * 3600



def node_custom(user_id: int, name: str, content: str, time: int):
    return {
        "type": "node",
        "data": {
            "name": name,
            "user_id": user_id,
            "content": content.strip(),

        },
        "time": time,
    }


async def get_member_name(bot: HoshinoBot, gid:str,uid:str) -> str:
    user_info = await bot.get_group_member_info(group_id=gid,user_id=uid)
    return user_info["card"] if not len(user_info["card"]) == 0 else user_info["nickname"]

def get_path(*paths) -> str:
    return os.path.join(os.path.dirname(__file__), *paths)


def init_db(db_dir, db_name='db.sqlite', tablename: str = "") -> SqliteDict:
    return SqliteDict(get_path(db_dir, db_name),
                      tablename=tablename,
                      encode=json.dumps,
                      decode=json.loads,
                      autocommit=True)


def reply_message_creator(ev: CQEvent, content: str):
    return MessageSegment.reply(ev.message_id) + content



