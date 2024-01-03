import random
import traceback
from lib.chat import handle_conversation
from lib.common import audio_probability
from lib.telegram import send_message, send_voice, send_photo

def lambda_handler(event, _):
    try:
        message = event["message"]
        is_private_chat = message["chat"]["type"] == "private"
        response = handle_conversation(message)

        if not response:
            return False

        message_id = message["message_id"]
        chat_id = message["chat"]["id"]
        reply_to_message_id = message_id if not is_private_chat else None
        
        if response.startswith("https://"):
            send_photo(chat_id, response, reply_to_message_id=reply_to_message_id)

        elif len(response) < 300 and random.random() <= audio_probability and not response.startswith("💸"):
            send_voice(chat_id, response, reply_to_message_id=reply_to_message_id)

        else:
            send_message(chat_id, response, reply_to_message_id=reply_to_message_id)

        return True

    except Exception:
        traceback.print_exc()
        return False
