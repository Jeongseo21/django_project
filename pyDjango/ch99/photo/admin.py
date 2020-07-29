from django.contrib import admin
from photo.models import Album, Photo

#앨범객체를 보여줄 때 객체에 연결된 사진객체를 같이 보여주기 위해서 세로로 나열되게 지정(TabularInline은 행으로 나열)
class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2 #추가로 입력할 수 있는 Photo 테이블 객체 수는 2 개.

@admin.register(Album)#데코레이터 장점 : 간편함.
class AlbumAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)#앨범 객체 수정 화면을 보여줄 때 PhotoInline에서 정의한 사항을 보여줌.
    list_display = ('id', 'name', 'description')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_dt')

