# HoshinoBot whoatme 谁艾特我插件

这是一个基于 HoshinoBot 的谁艾特我插件

## 使用方法

1.clone 本插件：
在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

```
git clone https://github.com/RSRH-Rs/whoatme.git
```

2.依赖：

```
pip install sqlitedict~=2.1.0

```

3.启用模块

在 hoshino\config\_\_bot\_\_.py 文件的 MODULES_ON 加入 'whoatme'

然后重启 HoshinoBot

谁艾特我触发关键词：`谁艾特我` `谁at我` `谁AT我` `谁.{0,3}艾特我了?$`
数据库操作触发关键词: 清空所有数据: `清除全部艾特记录` `cadb` 清除本人在特定群里的数据: `已阅`

4.配置文件
在 config.py 里面设置超时时间等等

```
expire_time: int = 3  # 合并转发消息记录的超时时间, 单位为天

reversed_range: bool = True  # 是否开启消息从最近到最晚，从上往下排列

tips_header: bool = True  # 是否开启第一条小提示

show_time: bool = False  # 是否显示时间戳

TIPS = f"""
{NICKNAME[0]}最多为每个用户单个群聊保存100条消息哦！
""".strip()  # 第一条小提示内容
```

**渣代码,欢迎提出改进建议~**
