#클래스형 제네릭 뷰 임포트
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

#테이블 조회를 위해 post모델 클래스를임포트
from blog.models import Post

# ListView
class PostLV(ListView): 
    model = Post #post테이블 가져옴
    template_name = 'blog/post_all.html' #템플릿 파일을 지정한다. 지정하지 않을 경우 blog/post_list.html로 설정됨
    context_object_name = 'posts' #템플릿 파일에 넘겨주는 객체명을 posts로 변경, 변경해도 기존의 'object_list를 사용할 수 있음
    paginate_by = 2 #한 페이지에 보여주는 객체리스트의 숫자는 2로 설정. 장고가 페이징 기능을 제공함.



