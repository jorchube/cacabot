import json


def get(secret_json_file_path):
    content = _get_file_content(secret_json_file_path)

    return content["bot_api_auth_token"]

def _get_file_content(secret_json_file_path):
    file = open(secret_json_file_path, "r")
    content = file.read()

    json_content = json.loads(content)

    return json_content
