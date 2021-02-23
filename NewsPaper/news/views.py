from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Post, Author, Category, PostCategory, Comment, User
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import render
from django.views import View # импортируем простую вьюшку
from django.core.paginator import Paginator
from .filters import NewsFilter # импортируем недавно написанный фильтр
from .forms import PostForm
from django.views.generic import TemplateView



 
 
class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    queryset = Post.objects.order_by('-post_datetime')  #сортируем по уменьшению
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        #context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['logged_user'] = self.request.user.username
        return context

class PostDetailView(DetailView):
#    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news_detail.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
#    context_object_name = 'post'   # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    queryset = Post.objects.all()


class PostCreateView(CreateView):
#    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'add.html'
    #context_object_name = 'post_create'
    form_class = PostForm

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['logged_user'] = self.request.user.username
        return context


class PostSearch(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news_search.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'post_search'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    form_class = PostForm #добавил тут  добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст

        context['categories'] = Category.objects.all()
        context['form'] = PostForm()  # added
        context['logged_user'] = self.request.user.username
                
        return context

        #added below
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST запроса 
 
        if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
            form.save()
 
        return super().get(request, *args, **kwargs)

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    #model = Post
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        context['logged_user'] = self.request.user.username
        print('aaa')
        return context




 
# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
 


