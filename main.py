"""Modul utama untuk aplikasi otomatisasi Telegram.

Aplikasi ini mengotomatiskan pengiriman pesan teks dari channel sumber ke grup target
dengan fitur blacklist dan logging.
"""

import asyncio
import json
import os
import random
import time
from typing import Optional, Union

from telethon.errors import (
    ChatIdInvalidError,
    ChatWriteForbiddenError,
    FloodWaitError,
    PeerIdInvalidError,
    SlowModeWaitError,
    UserBannedInChannelError,
    UserBlockedError,
)
from telethon.sync import TelegramClient
from telethon.tl.types import Channel

# Load configuration
with open("config.json", encoding="utf-8") as config_file:
    config = json.load(config_file)

API_ID = config["telegram"]["api_id"]
API_HASH = config["telegram"]["api_hash"]
MESSAGE_SOURCE_CHANNEL = config["telegram"]["message_source_channel"]
GROUP_LIST_CHANNEL = config["telegram"]["group_list_channel"]
MIN_DELAY_MESSAGE = config["delays"]["min_delay_message"]
MAX_DELAY_MESSAGE = config["delays"]["max_delay_message"]
MIN_DELAY_CYCLE = config["delays"]["min_delay_cycle"]
MAX_DELAY_CYCLE = config["delays"]["max_delay_cycle"]

BLACKLIST_FILE = "blacklist.json"
LOG_FILE = "activity.log"

client = TelegramClient("telegram", API_ID, API_HASH)

async def get_messages_from_channel(channel_entity: Channel) -> list[str]:
    """Mengambil semua pesan teks dari channel sumber."""
    messages = []
    async for message in client.iter_messages(channel_entity):
        if message.text:
            messages.append(message.text)
    return messages


async def get_groups_from_channel(channel_entity: Channel) -> list[int]:
    """Mengambil daftar grup dari channel target, memproses setiap baris pesan.

    Mencoba mendapatkan entitas dari setiap baris pesan dan memvalidasi apakah
    itu adalah grup atau channel yang valid.
    """
    groups = []
    async for message in client.iter_messages(channel_entity):
        if message.text:
            lines = message.text.splitlines()
            for line in lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    entity = await client.get_entity(line)
                    if isinstance(entity, Channel) and entity.megagroup:
                        groups.append(entity.id)
                    elif line.isdigit():
                        groups.append(int(line))
                    else:
                        log_activity(
                            f"Entitas {line} bukan grup/channel yang valid atau megagroup.",
                            status="WARNING",
                        )
                except Exception as e:
                    log_activity(f"Gagal mendapatkan entitas dari {line}: {e}", status="WARNING")
                    blacklist = load_blacklist()
                    blacklist_permanent: list[int] = blacklist.get("permanent", [])  # type: ignore
                    if line.isdigit():
                        group_id = int(line)
                    else:
                        # For non-numeric lines (usernames), we can't add them to the integer-based permanent blacklist directly.
                        # A more robust solution would be to store usernames in a separate blacklist or resolve them to IDs if possible.
                        # For now, we'll just log the warning and skip blacklisting.
                        log_activity(f"Tidak dapat menambahkan '{line}' ke blacklist permanen karena bukan ID numerik.", status="WARNING")
                        continue

                    if group_id not in blacklist_permanent:
                        blacklist_permanent.append(group_id)
                        blacklist["permanent"] = blacklist_permanent
                        save_blacklist(blacklist)
    return groups


def load_blacklist() -> dict[str, Union[list[int], dict[str, float]]]:
    """Memuat daftar blacklist dari file JSON."""
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, encoding="utf-8") as blacklist_file_read:
            loaded_data = json.load(blacklist_file_read)
            if "temporary" not in loaded_data or not isinstance(loaded_data["temporary"], dict):
                loaded_data["temporary"] = {}
            return loaded_data
    return {"permanent": [], "temporary": {}}


def save_blacklist(blacklist: dict[str, Union[list[int], dict[str, float]]]) -> None:
    with open(BLACKLIST_FILE, "w", encoding="utf-8") as blacklist_file_write:
        json.dump(blacklist, blacklist_file_write, indent=4)


def clean_expired_blacklist(
    blacklist: dict[str, Union[list[int], dict[str, float]]],
) -> dict[str, Union[list[int], dict[str, float]]]:
    """Membersihkan entri blacklist sementara yang sudah kadaluarsa."""
    current_time = time.time()
    temporary_blacklist = blacklist.get("temporary", {})
    if not isinstance(temporary_blacklist, dict):
        temporary_blacklist = {}
    expired_entries = [
        group_id
        for group_id, expiry_time in temporary_blacklist.items()
        if current_time > expiry_time
    ]
    for group_id in expired_entries:
        del temporary_blacklist[str(group_id)]
    if expired_entries:
        log_activity(f"Cleaned expired temporary blacklist entries: {expired_entries}")
        # Update the original blacklist with the modified temporary_blacklist
        blacklist["temporary"] = temporary_blacklist
        save_blacklist(blacklist)
    return blacklist


def log_activity(
    message: str,
    group_id: Optional[int] = None,
    status: str = "INFO",
    error: Optional[Exception] = None,
) -> None:
    """Mencatat aktivitas aplikasi ke file log dan konsol."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{status}]"
    if group_id:
        log_entry += f" [Group ID: {group_id}]"
    log_entry += f" {message}"
    if error:
        log_entry += f" (Error: {error})"
    with open(LOG_FILE, "a", encoding="utf-8") as log_file_write:
        log_file_write.write(log_entry + "\n")
    print(log_entry)


async def send_message_to_group(group_id: int, message_text: str) -> bool:
    """Mengirim pesan ke grup tertentu dan menangani berbagai error."""
    try:
        await client.send_message(group_id, message_text)
        log_activity("Pesan berhasil dikirim", group_id=group_id, status="SUCCESS")
        return True
    except (
        ChatWriteForbiddenError,
        UserBlockedError,
        UserBannedInChannelError,
        ChatIdInvalidError,
        PeerIdInvalidError,
    ) as e:
        log_activity(f"Gagal mengirim pesan: {e}", group_id=group_id, status="FAILED", error=e)
        blacklist = load_blacklist()
        blacklist_permanent: list[int] = blacklist.get("permanent", [])  # type: ignore
        if group_id not in blacklist_permanent:
            blacklist_permanent.append(group_id)
            blacklist["permanent"] = blacklist_permanent
        save_blacklist(blacklist)
        return False
    except SlowModeWaitError as e:
        log_activity(
            f"SlowModeWait terdeteksi, melewati grup ini untuk siklus saat ini: {e}",
            group_id=group_id,
            status="BLACKLIST_TEMPORARY",
        )
        return False
    except FloodWaitError as e:
        wait_time = e.seconds
        blacklist = load_blacklist()
        temp_blacklist: dict[str, float] = blacklist.get("temporary", {})  # type: ignore
        if not isinstance(temp_blacklist, dict):
            temp_blacklist = {}
        temp_blacklist[str(group_id)] = (
            time.time() + wait_time + 60  # Add 60 seconds buffer
        )
        blacklist["temporary"] = temp_blacklist
        log_activity(
            f"FloodWait terdeteksi, grup ditambahkan ke blacklist sementara "
            f"selama {wait_time} detik: {e}",
            group_id=group_id,
            status="BLACKLIST_TEMPORARY",
        )
        save_blacklist(blacklist)
        return False
    except Exception as e:
        log_activity(
            f"Terjadi kesalahan tidak terduga saat mengirim pesan: {e}",
            group_id=group_id,
            status="FAILED",
            error=e,
        )
        return False


async def main() -> None:
    """Fungsi utama aplikasi otomatisasi Telegram."""
    log_activity("Aplikasi dimulai")
    await client.start()
    log_activity("Login ke Telegram berhasil")

    try:
        message_source_entity = await client.get_entity(MESSAGE_SOURCE_CHANNEL)
        group_list_entity = await client.get_entity(GROUP_LIST_CHANNEL)
    except Exception as e:
        log_activity(
            f"Gagal mendapatkan entitas channel: {e}. Pastikan channel ID/username "
            "benar dan akun memiliki akses.",
            status="ERROR",
        )
        await client.run_until_disconnected()
        return

    while True:
        log_activity("Memulai siklus baru")
        messages = await get_messages_from_channel(message_source_entity)
        if not messages:
            log_activity("Tidak ada pesan ditemukan di channel sumber. Menunggu siklus berikutnya.")
            await asyncio.sleep(random.uniform(MIN_DELAY_CYCLE * 3600, MAX_DELAY_CYCLE * 3600))
            continue

        groups = await get_groups_from_channel(group_list_entity)
        if not groups:
            log_activity("Tidak ada grup ditemukan di channel target. Menunggu siklus berikutnya.")
            await asyncio.sleep(random.uniform(MIN_DELAY_CYCLE * 3600, MAX_DELAY_CYCLE * 3600))
            continue

        blacklist = load_blacklist()
        blacklist = clean_expired_blacklist(blacklist)

        valid_groups = [
            g
            for g in groups
            if g not in blacklist["permanent"] and str(g) not in blacklist["temporary"]
        ]
        if not valid_groups:
            log_activity(
                "Tidak ada grup valid untuk dikirimi pesan setelah pemeriksaan blacklist. "
                "Menunggu siklus berikutnya."
            )
            await asyncio.sleep(random.uniform(MIN_DELAY_CYCLE * 3600, MAX_DELAY_CYCLE * 3600))
            continue

        log_activity(f"Ditemukan {len(valid_groups)} grup valid untuk dikirimi pesan.")
        for group_id in valid_groups:
            message_to_send = random.choice(messages)
            log_activity(f"Mencoba mengirim pesan ke grup {group_id}", group_id=group_id)
            await send_message_to_group(group_id, message_to_send)
            await asyncio.sleep(random.uniform(MIN_DELAY_MESSAGE, MAX_DELAY_MESSAGE))

        log_activity("Siklus pengiriman pesan selesai. Menunggu delay antar siklus.")
        await asyncio.sleep(random.uniform(MIN_DELAY_CYCLE * 3600, MAX_DELAY_CYCLE * 3600))


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
