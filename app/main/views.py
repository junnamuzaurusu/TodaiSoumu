from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import LoginForm

from .utils import invite_user_to_channel
from .utils import get_channels

@require_http_methods(["GET", "POST"])
def login_view(request):
    """ログインビュー"""
    # 既にログインしている場合はhomeにリダイレクト
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # データベースでユーザー認証
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # ログイン成功
                auth_login(request, user)
                messages.success(request, f'ようこそ、{user.username}さん！')
                return redirect('main:home')
            else:
                # ログイン失敗
                messages.error(request, 'ユーザー名またはパスワードが正しくありません。')
    else:
        form = LoginForm()
    
    return render(request, 'main/login.html', {'form': form})


@login_required
def home(request):
    """ホームビュー"""
    return render(request, 'main/home.html', {
        'user': request.user
    })


@login_required
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
        return render(request, 'main/captain_and_chief_officer.html', {
            'user': request.user
        })  

@login_required
def accounting(request):
    """会計ビュー"""
    return render(request, 'main/accounting.html', {
        'user': request.user
    })