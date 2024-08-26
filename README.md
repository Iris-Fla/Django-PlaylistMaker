![top](https://github.com/user-attachments/assets/05b0605a-f964-4454-ad1d-b909d132f9b7)

# Django-PlaylistMaker
 Youtubeのプレイリストを作ります。
 こちらのアプリケーションは【技育CAMP2024】ハッカソン Vol.12で提出しました。
 提出した際のプレゼンテーション(デモ)→[GooglePresentation](https://docs.google.com/presentation/d/150LGL_8jzaAaG7jpunIpRTN-dr8uUMSgzHr9ilyE608/edit?usp=drive_link)

## YoutubeApiKeyを取得してください
取得方法についてはこちらの記事[Link](https://zenn.dev/eito_blog/articles/f2d870ffddb636)が分かりやすいです。.envに記載。

## OAuth2.0クライアントIDの取得も必要です。
OAuthクライアントのJSONを「client_secret.json」で保存し、django_app(db.sqlite3)と同ディレクトリに配置してください。

![image](https://github.com/user-attachments/assets/95a2bad9-b290-4b27-941c-fca0bd67a95a)

### 機能追加要素
- SQLiteを用いた絞り込み機能!
- より簡単なアプリケーション立ち上げ
- 導入の為の記事を作成✨

## アプリ起動
```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd .\django_app\
python manage.py migrate
python manage.py runserver  
```
