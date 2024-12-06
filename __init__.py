from hoshino import Service, R, priv
from hoshino.priv import get_user_priv
from hoshino.typing import CQEvent, HoshinoBot
import asyncio
from nonebot import MessageSegment, Message
from .utils import *
from nonebot import NoneBot
import re
from sqlitedict import SqliteDict
from hoshino.config.__bot__ import NICKNAME, SUPERUSERS
from .config import *

DB_PATH = get_path("data")
nickname = NICKNAME[0]
sv_help = """
[谁艾特我使用说明]

#[谁艾特我]
查看3天内被艾特的所有记录
<谁@我>
""".strip()

sv = Service(
    name="谁艾特我",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="功能",  # 分组归类
    help_=sv_help,  # 帮助说明
)


@sv.on_fullmatch(
    "谁艾特我",
    "谁at我",
    "谁AT我",
    "谁艾特我？",
    "谁At我",
    "谁@我",
    "谁@我了",
    "wam",
)
@sv.on_rex(r"^谁.{0,3}艾特我了?$")
async def who_at_me(bot: HoshinoBot, ev: CQEvent):
    uid = str(ev.user_id)
    gid = str(ev.group_id)
    db = init_db("data", tablename=gid)
    reminder_expire_time = get_reminder_expire_time()

    if not (uid in db.keys()) or not db[str(uid)]:
        await bot.finish(ev, "目前还没有人@您噢!")

    ated_user_messages: list = db[uid]
    new_ated_user_messages = ated_user_messages.copy()
    forward_messages = []

    for index, msg in enumerate(new_ated_user_messages):
        converted_time = convert_stamp_time_to_date(msg["time"])
        if get_now_time() - msg["time"] >= reminder_expire_time:
            del new_ated_user_messages[index]
            continue
        else:
            if show_time and not str(msg["data"]["content"]).startswith(
                f"[{converted_time}]"
            ):
                msg["data"][
                    "content"
                ] = f"[{converted_time}]\n{msg['data']['content']}"
            forward_messages.append(msg)

    if not forward_messages:
        await bot.finish(ev, "目前还没有人@您噢!")

    db[uid] = new_ated_user_messages
    forward_messages.reverse() if reversed_range else None
    (
        forward_messages.insert(
            0,
            node_custom(
                user_id=ev.self_id,
                name=nickname,
                content=TIPS,
                time=get_now_time(),
            ),
        )
        if tips_header
        else None
    )

    await bot.send_group_forward_msg(group_id=gid, messages=forward_messages)


@sv.on_message("group")
async def message_monitor(bot: HoshinoBot, ev: CQEvent):
    gid = str(ev.group_id)
    raw_message = str(ev.raw_message)
    replied_message = re.match(
        r".*?(\[CQ:reply,id=-?\d+])(\[CQ:at,qq=\d+]).*?", raw_message
    )
    ated_user_ids = set(re.findall(rf"\[CQ:at,qq=(\d+).*?]", raw_message))
    sender_user_name = await get_member_name(bot=bot, gid=gid, uid=ev.user_id)
    db = init_db("data", tablename=gid)
    if not ated_user_ids:
        return

    if replied_message:
        raw_message = raw_message.replace(
            replied_message.group(0), replied_message.group(1)
        )

    for user_id in ated_user_ids:
        user_id = str(user_id)
        user_name = await get_member_name(bot=bot, gid=gid, uid=user_id)
        raw_message = raw_message.replace(
            f"[CQ:at,qq={user_id}]", f"@{user_name}"
        ).strip()

    for user_id in ated_user_ids:
        msg = node_custom(
            user_id=ev.user_id,
            name=sender_user_name,
            content=raw_message.strip(),
            time=get_now_time(),
        )
        if user_id in db:
            # db[user_id].append(msg)不知道为什么不好使
            db_messages: list = db[user_id].copy()

            db_messages.append(msg)

            if len(db_messages) > 100:
                db_messages = db_messages[::-1]
                del db_messages[100::]
                db_messages = db_messages[::-1]
            db[user_id] = db_messages
        else:
            db[user_id] = [msg]


@sv.on_fullmatch("清除全部艾特记录", "清除艾特db", "cadb")
async def del_all_data(bot: HoshinoBot, ev: CQEvent):
    if get_user_priv(ev) < priv.SUPERUSER:
        await bot.finish(ev, "删除全部@记录只能超管删除")

    db_path = get_path("data", "db.sqlite")
    for table in SqliteDict.get_tablenames(db_path):
        db = init_db("data", tablename=table)
        for i in db:
            del db[i]
    await bot.send(ev, f"好哦，{nickname}已经清除所有人的@记录了")


@sv.on_fullmatch("已阅")
async def del_all_data(bot: HoshinoBot, ev: CQEvent):
    uid = str(ev.user_id)
    gid = str(ev.group_id)
    db = init_db("data", tablename=gid)
    if uid in db:
        del db[uid]
    await bot.send(ev, f"好哦，{nickname}已经帮你清除被@过的记录了")
