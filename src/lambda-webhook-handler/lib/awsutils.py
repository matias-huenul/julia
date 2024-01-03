import boto3

def get_ssm_parameter(parameter_name: str) -> str:
    ssm_client = boto3.client("ssm")
    response = ssm_client.get_parameter(Name=parameter_name)
    return response["Parameter"]["Value"]
