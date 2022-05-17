import re
from typing import List

FEEDBACK_STATUS_DEFAULT = 0
FEEDBACK_STATUS_FIX = 1


def filter_emoji(des_str, result_str=""):
    # 过滤表情
    res = re.compile("[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]")
    return res.sub(result_str, des_str)


def get_user_list(params: str) -> List[str]:
    """获取消息中的用户ID -> 列表"""
    # user_list = params.replace("<@", "").replace(">", "").replace(" ", "").replace("\xa0", "").split("!")
    # user_list.remove("")
    user_list = re.findall(r"<@(.*)>", params)
    user_list = "".join(user_list)
    user_list = user_list.replace("<@", "").replace(">", "").replace(" ", "").replace("\xa0", "").split("!")
    user_list.remove("")
    return user_list


def get_pure_text(params: str) -> str:
    """获取消息中的纯文本"""
    pure_text = re.sub("<(\S*?)[^>]*>.*?|<.*? />", "", params).replace(" ", "")
    return pure_text


def get_morning_markdown_content(owners) -> str:
    if not owners:
        return ""

    markdown_content = "**新的一天开始啦，全员禁言已解除，有问题和建议可以找我反馈哦**\n\n"

    # 添加值班信息
    markdown_content += "今日值班人员：\n\n"
    for owner in owners:
        markdown_content += "> 「%s」\t%s\n" % (owner["owner_type"], owner["owner_name"])

    # 添加可用指令信息
    markdown_content += "\n\n全员可用指令：\n" \
    + "\n> **/问题反馈** [问题内容]" \
    + "\n> 反馈一些问题，并通知值班人员" \
    + "\n> **/产品建议** [建议内容]" \
    + "\n> 提供一些需求建议，并通知值班人员" \
    + "\n> **/查看值班表**" \
    + "\n> 查看当前的官方值班表和今日值班人员"

    return markdown_content