import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

def get_channels():
    load_dotenv()
    
    # 環境変数からトークンを取得
    captain_chief_officer_token = os.getenv("CAPTAIN_CHIEF_OFFICER_TOKEN")
    
    # Slackクライアントを初期化
    client = WebClient(token=captain_chief_officer_token)
    
    try:
        # トークンの認証情報を確認
        print("トークンの認証情報を確認中...")
        auth_response = client.auth_test()
        
        if auth_response["ok"]:
            print(f"✅ 認証成功!")
            
            # ボットトークンかどうかを判定
            is_bot_token = bool(auth_response.get('bot_id'))
            if not is_bot_token:
                print("\n⚠️  警告: ユーザートークンを使用しています")
                print("   プライベートチャンネルにアクセスするにはボットトークンが必要です")
        else:
            print(f"❌ 認証テストエラー: {auth_response['error']}")
            return []
        
        print("\n" + "="*50)
        
        # チャンネル一覧を取得
        print("チャンネル一覧を取得中...")
        response = client.conversations_list(types='public_channel,private_channel')
        
        if response["ok"]:
            print("✅ チャンネル一覧の取得に成功しました:")
            
            return response['channels']
                
        else:
            print(f"❌ チャンネル取得エラー: {response['error']}")
            if response['error'] == 'missing_scope':
                print("\n📋 プライベートチャンネルにアクセスするには以下のスコープが必要です:")
                print("   - groups:read (プライベートチャンネルを読み取り)")
                print("   - channels:read (パブリックチャンネルを読み取り)")
                print("\n🔧 Slackアプリの設定でこれらのスコープを追加してください:")
                print("   https://api.slack.com/apps でアプリを選択 → OAuth & Permissions → Scopes")
            return []
            
    except SlackApiError as e:
        print(f"Slack APIエラー: {e.response['error']}")
        if e.response['error'] == 'not_authed':
            print("認証に失敗しました。トークンが正しいか確認してください。")
        elif e.response['error'] == 'invalid_auth':
            print("無効なトークンです。トークンが正しいか確認してください。")
        elif e.response['error'] == 'missing_scope':
            print("必要なスコープが不足しています。Slackアプリの設定を確認してください。")
        return []
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return []

def invite_user_to_channel(channels, user_id):
    load_dotenv()
    
    # 環境変数からトークンを取得
    captain_chief_officer_token = os.getenv("CAPTAIN_CHIEF_OFFICER_TOKEN")
    client = WebClient(token=captain_chief_officer_token)

    print("=" * 50)
    print("ユーザーをチャンネルに招待中...")
    print("=" * 50)

    for channel in channels:
        channel_name = channel['name']
        channel_id = channel['id']
        
        
        
        try:
            # ユーザーを招待
            response = client.conversations_invite(channel=channel_id, users=user_id)
            print(f"\n📢 チャンネル: {channel_name} (ID: {channel_id}) ✅️")

        except Exception as e:
            print(f"\n📢 チャンネル: {channel_name} (ID: {channel_id})")
            print(f"\033[31m{channel_name}にユーザーをチャンネルに招待できませんでした: {e.response['error']}\033[0m")

