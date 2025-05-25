# app/utils/passcode_generator.py

"""
passcode_generator.py

このモジュールは、クイズの回答が全問正解だった場合に
SwitchBot APIを使って一時的な6桁パスコードを生成する処理を提供します。
"""

import os
import random
import logging
from datetime import datetime, timedelta
import requests
import json

from dotenv import load_dotenv

# .env読み込み
load_dotenv()

# ロギングの設定
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = 'https://api.switch-bot.com'

def is_weak_passcode(code: int) -> bool:
    """連続または同一数字などの脆弱なパスコードを検出"""
    str_code = str(code)
    return (
        str_code == str_code[0] * 6 or
        str_code in "0123456789" or
        str_code in "9876543210"
    )

def generate_strong_passcode() -> int:
    """6桁の強力なパスコードを生成"""
    while True:
        code = random.randint(100000, 999999)
        if not is_weak_passcode(code):
            return code

def make_request_header() -> dict:
    """SwitchBot API用のヘッダーを作成"""
    token = os.getenv("SWITCHBOT_TOKEN")
    secret = os.getenv("SWITCHBOT_SECRET")
    return {
        "Authorization": token,
        "Content-Type": "application/json",
    }

def create_passcode_if_correct(user_answers: dict, correct_answers: dict, name: str, valid_hours: int) -> dict:
    """
    クイズが全問正解だった場合のみ、SwitchBotでパスコードを作成する。

    :param user_answers: ユーザーの回答（辞書）
    :param correct_answers: 正解の回答（辞書）
    :param name: 作成するパスコードに紐づける名前
    :param valid_hours: パスコードの有効時間（時間）
    :return: パスコードまたはエラー情報を含む辞書
    """
    # 全問正解チェック
    for question, correct_answer in correct_answers.items():
        if user_answers.get(question) != correct_answer:
            logger.info("不正解の回答あり: %s", question)
            return {"error": "不正解のため、パスコードは生成されません。"}

    # 正解だった場合、パスコード作成
    try:
        device_id = os.getenv("DEVICE_ID")
        url = f"{BASE_URL}/v1.1/devices/{device_id}/commands"
        headers = make_request_header()

        password = generate_strong_passcode()
        start_dt = datetime.now()
        end_dt = start_dt + timedelta(hours=valid_hours)
        start_time = int(start_dt.timestamp() * 1000)
        end_time = int(end_dt.timestamp() * 1000)

        payload = {
            "command": "createKey",
            "parameter": {
                "name": name,
                "type": "permanent",
                "password": password,
                "startTime": start_time,
                "endTime": end_time
            },
            "commandType": "command"
        }

        logger.debug("送信ペイロード: %s", json.dumps(payload, indent=2, ensure_ascii=False))

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if result.get("statusCode") == 100:
            logger.info("パスコード生成成功")
            return {"passcode": str(password)}
        else:
            error_message = result.get("message", "不明なエラー")
            logger.error("SwitchBotエラー: %s", error_message)
            return {"error": f"SwitchBotエラー: {error_message}"}

    except requests.RequestException as e:
        logger.exception("HTTPエラー")
        return {"error": f"リクエスト失敗: {e}"}
    except Exception as e:
        logger.exception("未知のエラー")
        return {"error": f"エラー: {e}"}
