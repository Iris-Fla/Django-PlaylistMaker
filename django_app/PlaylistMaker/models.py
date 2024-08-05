from django.db import models

# Create your models here.
class video_info(models.Model):
  # name = models.CharField(max_length=100)
  # mail = models.EmailField(max_length=200)
  # gender = models.BooleanField()
  # age = models.IntegerField(default=0)
  # birthday = models.DateField()
  title = models.CharField(max_length=100) #titleとchannelは文字列なのでCharFieldを使った
  channel = models.CharField(max_length=100)
  image = models.ImageField(width_field=image_width) #ImageFieldの使い方がこれであってるか分からん　一応画像の保存に使うっぽい
  url = models.URLField() #URlのみを保存するフィールド
  views = models.PositiveBigIntegerField() #再生回数は正の数かつ最も再生されている動画が100億ぐらいなのでこのフィールド
  published_date = models.DateTimeField(null=True, blank=True) #Datetimeを保存するやつ　これであってるか分からん


  def __str__(self): #オブジェクトを表示する際の出力形式をカスタマイズ
    return '<video:id=' + str(self.id) + ',' + \
      self.title + '(' + str(self.url) + ')>' #IDとtitleとurlを表示するためのメソッド