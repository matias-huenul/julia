import boto3
import botocore
from .common import (
    chats_table_name,
    aws_polly_engine,
    aws_polly_language_code,
    aws_polly_voice_id,
)

def synthesize_speech(text: str) -> botocore.response.StreamingBody:
    """
    Synthesize speech from text using Amazon Polly.

    :param text: The text to synthesize speech from.
    :return: The synthesized speech as an Ogg Vorbis audio stream.
    """
    polly_client = boto3.client("polly")
    response = polly_client.synthesize_speech(
        Engine=aws_polly_engine,
        LanguageCode=aws_polly_language_code,
        OutputFormat="ogg_vorbis",
        Text=text,
        VoiceId=aws_polly_voice_id
    )

    return response["AudioStream"]

def get_chat_dynamodb(chat_id: int) -> list:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(chats_table_name)
    response = table.get_item(Key={"chat_id": chat_id})

    if "Item" not in response:
        return []

    return response["Item"]["chat"]

def put_chat_dynamodb(chat_id: int, chat: list) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(chats_table_name)

    table.put_item(
        Item={
            "chat_id": chat_id,
            "chat": chat
        }
    )
