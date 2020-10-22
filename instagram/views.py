from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Post
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, CreateView, \
    UpdateView, DeleteView
from .forms import PostForm
from django.urls import reverse, reverse_lazy


# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user #현재 로그인 된 인스턴스
#             post.save()
#             messages.success(request, '포스팅을 저장했습니다.')
#             return redirect(post)
#     else:
#         form = PostForm()
#
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': None,
#     })

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, '포스팅을 저장했습니다.')
        return super().form_valid(form)

post_new = PostCreateView.as_view()

# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     #  작성자 Check Tip
#     if post.author != request.user:
#         messages.error(request, '작성자만 수정할 수 있습니다.')
#         return redirect(post)
#
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save()
#             messages.success(request, '포스팅을 수정했습니다.')
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
#
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': post
#     })

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    # todo 49번째줄 구현해보자
    # todo 방법1 : def get(self):
    # todo 방법2 : def dispatch(self, request, *args, **kwargs):

    def form_valid(self, form):
        # self.object = form.save()
        messages.success(self.request, '포스팅을 수정했습니다.')
        return super().form_valid(form)

post_edit = PostUpdateView.as_view()

# @login_required
# def post_delete (request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '포스팅을 삭제했습니다.')
#         return redirect('instagram:post_list')
#
#     return render(request, 'instagram/post_confirm_delete.html', {
#         'post' : post
#     })

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('instagram:post_list')

    # def get_success_url(self):
    #     return reverse('instagram:post_list')


post_delete = PostDeleteView.as_view()



# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))

# @method_decorator(login_required, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    # template_name = 'instagram/post_list.html'
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super(PostListView, self).get_context_data(**kwargs)
    #     if 'search' in str(self.request):
    #         number = str(self.request).split('=')[1]
    #         context['post_list'] = Post.objects.filter(id=number[:-2])
    #
    #     return context

post_list = PostListView.as_view(queryset=Post.objects.all().order_by())

#
# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#
#     messages.info(request, 'messages 테스트')
#    # instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html', {
#         'post_list': qs,
#         'q': q
#     })


# def post_detail(request : HttpResponse, pk : int) -> HttpResponse:
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except Post.DoesNotExist:
#     #     raise Http404
#     post = get_object_or_404(Post, pk=pk)
#
#     return render(request, 'instagram/post_detail.html', {
#         'post': post,
#     })

# post_detail = DetailView.as_view(model=Post,
#                                  queryset=Post.objects.filter(is_public=True))

class PostDetailView(DetailView):
    model = Post

    # queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs




post_detail = PostDetailView.as_view()

# def archives_year(request, year):
#
#     return HttpResponse(f"{year}년 archives")

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)

post_archive_month = MonthArchiveView.as_view(model=Post, date_field='created_at', month_format='%m')
