# 🤖 My AI Toolkit

Kumpulan script dan tools sederhana untuk produktivitas sehari-hari.

## Isi Project

| File | Fungsi |
|---|---|
| `bot.py` | Bot Telegram sederhana |
| `setup.sh` | Auto-install semua dependency |
| `utils.py` | Fungsi utilitas umum |
| `index.html` | Landing page project |

## Cara Pakai

### 1. Clone repo
```bash
git clone https://github.com/username/my-project.git
cd my-project
```

### 2. Install dependency
```bash
bash setup.sh
```

### 3. Isi konfigurasi
```bash
cp .env.example .env
nano .env
```

### 4. Jalankan bot
```bash
python3 bot.py
```

## Konfigurasi (.env)

```env
TELEGRAM_BOT_TOKEN=isi_token_dari_botfather
TELEGRAM_OWNER_ID=isi_user_id_kamu
OPENAI_API_KEY=isi_api_key_llm
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
```

## Requirements

- Python 3.10+
- pip
- VPS Linux (Ubuntu 22.04 recommended)

## License

MIT
