import sys 
from util import get_channels, invite_user_to_channel


def main():
    if len(sys.argv) != 2:
        print("⚠️ 実行方法: \n" + \
            "\033[32m"+ \
            "python main.py <招待するユーザーのID>" + \
            "\033[0m")
        print("IDの取得方法は以下のURLを参考にしてください: \n" + \
            "\033[31m"+ \
            "https://intercom.help/yoom/ja/articles/5480063-slack%E3%81%AE%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BCid%E3%81%AE%E7%A2%BA%E8%AA%8D%E6%96%B9%E6%B3%95" + \
            "\033[0m")
        return
    invited_user_id = sys.argv[1]
    channels = get_channels()
    for channel in channels:
        print(channel['name'])
    #invite_user_to_channel(channels, invited_user_id)

if __name__ == "__main__":
    main()