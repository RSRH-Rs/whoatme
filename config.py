from hoshino.config import NICKNAME
expire_time: int = 3  # 合并转发消息记录的超时时间, 单位为天

reversed_range: bool = True  # 消息从最近到最晚，从上往下排列

tips_header: bool = True  # 第一条为小提示

show_time: bool = False  # 是否显示时间戳

TIPS = f"""
{NICKNAME[0]}最多为每个用户单个群聊保存100条消息哦！
""".strip()  # 第一条小提示
