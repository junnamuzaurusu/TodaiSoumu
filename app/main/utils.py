import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

def get_channels(messages_list=None, type=None):
    """チャンネルリストを取得し、メッセージを収集する"""
    if messages_list is None:
        messages_list = []
    
    # プロジェクトルートの.envファイルを読み込む
    from django.conf import settings
    env_path = settings.BASE_DIR.parent / '.env'
    load_dotenv(env_path)
    
    # 環境変数からトークンを取得
    if type == 'captain_chief_officer':
        captain_chief_officer_token = os.getenv("CAPTAIN_CHIEF_OFFICER_TOKEN")
    elif type == 'accounting':
        accounting_token = os.getenv("ACCOUNTING_TOKEN")
    
    if not captain_chief_officer_token:
        messages_list.append("❌ トークンが.envファイルに設定されていません。")
        return None, messages_list
    
    # Slackクライアントを初期化
    client = WebClient(token=captain_chief_officer_token)
    
    try:
        # トークンの認証情報を確認
        messages_list.append("トークンの認証情報を確認中...")
        auth_response = client.auth_test()
        
        if auth_response["ok"]:
            messages_list.append("✅ 認証成功!")
            
            # ボットトークンかどうかを判定
            is_bot_token = bool(auth_response.get('bot_id'))
            if not is_bot_token:
                messages_list.append("⚠️  警告: ユーザートークンを使用しています。プライベートチャンネルにアクセスするにはボットトークンが必要です")
        else:
            msg = f"❌ 認証テストエラー: {auth_response['error']}"
            return None, messages_list
        
        messages_list.append("=" * 50)
        
        # チャンネル一覧を取得
        messages_list.append("チャンネル一覧を取得中...")
        response = client.conversations_list(types='public_channel,private_channel')
        
        if response["ok"]:
            messages_list.append(f"✅ チャンネル一覧の取得に成功しました: {len(response['channels'])}チャンネル")
            
            return response['channels'], messages_list
                
        else:
            messages_list.append(f"❌ チャンネル取得エラー: {response['error']}")
            if response['error'] == 'missing_scope':
                scope_msg = "📋 プライベートチャンネルにアクセスするには以下のスコープが必要です: groups:read, channels:read"
                messages_list.append(scope_msg)
            return None, messages_list
            
    except SlackApiError as e:
        messages_list.append(f"Slack APIエラー: {e.response['error']}")
        if e.response['error'] == 'not_authed':
            messages_list.append("認証に失敗しました。トークンが正しいか確認してください。")
        elif e.response['error'] == 'invalid_auth':
            messages_list.append("無効なトークンです。トークンが正しいか確認してください。")
        elif e.response['error'] == 'missing_scope':
            messages_list.append("必要なスコープが不足しています。Slackアプリの設定を確認してください。")
        return None, messages_list
    except Exception as e:
        messages_list.append(f"予期しないエラーが発生しました: {e}")
        return None, messages_list

def invite_user_to_channel(channels, user_id, messages_list=None, type=None):
    """ユーザーをチャンネルに招待し、メッセージを収集する"""
    if messages_list is None:
        messages_list = []
    
    if channels is None:
        messages_list.append("❌ チャンネルリストが取得できませんでした。")
        return messages_list
    
    # プロジェクトルートの.envファイルを読み込む
    from django.conf import settings
    env_path = settings.BASE_DIR.parent / '.env'
    load_dotenv(env_path)
    
    # 環境変数からトークンを取得
    if type == 'captain_chief_officer':
        captain_chief_officer_token = os.getenv("CAPTAIN_CHIEF_OFFICER_TOKEN")
    elif type == 'accounting':
        accounting_token = os.getenv("ACCOUNTING_TOKEN")
    
    if not captain_chief_officer_token:
        messages_list.append("❌ トークンが.envファイルに設定されていません。")
        return messages_list
    
    client = WebClient(token=captain_chief_officer_token)

    messages_list.append("=" * 50)
    messages_list.append("ユーザーをチャンネルに招待中...")

    for channel in channels:
        channel_name = channel['name']
        channel_id = channel['id']
        
        try:
            # ユーザーを招待
            response = client.conversations_invite(channel=channel_id, users=user_id)
            messages_list.append(f"📢 チャンネル: {channel_name} (ID: {channel_id}) ✅️")            

        except SlackApiError as e:
            messages_list.append(f"📢 チャンネル: {channel_name} (ID: {channel_id}) ❌ エラー: {e.response.get('error', str(e))}")    
        except Exception as e:
            messages_list.append(f"📢 チャンネル: {channel_name} (ID: {channel_id}) ❌ エラー: {str(e)}")
    
    return messages_list

