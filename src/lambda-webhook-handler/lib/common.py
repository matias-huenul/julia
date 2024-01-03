import os
import json
from .awsutils import get_ssm_parameter

chatbot_function_name = os.environ["CHATBOT_FUNCTION_NAME"]
bot_configuration_ssm_parameter = os.environ["BOT_CONFIGURATION_SSM_PARAMETER"]

bot_configuration = json.loads(
    get_ssm_parameter(bot_configuration_ssm_parameter)
)

allowed_chat_ids = bot_configuration["allowed_chat_ids"]
