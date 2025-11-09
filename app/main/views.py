import os
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv
from django.conf import settings

from .forms import LoginForm

from .utils import invite_user_to_channel
from .utils import get_channels


def login_required_custom(view_func):
    """簡易認証用のlogin_requiredデコレータ（.envベース）"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_logged_in', False):
            return redirect('main:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_http_methods(["GET", "POST"])
def login_view(request):
    """ログインビュー（.envベースの簡易認証）"""
    # 既にログインしている場合はhomeにリダイレクト
    if request.session.get('is_logged_in', False):
        return redirect('main:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # .envファイルから認証情報を読み込む（存在する場合のみ）
            # Render.comなどでは環境変数が直接設定されるため、.envファイルはオプショナル
            env_path = settings.BASE_DIR.parent / '.env'
            if env_path.exists():
                load_dotenv(env_path, override=True)
            
            # USER_NAME と USERNAME の両方を確認
            env_username = os.getenv('USERNAME') or os.getenv('USER_NAME')
            env_password = os.getenv('PASSWORD')
            
            # .envファイルの認証情報と照合
            if username == env_username and password == env_password:
                # ログイン成功 - セッションに保存
                request.session['is_logged_in'] = True
                request.session['username'] = username
                messages.success(request, f'ようこそ、{username}さん！')
                return redirect('main:home')
            else:
                # ログイン失敗
                messages.error(request, 'ユーザー名またはパスワードが正しくありません。')
    else:
        form = LoginForm()
    
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    """ログアウトビュー"""
    request.session.flush()
    messages.success(request, 'ログアウトしました。')
    return redirect('main:login')


@login_required_custom
def home(request):
    """ホームビュー"""
    username = request.session.get('username', 'ゲスト')
    return render(request, 'main/home.html', {
        'username': username
    })


@login_required_custom
def captain_and_chief_officer(request):
    """主将主務ビュー"""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if not user_id:
            messages.error(request, 'ユーザーIDを入力してください。')
            return redirect('main:captain-and-chief-officer')
        
        # チャンネルリストとメッセージを取得
        channels, log_messages = get_channels(type = 'captain_chief_officer')
        
        # 取得したメッセージを表示
        for msg in log_messages:
            if '✅' in msg:
                messages.success(request, msg)
            elif '❌' in msg or 'エラー' in msg:
                messages.error(request, msg)
            elif '⚠️' in msg:
                messages.warning(request, msg)
            else:
                messages.info(request, msg)
        
        if channels is None:
            return redirect('main:captain-and-chief-officer')
        
        channels = sorted(channels, key=lambda x: x['name'])
        # ユーザーを招待してメッセージを取得
        invite_messages = invite_user_to_channel(channels, user_id, log_messages, type = 'captain_chief_officer')
        
        # 招待結果のメッセージをすべて表示
        for msg in invite_messages:
            if '✅' in msg:
                messages.success(request, msg)
            elif '❌' in msg or 'エラー' in msg:
                messages.error(request, msg)
            elif '⚠️' in msg or '警告' in msg:
                messages.warning(request, msg)
            elif '📢' in msg or '📋' in msg or '💡' in msg:
                messages.info(request, msg)
            else:
                messages.info(request, msg)
        
        return redirect('main:captain-and-chief-officer')
    else:
        username = request.session.get('username', 'ゲスト')
        return render(request, 'main/captain_and_chief_officer.html', {
            'username': username
        })  

@login_required_custom
def accounting(request):
    """会計ビュー"""
    username = request.session.get('username', 'ゲスト')
    return render(request, 'main/accounting.html', {
        'username': username
    })