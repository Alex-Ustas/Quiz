# Store/change/get json data (quiz, user)

import os
import json


def get_json_data(file: str) -> dict:
    """Get all settings from json file"""
    if not os.path.exists(file):
        return dict()
    with open(file, 'r', encoding='utf-8') as file:
        quiz = json.load(file)
    return quiz


def save_user_data(file: str, name: str, score: list):
    """Save dict data in json file"""
    data = get_json_data(file)
    for i in range(len(data)):
        if data[i]['name'] == name:
            data[i]['quizes'] += 1
            data[i]['answered_questions'] = score[0]
            data[i]['total_questions'] = score[1]
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
