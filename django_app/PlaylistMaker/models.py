from django.db import models

"""
videosテーブル
videoid: 動画ID
title: 動画タイトル
channel: チャンネル名
image: サムネイル画像のURL
url: 動画のURL
views: 再生回数
published_date: 公開日
"""

# Create your models here.
class video_info(models.Model):
  videoid = models.CharField(max_length=100) #idは文字列なのでCharFieldを使った
  title = models.CharField(max_length=100) #titleとchannelは文字列なのでCharFieldを使った
  channel = models.CharField(max_length=100)
  image = models.CharField(max_length=200) #画像のURLを保存するフィールド
  url = models.URLField() #URlのみを保存するフィールド
  views = models.PositiveBigIntegerField() #再生回数は正の数かつ最も再生されている動画が100億ぐらいなのでこのフィールド
  published_date = models.DateTimeField(null=True, blank=True) #Datetimeを保存するやつ　これであってるか分からん
  is_selected = models.BooleanField(default=False)


  def __str__(self):
    return '<videos:id=' + str(self.id) + ', title=' + self.title + ', channel=' + self.channel + ', image=' + self.image + ', url=' + self.url + ', views=' + str(self.views) + ', published_date=' + str(self.published_date) + '>'