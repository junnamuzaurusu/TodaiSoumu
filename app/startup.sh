#!/bin/bash
# Azure App Service 起動スクリプト

# appディレクトリに移動（既にappディレクトリにいる場合はそのまま）
cd /home/site/wwwroot/app 2>/dev/null || cd "$(dirname "$0")" || exit 1

# マイグレーション実行
python manage.py migrate --noinput

# 静的ファイルの収集
python manage.py collectstatic --noinput

# Gunicornで起動（Azure App Service用）
# ポート番号は環境変数PORTから取得（Azureが自動設定）
gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 120 --access-logfile - --error-logfile -

