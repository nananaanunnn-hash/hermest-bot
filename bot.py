#!/usr/bin/env python3
"""
Bot Telegram Sederhana
Mendukung perintah dasar dan integrasi LLM
"""

import os
import logging
from dotenv import load_dotenv
import telebot
import requests

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = int(os.getenv("TELEGRAM_OWNER_ID", "0"))
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://integrate.api.nvidia.com/v1")
MODEL = os.getenv("DEFAULT_MODEL", "meta/llama-3.3-70b-instruct")

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(TOKEN)


def is_owner(message):
    return message.from_user.id == OWNER_ID


def ask_llm(prompt: str) -> str:
    """Kirim prompt ke LLM dan return responnya."""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        res = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers, timeout=30)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"


# ── Commands ──────────────────────────────────────────

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(message, "👋 Halo! Bot aktif.\nKetik /help untuk daftar perintah.")


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = (
        "📋 *Daftar Perintah:*\n\n"
        "/start — Mulai bot\n"
        "/help — Daftar perintah\n"
        "/ping — Cek bot aktif\n"
        "/ask [pertanyaan] — Tanya ke LLM\n"
        "/info — Info server (owner only)\n"
    )
    bot.reply_to(message, text, parse_mode="Markdown")


@bot.message_handler(commands=["ping"])
def cmd_ping(message):
    bot.reply_to(message, "🟢 Pong! Bot aktif.")


@bot.message_handler(commands=["ask"])
def cmd_ask(message):
    prompt = message.text.replace("/ask", "").strip()
    if not prompt:
        bot.reply_to(message, "⚠️ Contoh: /ask apa itu AI?")
        return
    bot.reply_to(message, "⏳ Memproses...")
    response = ask_llm(prompt)
    bot.reply_to(message, response)


@bot.message_handler(commands=["info"])
def cmd_info(message):
    if not is_owner(message):
        bot.reply_to(message, "⛔ Hanya owner yang bisa menggunakan perintah ini.")
        return
    import platform, psutil
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    text = (
        f"🖥️ *Info Server*\n\n"
        f"OS: {platform.system()} {platform.release()}\n"
        f"CPU: {cpu}%\n"
        f"RAM: {ram.used // 1024 // 1024}MB / {ram.total // 1024 // 1024}MB\n"
    )
    bot.reply_to(message, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    """Pesan biasa → kirim ke LLM."""
    if not is_owner(message):
        return
    bot.send_chat_action(message.chat.id, "typing")
    response = ask_llm(message.text)
    bot.reply_to(message, response)


if __name__ == "__main__":
    logging.info("Bot berjalan...")
    bot.infinity_polling()
