#클래스형 제네릭 뷰 임포트
from django.views.generic import ListView, DetailView,TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.conf import settings

#테이블 조회를 위해 post모델 클래스를임포트
from blog.models import Post

#검색 기능을 위해 forms에 만들어둔 form추가, Q클래스 임포트
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render


# ListView
class PostLV(ListView): 
    model = Post #post테이블 가져옴
    template_name = 'blog/post_all.html' #템플릿 파일을 지정한다. 지정하지 않을 경우 blog/post_list.html로 설정됨
    context_object_name = 'posts' #템플릿 파일에 넘겨주는 객체명을 posts로 변경, 변경해도 기존의 'object_list를 사용할 수 있음
    paginate_by = 2 #한 페이지에 보여주는 객체리스트의 숫자는 2로 설정. 장고가 페이징 기능을 제공함.

# DetailView
class PostDV(DetailView): 
    # DetailView 제네릭 뷰를 상속받아 PostDV 클래스형 뷰를 정의함. 
    # DetailView 제네릭 뷰는 테이블로부터 특정 객체를 가져와 그 객체의 상세 정보를 출력. 
    # 테이블에서 특정 객체를 조회하기 위한 키는 기본 키 대신 slug속성을 사용하고 있음. 
    # 이 slug파라미터는 URLconf에서 추출해 뷰로 넘겨줌.
    model = Post

    #템플릿에 넘겨줄 변수를 정의함.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}" #고유한 id를 만들어주기 위함. 
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}" #ex)http://127.0.0.1:8000/blog/post/99
        context['disqus_title'] = f"{self.object.slug}"
        return context


# ArchiveView
class PostAV(ArchiveIndexView):
    model = Post # 대상 테이블
    date_field = 'modify_dt' #기준이 되는 날짜 필드는 'modify_dt'를 사용함
    make_object_list = True #해당 연도에 해당하는 객체의 리스트를 만들어서 템플릿에 넘겨줍니다. 템플릿 파일에서 object_list 컨텍스트 변수를 사용할 수 있다.

class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'

class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

#FormView : GET 요청인 경우 폼을 화면에 보여줌. POST 요청의 경우 데이터의 유효성 검사를 한 후, 데이터가 유효하면 form_valid()함수를 실행한 후 리다이렉트 시킴.
#(하지만, 여기에서는 HttpResponse객체를 반환)
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)



