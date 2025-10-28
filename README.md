# CaptainAndChiefOfficer

主将主務Slackワークスペースのチャンネル一覧を取得し、指定したユーザーをすべてのチャンネルに招待するPythonスクリプトです。


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
pip install -r requirement.txt
```

### 4. 環境変数の設定

`.env`ファイルを作成し、Slackボットトークンを設定：

```bash
# .envファイルを作成
touch .env

# .envファイルに以下を記述
# トークンの値を知りたいは私に連絡ください
CAPTAIN_CHIEF_OFFICER_TOKEN="<トークンの値>"
```

## 使用方法

### 基本的な使用方法

```bash
cd CaptainAndChiefOfficer
python main.py <ユーザーID>
```

### ユーザーIDの取得方法

1. Slackで対象ユーザーのプロフィールを開く
2. 「その他」→「メンバーIDをコピー」
3. または、[こちらのガイド](https://intercom.help/yoom/ja/articles/5480063-slack%E3%81%AE%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BCid%E3%81%AE%E7%A2%BA%E8%AA%8D%E6%96%B9%E6%B3%95)を参考

### 実行例

```bash
python main.py U09NE9GQGQP
```





## エラーハンドリング

スクリプトは以下のエラーを適切に処理します：

- `not_authed`: 認証エラー
- `invalid_auth`: 無効なトークン
- `missing_scope`: 必要なスコープが不足
- `not_in_channel`: ボットがチャンネルのメンバーではない
- `already_in_channel`: ユーザーが既にチャンネルのメンバー


