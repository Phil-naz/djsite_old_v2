from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView  # class LastView using for show several articles from database,
from django.contrib.auth.mixins import LoginRequiredMixin
# Функция render - встроенный шаблонизатор джанго                'DetailView' for 1 ordinary article, 'CreateView' for creating
from .forms import *
from .models import *
from .serializers import WomenSerializer
from .utils import *
from rest_framework import generics

class WomenAPIView(generics.ListAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# Menu in the file 'utils.py' (DataMixin)


class WomenHome(DataMixin, ListView):   # class 'ListView' includes paginator
    # class 'DataMixin' - functions from file 'utils.py'
    # paginate_by = 3   # count of articles, included 1 page - transfer to 'utils.py'
    model = Women   # will show articles from 'model.py' - 'Women'
    template_name = 'women/index.html'   # Way fo template. By default use 'women/women_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):   # for transfer dynamic data
        context = super().get_context_data(**kwargs)   # mandatory (обязательное) condition
#   import from function 'DataMixin' ('utils.py')
#        context['menu'] = menu   # MENU gets from 'women_tags.py'
#        context['title'] = 'Главная страница'   # we may transfer static data here
#        context['cat_selected'] = 0   # for 'Все категории' mark charged
        c_def = self.get_user_context(title = 'Главная страница')   # for adding to transferred class 'DataMixin'
        # this class created in file 'utils.py'
        context['cat_selected'] = 0
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):   # show entries (записи) marked 'is_published'
        return Women.objects.filter(is_published=True).select_related('cat')   # '.select_related' - optimization SQL query


def about(request):   # 'DataMixin' is not working here!
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):   # 'LoginRequiredMixin' working only with classes. For using in function DEF:
                                                            # over DEF add code '@login_required and import this function
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')   # transfer to URL after add article. With functon 'reverse_lazy' we can use names of URLs
    login_url = '/admin/'   # for reversing user, if he don't logined.
#    raise_exception = True   # for reversing to page 403 'Forbidden' (доступ запрещен)

    def get_context_data(self, *, object_list=None, **kwargs):   # for transfer dynamic data
        context = super().get_context_data(**kwargs)   # mandatory (обязательное) condition
        context['menu'] = menu   # MENU gets from 'women_tags.py'
#        context['title'] = 'Добавление статьи'   # we may transfer static data here
        c_def = self.get_user_context(title = 'Добавление статьи')   # class 'DataMixin'
        return dict(list(context.items()) + list(c_def.items()))   # combine (объединяем) classes ‘context’ & c_def (local data for transferring)


def contact(request):
    return HttpResponse('<h1>Feedback page</h1>')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Women   # will show articles from 'model.py' - 'Women'
    template_name = 'women/post.html'   # Way fo template. By default, use 'women/women_list.html'
    slug_url_kwarg = 'post_slug'   # for don't use mandatory name 'slug'
    # pk_url_kwarg = 'pk'   # for using article's number
    context_object_name = 'post'   # set name, witch transfer to HTML-template

    def get_context_data(self, *, object_list=None, **kwargs):   # for transfer dynamic data
        context = super().get_context_data(**kwargs)   # mandatory (обязательное) condition
        context['menu'] = menu   # MENU gets from 'women_tags.py'
#        context['title'] = context['post']   # we may transfer static data here
#        context['cat_selected'] = 0   # for 'Все категории' mark changed
        context['cat_selected'] = Women.cat_id
        c_def = self.get_user_context(title = context['post'])   # class 'DataMixin'
        return dict(list(context.items()) + list(c_def.items()))



# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False   # if incorrect URL '/category/xxx' show page 404

    def get_queryset(self):
        print(connection.queries)
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')   # '.select_related' - optimization SQL query


    def get_context_data(self, *, object_list=None, **kwargs):   # for transfer dynamic data
        context = super().get_context_data(**kwargs)   # mandatory (обязательное) condition
#        context['title'] = 'Категория: ' + str(context['posts'][0].cat)   # we may transfer static data here
#        context['cat_selected'] = context['posts'][0].cat_id   # for Наименование категории mark changed
#        return context
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title = 'Категория: ' + str(c.name), cat_selected = c.pk)   # class 'DataMixin'
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
# #    posts = Women.objects.filter(slug=cat_slug)   # cat_id
#     posts = Women.objects.filter(cat__slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {  # moving parameters to function 'return'
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#
#     return render(request, 'women/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm   # standard form in Django 'UserCreationForm'
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Регистрация')   # class 'DataMixin'
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):   # function if registration successfully
        user = form.save()
        login(self.request, user)   # maybe 1 argument, without (self.request)
        return redirect('home')



class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm   # standard form in Django 'AuthenticationForm'
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Авторизация')   # class 'DataMixin'
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):   # URL for redirecting authorizated user
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

class ContactFormView(DataMixin, FormView): # !!! FormView don't import in lesson
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)   # mandatory (обязательное) condition
        c_def = self.get_user_context(title = 'Обратная связь')   # class 'DataMixin'
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')
