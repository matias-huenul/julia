# import uuid
# import boto3
import requests
from .awsutils import synthesize_speech
from .common import make_request, telegram_api_token

telegram_api_url = f"https://api.telegram.org/bot{telegram_api_token}"

def send_message(
        chat_id: str,
        text: str,
        reply_to_message_id: str = None
    ) -> None:
    """
    Send a message to a Telegram chat.

    :param chat_id: The ID of the chat to send the message to.
    :param text: The text of the message to send.
    :param reply_to_message_id: The ID of the message to reply to.

    :return: None

    :raises: requests.HTTPError if the request fails.
    """
    make_request(
        requests.post, 
        f"{telegram_api_url}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text,
            "reply_to_message_id": reply_to_message_id,
            "parse_mode": "Markdown"
        }
    )

def send_voice(
        chat_id: str,
        text: str,
        reply_to_message_id: str = None
    ) -> None:
    """
    Send a voice message to a Telegram chat.

    :param chat_id: The ID of the chat to send the message to.
    :param text: The text of the message to send.
    :param reply_to_message_id: The ID of the message to reply to.

    :return: None

    :raises: requests.HTTPError if the request fails.
    """
    audio_stream = synthesize_speech(text)

    # audio_file_path = f"/tmp/audio_{str(uuid.uuid4())}.ogg"

    # with open(audio_file_path, "wb") as f:
    #     f.write(audio_stream.read())
    
    # with open(audio_file_path, "rb") as f:
    #     make_request(
    #         requests.post, 
    #         f"{telegram_api_url}/sendVoice",
    #         data={
    #             "chat_id": chat_id,
    #             "reply_to_message_id": reply_to_message_id
    #         },
    #         files={"voice": f.read()}
    #     )

    make_request(
        requests.post, 
        f"{telegram_api_url}/sendVoice",
        data={
            "chat_id": chat_id,
            "reply_to_message_id": reply_to_message_id
        },
        files={"voice": audio_stream.read()}
    )

def send_photo(
        chat_id: str,
        text: str,
        reply_to_message_id: str = None
    ) -> None:
    """
    Send a photo message to a Telegram chat.

    :param chat_id: The ID of the chat to send the message to.
    :param text: The text of the message to send.
    :param reply_to_message_id: The ID of the message to reply to.

    :return: None

    :raises: requests.HTTPError if the request fails.
    """
    make_request(
        requests.post, 
        f"{telegram_api_url}/sendPhoto",
        data={
            "chat_id": chat_id,
            "photo": text,
            "reply_to_message_id": reply_to_message_id
        }
    )

def send_video(
        chat_id: str,
        video_file_path: str,
        reply_to_message_id: str = None
    ) -> None:
    """
    Send a video message to a Telegram chat.

    :param chat_id: The ID of the chat to send the message to.
    :param video_file_path: The path of the video file to send.
    :param reply_to_message_id: The ID of the message to reply to.

    :return: None

    :raises: requests.HTTPError if the request fails.
    """
    with open(video_file_path, "rb") as fh:
        make_request(
            requests.post, 
            f"{telegram_api_url}/sendVideo",
            files={"video": fh},
            data={
                "chat_id": chat_id,
                "reply_to_message_id": reply_to_message_id
            }
        )
