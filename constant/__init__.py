import os
import qqbot

from qqbot.core.util.yaml_util import YamlUtil

config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "../config.yaml"))
Bot_name = config["bot"]["nickname"]
Token = qqbot.Token(config["token"]["appid"], config["token"]["token"])