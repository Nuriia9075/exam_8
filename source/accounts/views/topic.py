from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from accounts.models import Topic
from accounts.forms import TopicForm, AnswerCreationForm


class TopicListView(ListView):
    template_name = "topic/index.html"
    context_object_name = "topics"
    ordering = ["-created_at"]
    queryset = Topic.objects.select_related('author')
    paginate_by = 8
    paginate_orphans = 1


class TopicCreateView(LoginRequiredMixin,CreateView):
    template_name = "topic/topic_create.html"
    form_class = TopicForm
    success_url = reverse_lazy("account:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("topic_detail", kwargs={"pk": self.object.pk})


class TopicDetailView(DetailView):
    template_name = "topic/topic_detail.html"
    queryset = Topic.objects.select_related('author').prefetch_related('answers__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AnswerCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('account:login')
        form = AnswerCreationForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.topic = self.object
            answer.author = request.user
            answer.save()
            return redirect(reverse('account:topic_detail', kwargs={'pk': self.object.pk}))
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)

# class ArticleDetailView(DetailView):
#     template_name = "articles/article_view.html"
#     model = Article
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comments'] = self.object.comments.filter(author='asdqwe')
#         return context
#
#

#
#
# class ArticleUpdateView(UpdateView):
#     template_name = "articles/article_update.html"
#     form_class = ArticleForm
#     model = Article
#     # queryset = Article.objects.all()
#
#     # def get_success_url(self):
#     #     return reverse("detail", kwargs={"pk": self.object.pk})
#
# class ArticleDeleteView(DeleteView):
#     template_name = "articles/delete_confirm.html"
#     model = Article
#     form_class = ArticleDeleteForm
#     success_url = reverse_lazy("list")
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#
#         if self.request.method == 'POST':
#             kwargs['instance'] = self.object
#         return kwargs
#
#     # def post(self, request, *args, **kwargs):
#     #     article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
#     #     article.delete()
#     #     return redirect("list")