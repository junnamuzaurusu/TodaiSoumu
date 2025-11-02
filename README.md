# CaptainAndChiefOfficer (Django Webアプリケーション)

主将主務・会計Slackワークスペースのチャンネル一覧を取得し、指定したユーザーをすべてのチャンネルに招待するDjango Webアプリケーションです。

## セットアップ

### 1. リポジトリのクローン

```bash
git clone git@github.com:junnamuzaurusu/TodaiSoumu.git
cd sports
```

### 2. 仮想環境の作成とアクティベート

```bash
python -m venv slack_api
source slack_api/bin/activate  # macOS/Linux
# または
slack_api\Scripts\activate  # Windows
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env`ファイルをプロジェクトルート（`sports/`ディレクトリ）に作成し、以下の設定を行います：

```bash
# .envファイルを作成
touch .env

# .envファイルに以下を記述
CAPTAIN_CHIEF_OFFICER_TOKEN="<主将主務Slackのトークン>"
ACCOUNTING_TOKEN="<会計Slackのトークン>"
USER_NAME="<ログインユーザー名>"
PASSWORD="<ログインパスワード>"
```

**注意**: トークンの値が必要な場合は、管理者に連絡してください。

### 5. データベースマイグレーション（初回のみ）

```bash
cd app
python manage.py migrate
```

## 使用方法

### 開発サーバーの起動

```bash
cd app
python manage.py runserver
```

ブラウザで `http://localhost:8000/` にアクセスしてください。

### Webアプリケーションでの使用

1. **ログイン**
   - `http://localhost:8000/login/` にアクセス
   - `.env`ファイルに設定した`USER_NAME`と`PASSWORD`でログイン

2. **主将主務Slack一括招待**
   - ホーム画面から「主将主務Slack一括招待」をクリック
   - ユーザーIDを入力して「主将主務Slackに招待する」ボタンをクリック

3. **会計Slack一括招待**
   - ホーム画面から「会計Slack一括招待」をクリック（今後実装予定）

### ユーザーIDの取得方法

1. Slackで対象ユーザーのプロフィールを開く
2. 「その他」→「メンバーIDをコピー」
3. または、[こちらのガイド](https://intercom.help/yoom/ja/articles/5480063-slack%E3%81%AE%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BCid%E3%81%AE%E7%A2%BA%E8%AA%8D%E6%96%B9%E6%B3%95)を参考

## プロジェクト構造

```
sports/
├── app/                    # Djangoプロジェクト
│   ├── config/            # プロジェクト設定
│   │   ├── settings.py
│   │   └── urls.py
│   ├── main/              # メインアプリ
│   │   ├── views.py       # ビュー
│   │   ├── utils.py       # Slack API関連のユーティリティ
│   │   ├── forms.py       # フォーム
│   │   ├── urls.py        # アプリURL設定
│   │   └── templates/
│   │       └── main/      # テンプレート
│   ├── manage.py
│   └── db.sqlite3         # SQLiteデータベース（セッション管理用）
├── .env                   # 環境変数（.gitignoreに含まれている）
├── requirements.txt       # 依存関係
└── README.md
```

## 機能

- ✅ 簡易認証システム（.envベース）
- ✅ 主将主務Slackチャンネル一覧の取得
- ✅ ユーザーを全チャンネルに一括招待
- ✅ 実行結果のメッセージ表示
- 🔄 会計Slack一括招待（今後実装予定）

## エラーハンドリング

アプリケーションは以下のエラーを適切に処理します：

- `not_authed`: 認証エラー
- `invalid_auth`: 無効なトークン
- `missing_scope`: 必要なスコープが不足
- `not_in_channel`: ボットがチャンネルのメンバーではない
- `already_in_channel`: ユーザーが既にチャンネルのメンバー

エラーメッセージはブラウザ上に表示されます。

## 技術スタック

- **フレームワーク**: Django 5.2.7
- **データベース**: SQLite3（セッション管理のみ）
- **認証**: .envファイルベースの簡易認証
- **Slack API**: slack_sdk 3.37.0

## 注意事項

- データベースはセッション管理のみに使用しています
- 認証は`.env`ファイルの`USER_NAME`と`PASSWORD`で行われます
- トークンは`.env`ファイルに保存されるため、`.gitignore`に含まれています
