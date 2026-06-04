#!/bin/bash
# setup.sh — Auto install semua dependency

set -e

echo "🚀 Setup dimulai..."

# Update system
apt update -y && apt install -y python3 python3-pip python3-venv curl git

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install pyTelegramBotAPI python-dotenv requests psutil

# Buat .env dari example jika belum ada
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 File .env dibuat. Silakan isi konfigurasi:"
    echo "   nano .env"
fi

# Setup systemd service (opsional)
read -p "Install sebagai systemd service? (y/n): " INSTALL_SERVICE
if [ "$INSTALL_SERVICE" = "y" ]; then
    WORK_DIR=$(pwd)
    cat > /etc/systemd/system/mybot.service <<EOF
[Unit]
Description=My Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$WORK_DIR
ExecStart=$WORK_DIR/venv/bin/python3 $WORK_DIR/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    systemctl enable --now mybot
    echo "✅ Service mybot aktif!"
fi

echo ""
echo "✅ Setup selesai!"
echo "   Jalankan: source venv/bin/activate && python3 bot.py"
