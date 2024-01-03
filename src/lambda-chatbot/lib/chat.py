"""
This module contains the chatbot logic, using OpenAI's API.
"""

import openai
import requests
import traceback
from .common import (
    openai_api_key,
    chat_model,
    bot_name,
    bot_id,
    bot_system_configuration,
    make_request
)
from .awsutils import (
    get_chat_dynamodb,
    put_chat_dynamodb,
)

openai.api_key = openai_api_key

def create_image(image_description: str) -> str:
    """
    Create an image using OpenAI's API.

    :param image_description: The description of the image to create.
    :return: The URL of the image or an error message.
    """
    try:
        response = openai.Image.create(
            prompt=image_description,
            n=1,
            size="1024x1024"
        )
        return response["data"][0]["url"]
    except Exception:
        traceback.print_exc()
        return "No pude generar la imagen."

def create_chat_completion(chat_history: list) -> str:
    """
    Create a chat completion using OpenAI's API.

    :param chat_history: The chat history to use.
    :return: The response message.
    """
    chat_completion = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": bot_system_configuration},
            *[{"role": "user", "content": msg} for msg in chat_history],
        ]
    )

    response_message = chat_completion.choices[0].message.content

    if response_message.startswith(f"{bot_name}: "):
        response_message = response_message[len(f"{bot_name}: "):]

    return response_message

def handle_conversation(message: dict) -> str or None:
    """
    Handle a conversation with a user, responding either
    with a message or an image URL.

    :param message: The message to handle.
    :return: The response message or None if no response is needed.
    """
    chat_id = message["chat"]["id"]
    is_private_chat = message["chat"]["type"] == "private"
    user_name = message["from"]["first_name"]
    message_text = message["text"].strip()

    try:
        reply_to = message["reply_to_message"]["from"]["id"]
    except KeyError:
        reply_to = None

    if message_text.startswith("/imagen"):
        image_description = message_text[len("/imagen"):].strip()
        if not image_description:
            return "Necesito una descripción para generar la imagen."
        return create_image(image_description)
    
    if message_text.startswith("/dolar"):
        response = make_request(requests.get, "https://api.bluelytics.com.ar/v2/latest")
        value_sell = response.json()["blue"]["value_sell"]
        return f"💸 Cotización del dólar blue: *${value_sell}* 💸"

    chat_history = get_chat_dynamodb(chat_id)[-10:]
    chat_history.append(f"{user_name}: {message_text}")

    if bot_name.lower() not in message_text.lower() and reply_to != bot_id and not is_private_chat:
        response_message = None
    else:
        response_message = create_chat_completion(chat_history)
        chat_history.append(f"{bot_name}: {response_message}")

    put_chat_dynamodb(chat_id, chat_history)

    return response_message
