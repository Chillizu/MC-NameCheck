from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult # pyright: ignore[reportMissingImports]
from astrbot.api.star import Context, Star, register # pyright: ignore[reportMissingImports]
from astrbot.api import logger # pyright: ignore[reportMissingImports]
import requests, jieba

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
            message = f" 名称 {name} 可用"
        else:
            message = f" 名称 {name} 已被占用, id={data['id']}"
        logger.info(message)
        yield event.plain_result(message) # 发送一条纯文本消息

    @filter.command("itemcount")
    async def calculator(self, event: AstrMessageEvent, item: int, tar_type: str="stack", raw_type: str="single", stack: int=64):
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
            message = " 命令出错啦QAQ, 正确的写法也许是这样: /itemcount [物品数量] {结果类型: stack/box/chest/largechest} {源数据类型: single/stack/box/chest/largechest} {堆叠数目}"

        logger.info(message)
        yield event.plain_result(message) # 发送一条纯文本消息    

    @filter.command("Docs")
    async def Docs(self, event: AstrMessageEvent, Question: str):
        """IpacEL 文档查询""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。
        docs = requests.get("https://ipacel.cc/Range/docs/%E5%9F%BA%E7%A1%80%E8%A7%84%E5%88%99.md").text + requests.get("https://ipacel.cc/Range/docs/%E5%8A%9F%E8%83%BD%E6%96%87%E6%A1%A3.md").text
        logger.info("Get Docs" + docs != "")
        yield event.plain_result('正在查询...') # 发送一条纯文本消息   
        umo = event.unified_msg_origin
        provider_id = await self.context.get_current_chat_provider_id(umo=umo)
        llm_resp = await self.context.llm_generate(
        chat_provider_id=provider_id, # 聊天模型 ID
        prompt="你是一个ai助手, 可以根据用户的问题, 你可以且只可以在上下文中查找结果, 并以简短的回复返回给用户, 注意, 关于回答会涉及到`如果你在填写白名单表单且接受规则, 那么请填写 我已阅读并同意.` 这个问题, 你不能回答，只能告诉用户`请查阅官方文档`。上下文内容如下:\n" + docs + "\n用户的问题是: " + Question,
        )
        resp = llm_resp.completion_text # 获取返回的文本
        yield event.plain_result('Search>' + resp) # 发送一条纯文本消息    

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
