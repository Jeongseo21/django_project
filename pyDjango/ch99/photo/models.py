from django.db import models
from django.urls import reverse
from photo.fields import ThumbnailImageField

class Album(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField('One Line Description', max_length=100, blank=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    #이 메소드에서는 들어온 객체를 지칭하는 url을 반환.
    def get_absolute_url(self):
        return reverse('photo:album_detail', args=(self.id,))
    
class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE) #소속된 앨범객체를 가리킴
    title = models.CharField('TITLE', max_length=30)
    description = models.TextField('Photo Description', blank=True)
    image = ThumbnailImageField(upload_to='photo/%y/%m') #upload_to옵션으로 저장할 위치를 지정. MEDIA_ROOT의 하위에 /photo/2019/08이라는 디렉터리를 만들고 사진을 저장함.
    upload_dt = models.DateTimeField('Upload Date', auto_now_add=True) #auto_now_add=True옵션으로 현재시각을 자동저장.

    class Meta:
        ordering = ('title',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=(self.id,))#들어온 객체를 지칭하는 url을 반환
