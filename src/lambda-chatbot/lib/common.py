import os
import json
import boto3

def get_ssm_parameter(parameter_name: str) -> str:
    ssm_client = boto3.client("ssm")
    response = ssm_client.get_parameter(Name=parameter_name)
    return response["Parameter"]["Value"]

bot_configuration_ssm_parameter = os.environ["BOT_CONFIGURATION_SSM_PARAMETER"]

bot_configuration = json.loads(
    get_ssm_parameter(bot_configuration_ssm_parameter)
)

telegram_api_token = bot_configuration["telegram_api_token"]
bot_id = bot_configuration["bot_id"]
bot_name = bot_configuration["bot_name"]
chats_table_name = bot_configuration["chats_table_name"]
openai_api_key = bot_configuration["openai_api_key"]
audio_probability = bot_configuration["audio_probability"]
bot_system_configuration = f"Eres {bot_name}. " + bot_configuration["bot_system_configuration"]
chat_model = bot_configuration["chat_model"]
aws_polly_engine = bot_configuration["aws_polly_engine"]
aws_polly_language_code = bot_configuration["aws_polly_language_code"]
aws_polly_voice_id = bot_configuration["aws_polly_voice_id"]

def make_request(method, url, **kwargs):
    response = method(
        url,
        headers={
            "User-Agent": "Reddit Video Bot"
        },
        **kwargs
    )
    response.raise_for_status()
    return response
