from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from accounts.models import Topic, Answer
from accounts.forms import TopicForm, AnswerCreationForm
from django.core.paginator import Paginator



class TopicListView(ListView):
    template_name = "topic/index.html"
    context_object_name = "topics"
    ordering = ["-created_at"]
    queryset = Topic.objects.select_related('author')
    paginate_by = 5
    paginate_orphans = 1


class TopicCreateView(LoginRequiredMixin,CreateView):
    template_name = "topic/topic_create.html"
    form_class = TopicForm
    success_url = reverse_lazy("account:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("account:topic_detail", kwargs={"pk": self.object.pk})


class TopicDetailView(DetailView):
    template_name = "topic/topic_detail.html"
    queryset = Topic.objects.select_related('author').prefetch_related('answers__author')
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers_list = self.object.answers.all()
        paginator = Paginator(answers_list, self.paginate_by, orphans=self.paginate_orphans)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = page_obj.has_other_pages()
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

class AnswerUpdateView(UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerCreationForm
    template_name = "answer/answer_update.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("account:topic_detail", kwargs={"pk": self.object.topic.pk})


class AnswerDeleteView(UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = "answer/delete_confirm.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("account:topic_detail", kwargs={"pk": self.object.topic.pk})
