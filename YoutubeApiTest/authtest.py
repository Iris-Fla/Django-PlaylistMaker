import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_credentials(client_secret_file, scopes,
                    token_storage_pkl='token.pickle'):
    '''google_auth_oauthlibを利用してOAuth2認証

        下記URLのコードをほぼそのまま利用。Apache 2.0
        https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the_api_name
    '''
    creds = None
    # token.pickleファイルにユーザのアクセス情報とトークンが保存される
    # ファイルは初回の認証フローで自動的に作成される
    if os.path.exists(token_storage_pkl):
        with open(token_storage_pkl, 'rb') as token:
            creds = pickle.load(token)

    # 有効なクレデンシャルがなければ、ユーザーにログインしてもらう
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, scopes=scopes)
            creds = flow.run_local_server(port=0)

        # クレデンシャルを保存（次回以降の認証のため）
        with open(token_storage_pkl, 'wb') as token:
            pickle.dump(creds, token)

    return creds

'''OAuth認証と再生リストの作成'''
# 利用するAPIサービス
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# OAuthのスコープとクレデンシャルファイル
YOUTUBE_READ_WRITE_SCOPE = 'https://www.googleapis.com/auth/youtube'
CLIENT_SECRET_FILE = 'client_secret.json'

# OAuth認証：クレデンシャルを作成
creds = get_credentials(
                    client_secret_file=CLIENT_SECRET_FILE,
                    scopes=YOUTUBE_READ_WRITE_SCOPE
                    )

# API のビルドと初期化
youtube_auth = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    credentials=creds)

# Add Playlist
# This code creates a new, private playlist in the authorized user's channel.
playlists_insert_response = youtube_auth.playlists().insert(
  part="snippet,status",
  body=dict(
    snippet=dict(
      title='サンプルやで',
      description='APIで作成したプレイリスト'
    ),
    status=dict(
      privacyStatus="private"
    )
  )
).execute()

def add_videos_to_playlist(youtube_auth, playlist_id, video_ids):
    for video_id in video_ids:
        try:
            playlist_item = youtube_auth.playlistItems().insert(
                part="snippet",
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()
            print(f"動画 {video_id} をプレイリストに追加しました。")
        except Exception as e:
            print(f"動画 {video_id} の追加中にエラーが発生しました: {str(e)}")

# 使用例
playlist_id = playlists_insert_response['id']  # 作成したプレイリストのID
video_ids = ['PIbgoW7WIFc','0LUsucgY8q0']  # 追加したい動画のIDリスト

add_videos_to_playlist(youtube_auth, playlist_id, video_ids)