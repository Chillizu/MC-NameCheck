from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import requests

@register("namecheck", "Name", "一个简单的检查mc名称是否冲突的插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("namecheck")
    async def helloworld(self, event: AstrMessageEvent, name: str):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        url = str('https://api.mojang.com/users/profiles/minecraft/' + name)
        response = requests.get(url)
        data = response.json()

        if 'errorMessage' in data:
            message = f"名称 {name} 可用"
        else:
            message = f"名称 {name} 已被占用, id={data['id']}"
        logger.info(message)
        yield event.plain_result(message) # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
