import json
import boto3
import traceback
from lib.common import allowed_chat_ids, chatbot_function_name

def lambda_handler(event, _):
    try:
        print(event["body"])

        request_body = json.loads(event["body"])
        message = request_body["message"]
        chat_id = message["chat"]["id"]

        if chat_id not in allowed_chat_ids:
            print(f"Chat {chat_id} is not allowed to use this bot.")

        else:
            client = boto3.client("lambda", region_name="us-east-1")
            client.invoke(
                FunctionName=chatbot_function_name,
                InvocationType="Event",
                Payload=bytes(event["body"], encoding="utf-8")
            )
    except:
        traceback.print_exc()

    return {"statusCode": 200}
