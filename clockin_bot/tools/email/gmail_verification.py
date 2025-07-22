import re
import time
import logging
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

import httpx
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_PATH = Path("credentials.json")
TOKEN_PATH = Path("token.json")

logger = logging.getLogger(__name__)

async def get_gmail_service_async():
    # 這裡示範同步邏輯包成線程，因為 google api 目前沒官方 async
    def build_service():
        creds = None
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        if not creds or not creds.valid:
            if not CREDENTIALS_PATH.exists():
                raise RuntimeError("缺少 credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

            with open(TOKEN_PATH, "w") as token_file:
                token_file.write(creds.to_json())
        # 目前只能同步呼叫 build 函式
        from googleapiclient.discovery import build
        return build("gmail", "v1", credentials=creds)

    service = await asyncio.to_thread(build_service)
    return service

async def fetch_gmail_verification_code_with_debug_async(
    service,
    newer_than: int,
    timeout_sec: int = 60,
    debug: bool = False
) -> str:
    start_time = time.time()
    query = f'subject:"104企業大師" after:{newer_than}'
    sleep_interval = 5

    async with httpx.AsyncClient() as client:
        while time.time() - start_time < timeout_sec:
            try:
                headers = {"Authorization": f"Bearer {service._http.credentials.token}"}
                params = {"userId": "me", "q": query, "maxResults": 10}
                response = await client.get(
                    "https://gmail.googleapis.com/gmail/v1/users/me/messages",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                messages = data.get("messages", [])

                if debug:
                    logger.debug(f"[DEBUG] 抓到 {len(messages)} 封信，查詢語法：{query}")

                for msg in messages:
                    msg_id = msg["id"]
                    resp_msg = await client.get(
                        f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
                        headers=headers,
                    )
                    resp_msg.raise_for_status()
                    full_msg = resp_msg.json()

                    internal_date_sec = int(full_msg.get("internalDate", "0")) // 1000

                    # ✅ 補這段：過濾過舊信件
                    if internal_date_sec <= newer_than:
                        if debug:
                            logger.debug(f"[DEBUG] 跳過太舊信件：{internal_date_sec} <= {newer_than}")
                        continue

                    headers_list = full_msg.get("payload", {}).get("headers", [])
                    subject = next((h["value"] for h in headers_list if h["name"] == "Subject"), "(無主旨)")

                    tw_time = datetime.fromtimestamp(internal_date_sec, tz=timezone(timedelta(hours=8)))
                    if debug:
                        logger.debug(
                            f"[DEBUG] 信件時間：{internal_date_sec}（台灣時間：{tw_time.strftime('%Y-%m-%d %H:%M:%S')}），主旨：{subject}"
                        )

                    match = re.search(r"[【\[]?(\d{6})[】\]]?", subject)
                    if match:
                        code = match.group(1)
                        if debug:
                            logger.debug(f"✅ 擷取成功！驗證碼為：{code}")
                        return code
                    else:
                        if debug:
                            logger.debug(f"[DEBUG] ❌ 未擷取到驗證碼（主旨格式可能不符）")

                if debug:
                    logger.debug(f"[DEBUG] 尚無新信件符合條件... ({int(time.time() - start_time)}s)")
                await asyncio.sleep(sleep_interval)

            except Exception as e:
                if debug:
                    logger.error(f"[ERROR] 擷取 Gmail 驗證碼失敗: {e}")
                raise RuntimeError(f"擷取失敗") from e

        raise RuntimeError(f"查無驗證碼")


async def get_latest_message_time_async(service) -> int:
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {service._http.credentials.token}"}
            params = {"userId": "me", "maxResults": 1}
            response = await client.get(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            messages = data.get("messages", [])
            if not messages:
                return 0

            msg_id = messages[0]["id"]
            resp_msg = await client.get(
                f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
                headers=headers,
            )
            resp_msg.raise_for_status()
            full_msg = resp_msg.json()

            headers_list = full_msg.get("payload", {}).get("headers", [])
            date_header = next((h["value"] for h in headers_list if h["name"].lower() == "date"), None)

            if date_header:
                dt = parsedate_to_datetime(date_header)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                dt_tw = dt.astimezone(timezone(timedelta(hours=8)))
                return int(dt_tw.timestamp())
            else:
                internal_date = int(full_msg.get("internalDate", "0"))
                return internal_date // 1000

        except Exception as e:
            logger.error(f"Gmail get_latest_message_time_async failed: {e}")
            return 0
