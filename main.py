from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult # pyright: ignore[reportMissingImports]
from astrbot.api.star import Context, Star, register # pyright: ignore[reportMissingImports]
from astrbot.api import logger # pyright: ignore[reportMissingImports]
import requests

@register("mcTools", "Name", "一个mc服务器便携工具包", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("namecheck")
    async def checkname(self, event: AstrMessageEvent, name: str):
        """名称冲突查询""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        url = str('https://api.mojang.com/users/profiles/minecraft/' + name)
        response = requests.get(url)
        data = response.json()

        if 'errorMessage' in data:
            message = f"名称 {name} 可用"
        else:
            message = f"名称 {name} 已被占用, id={data['id']}"
        logger.info(message)
        yield event.plain_result(message) # 发送一条纯文本消息

    @filter.command("itemcount")
    async def calculator(self, event: AstrMessageEvent, item: int, tar_type: str="group", raw_type: str="single", stack: int=64):
        """物品数量计算器""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        if raw_type == "single":
            pass
        elif raw_type == "stack":
            item = item * stack
        elif raw_type == "box" or raw_type == "chest":
            item = item * stack * 27
        elif raw_type == "largechest":
            item = item * stack * 54
        else:
            pass

        if tar_type == "stack":
            message = "{:f} 个物品可以堆叠成 {:.2f} 组——".format(item, (item / stack))
        elif tar_type == "box" or type == "chest":
            count_box = item / stack / 27
            message = "{:f} 个物品可以塞满 {:.2f} 个箱子~".format(item, count_box)
        elif tar_type == "largechest":
            count_largechest = item / stack / 54
            message = "{:f} 个物品可以塞满 {:.2f} 个大箱子！".format(item, count_largechest)
        else:
            message = "命令出错啦QAQ, 正确的写法也许是这样: /itemcount [物品数量] {结果类型: stack/box/chest/largechest} {源数据类型: single/stack/box/chest/largechest} {堆叠数目}"

        logger.info(message)
        yield event.plain_result(message) # 发送一条纯文本消息        

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
