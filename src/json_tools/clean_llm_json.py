

def clean_llm_json(text: str):
    """
    大模型输出可能包含非json的内容，需要清理掉，并解析json
    :param text:
    :return:
    """
    import json

    json_str = text[text.find('{'):text.rfind('}') + 1]
    return json.loads(json_str)