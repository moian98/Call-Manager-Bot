class BotReply:
    """被动回复"""
    NOT_IS_ADMIN = "小召还不是管理员，无法执行此操作，请先授权小招位管理员"
    NO_AUTHORITY = "小召无法执行你的指令，需要对应管理权限的管理员才能使用哦"
    NO_CRATE = "小召无法执行你的指令，需要频道主才能使用哦"
    NO_CHANNEL_OWNER = "小召无法执行你的指令，需要子频道管理员才能使用哦"
    NO_MATCH_REPLY = "小召无法识别你的指令，请正确输入指令需要的参数"
    NOT_OWNER = ""
    DUTY_HELP = f"""以下为召唤管理相关指令：

🔘 /召唤管理
  ▫️ 普通频友需要找管理时在需要的子频道发送指令
🔘 /查看在线管理
  ▫️ 查看当前已签到在线的管理员
🔘 /管理注册
  ▫️ 初次使用本功能的管理员需先注册
🔘 /添加子频道
  ▫️ 🔵子频道管理员 注册后到你所管理的子频道使用指令添加
🔘 /删除子频道
  ▫️ 🔵子频道管理员 到你要删除的子频道使用指令删除一个已添加的子频道
🔘 /管理签到
  ▫️ 有时间管理频道时请签到
🔘 /管理签退
  ▫️ 没时间管理频道时请签退
🔘 /私信通知 [开丨关]
  ▫️ 开启或关闭私信通知
🔘 /查看信息 [我丨@管理员]
  ▫️ 查看我的值班信息或其他管理员的值班信息
🔴 /删除管理 @要删除的管理员
  ▫️ 删除一个已注册的管理员(❗注：此指令仅频道主可使用❗)

Tips: 所有指令请先@召唤管理，[]为多选一参数"""
# 🔘 /问题反馈 + 问题
#   ▫️ 反馈问题给管理（目前无法识别图片，尽量使用文字反馈）
# 🔘 /设置反馈子频道
#   ▫️ 到需要接受反馈的子频道使用指令
    DUTY_MENU = f"""￣￣￣￣￣＼功能菜单／￣￣￣￣￣
       🔹召唤管理  查看在线🔹
       🔹管理注册  私信通知🔹
       🔹管理签到  管理签退🔹
       🔹添加子频  删除子频🔹
       🔹查看信息  删除管理🔹

         ‼️指令详细介绍请‼️
        @召唤管理 /帮助 查看"""


class BotNotify:
    """主动通知"""
    pass


class BotDefault:
    """默认变量"""
    DEFAULT_MOIAN = "1198230457609294660"
    DEFAULT_BOT = "3665247604073490362"
    DEFAULT_BOT_NAME = "召唤管理"
    DEFAULT_GET_FEEDBACK = "错误。"
    DEFAULT_ARK_KEY = "key"
    DEFAULT_ARK_VALUE = "value"
