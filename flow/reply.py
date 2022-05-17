from tokenize import Token
from typing import List

import qqbot
from qqbot.model.message import (
    MessageReference,
    MessageSendRequest,
    MessageEmbed,
    MessageEmbedField,
    MessageArk,
    MessageArkKv,
    MessageMarkdown,
    MessageEmbedThumbnail,
    CreateDirectMessageRequest
)

from constant import config
from constant.words import BotDefault

APPID = config["token"]["appid"]
TOKEN = config["token"]["token"]


async def reply_text(message: qqbot.Message, content: str, channel_id=None, msg_id=None):
    """发送回复消息
    - message：固定的参数 `qqbot.Message`
    - content：回复文本内容
    - channel_id：发送消息的子频道ID `(选填)`
    - msg_id: 消息ID `(选填)`
    """
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    if channel_id is None:
        message_channel_id = message.channel_id
    else:
        message_channel_id = channel_id
    if msg_id is None:
        message_msg_id = message.id
    else:
        message_msg_id = msg_id
    await message_api.post_message(
        message_channel_id,
        MessageSendRequest(
            content=content,
            msg_id=message_msg_id,
        ),
    )


async def notify_text(channel_id: str, content: str, message_id=None):
    """推送主动消息
    - channel_id：子频道ID
    - content：消息内容
    - message_id：消息ID `(选填)`
    """
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    if message_id is None:
        msg_id = "0"
    else:
        msg_id = message_id
    await message_api.post_message(channel_id, MessageSendRequest(content=content, msg_id=msg_id))


async def reply_text_list(reply_message: qqbot.Message, content_list: List, title):
    # 发送回复消息
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    # 构造消息
    total_content = ""
    if len(content_list) == 0:
        total_content = BotDefault.DEFAULT_GET_FEEDBACK
    else:
        total_content = total_content.join([content + "\n" for content in content_list])

    # 通过api发送回复消息
    await message_api.post_message(
        reply_message.channel_id,
        qqbot.MessageSendRequest(content=title + "\n" + total_content, msg_id=reply_message.id)
    )


async def reply_markdown_content(channel_id: str, markdown_content: str, message_id: str = None):
    """发送MarkDown模板消息
    - channel_id：要发送的子频道ID
    - message_id：消息ID
    - markdown_content：MD模板消息文本内容
    """
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)

    markdown = MessageMarkdown()
    markdown.content = markdown_content

    if message_id:
        send = qqbot.MessageSendRequest(markdown=markdown, msg_id=message_id)
    else:
        send = qqbot.MessageSendRequest(markdown=markdown)

    # 发送 markdown 消息
    await message_api.post_message(channel_id, send)


async def reply_text_with_reference(message: qqbot.Message, content: str):
    """发送引用回复消息
    - content：发送引用回复的文本内容
    """
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    reference = MessageReference()
    reference.message_id = message.id
    await message_api.post_message(
        message.channel_id,
        MessageSendRequest(
            content=content,
            msg_id=message.id,
            message_reference=reference,
        ),
    )


async def reply_embed(reply_message: qqbot.Message, content_list: List, title: str, prompt: str, icon=None):
    """发送Embed模板消息
    - content_list：消息内容列表
    - title：消息标题
    - prompt：消息弹窗内容
    - icon：图片URL
    """
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    # 构造消息发送请求数据对象
    embed = MessageEmbed()
    embed.title = title
    embed.prompt = prompt
    if icon is None:
        pass
    else:
        thumbnail = MessageEmbedThumbnail()
        thumbnail.url = icon
        embed.thumbnail = thumbnail
    # 构造内嵌消息fields
    if len(content_list) == 0:
        embed.fields = [MessageEmbedField(name=BotDefault.DEFAULT_GET_FEEDBACK)]
    else:
        embed.fields = [MessageEmbedField(name=content) for content in content_list]

    # 通过api发送回复消息
    await message_api.post_message(
        reply_message.channel_id,
        qqbot.MessageSendRequest(embed=embed, msg_id=reply_message.id),
    )


async def reply_ark(reply_message: qqbot.Message, title: str, value: str, template_id: int):
    """发送ark模板回复
    - title：消息标题
    - value：消息内容
    - template_id：Ark模板ID 23,24,34,37
    """
    message_api = qqbot.AsyncMessageAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    # 构造消息发送请求数据对象
    ark = MessageArk()
    ark.template_id = template_id
    # 构造内嵌消息
    ark.kv = [
        MessageArkKv(key="#TITLE#", value=title),
        MessageArkKv(key="#METADESC#", value=value),
    ]

    # 通过api发送回复消息
    await message_api.post_message(
        reply_message.channel_id,
        qqbot.MessageSendRequest(ark=ark, msg_id=reply_message.id),
    )


async def reply_direct_text(message: qqbot.Message, content: str, user_id=None, msg_id=None):
    """发送私信消息
    - message：固定的参数 `qqbot.Message`
    - content：回复文本内容
    - user_id: 要私信的用户ID`(选填)`
    - msg_id: 消息ID `(选填)`
    """
    if user_id is None:
        message_user_id = message.author.id
    else:
        message_user_id = user_id
    if msg_id is None:
        message_msg_id = message.id
    else:
        message_msg_id = msg_id

    dms_api = qqbot.AsyncDmsAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    direct_message_guild = await dms_api.create_direct_message(
        CreateDirectMessageRequest(
            source_guild_id=message.guild_id,
            user_id=message_user_id
        )
    )

    await dms_api.post_direct_message(
        guild_id=direct_message_guild.guild_id,
        message_send=MessageSendRequest(
            content=content,
            msg_id=message_msg_id
        )
    )


async def reply_direct_text_duty(message: qqbot.Message, content: str, user_id=None, msg_id=None):
    """发送固定自召唤管理频道的私信消息
    - message：固定的参数 `qqbot.Message`
    - content：回复文本内容
    - user_id: 要私信的用户ID`(选填)`
    - msg_id: 消息ID `(选填)`
    """
    if user_id is None:
        message_user_id = message.author.id
    else:
        message_user_id = user_id
    if msg_id is None:
        message_msg_id = message.id
    else:
        message_msg_id = msg_id

    dms_api = qqbot.AsyncDmsAPI(qqbot.Token(APPID, TOKEN), False, timeout=6)
    direct_message_guild = await dms_api.create_direct_message(
        CreateDirectMessageRequest(
            source_guild_id="17590802707047114676",
            user_id=message_user_id
        )
    )

    await dms_api.post_direct_message(
        guild_id=direct_message_guild.guild_id,
        message_send=MessageSendRequest(
            content=content,
            msg_id=message_msg_id
        )
    )
