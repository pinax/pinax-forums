from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, UpdateView

from .compat import LoginRequiredMixin
from .forms import ReplyForm, ThreadForm
from .hooks import hookset
from .models import (
    Forum,
    ForumCategory,
    ForumReply,
    ForumThread,
    ThreadSubscription,
    UserPostCount,
)


class ForumsView(ListView):

    template_name = "pinax/forums/forums.html"

    def stats(self):
        categories = ForumCategory.objects.filter(parent__isnull=True)
        categories = categories.order_by("title")

        most_active_forums = Forum.objects.order_by("-post_count")[:5]
        most_viewed_forums = Forum.objects.order_by("-view_count")[:5]
        most_active_members = UserPostCount.objects.order_by("-count")[:5]

        latest_posts = ForumReply.objects.order_by("-created")[:10]
        latest_threads = ForumThread.objects.order_by("-last_modified")
        most_active_threads = ForumThread.objects.order_by("-reply_count")
        most_viewed_threads = ForumThread.objects.order_by("-view_count")

        return {
            "categories": categories,
            "most_active_forums": most_active_forums,
            "most_viewed_forums": most_viewed_forums,
            "most_active_members": most_active_members,
            "latest_posts": latest_posts,
            "latest_threads": latest_threads,
            "most_active_threads": most_active_threads,
            "most_viewed_threads": most_viewed_threads,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**self.stats())
        return context


class ForumCategoryView(DetailView):

    model = ForumCategory
    context_object_name = "category"
    template_name = "pinax/forums/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forums"] = self.object.forums.order_by("title")
        return context


class ForumView(DetailView):

    model = Forum
    context_object_name = "forum"
    template_name = "pinax/forums/forum.html"

    def can_create_thread(self):
        return all([
            self.request.user.has_perm("forums.add_forumthread", obj=self.object),
            not self.object.closed,
        ])

    def threads(self):
        return self.object.threads.order_by("-sticky", "-last_modified")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["threads"] = self.threads()
        context["can_create_thread"] = self.can_create_thread()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not hookset.can_access(request, self.object):
            raise Http404()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ForumThreadView(FormView, DetailView):

    form_class = ReplyForm
    model = ForumThread
    context_object_name = "thread"
    template_name = "pinax/forums/thread.html"

    def get_queryset(self):
        return super().get_queryset().select_related("forum")

    def can_create_reply(self):
        return all([
            self.request.user.has_perm("forums.add_forumreply", obj=self.object),
            not self.object.closed,
            not self.object.forum.closed,
        ])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.can_create_reply():
            context["reply_form"] = context["form"]
        else:
            context["reply_form"] = None
        order_type = self.request.GET.get("order_type", "asc")
        context.update({
            "posts": ForumThread.objects.posts(self.object, reverse=(order_type == "desc")),
            "order_type": order_type,
            "subscribed": self.object.subscribed(self.request.user, "email"),
            "can_create_reply": self.can_create_reply(),
        })
        return context

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.thread = self.object
        reply.author = self.request.user
        reply.save()

        self.object.new_reply(reply)

        # subscribe the poster to the thread if requested (default value is True)
        if form.cleaned_data["subscribe"]:
            self.object.subscribe(reply.author, "email")

        # all users are automatically subscribed to onsite
        self.object.subscribe(reply.author, "onsite")

        return HttpResponseRedirect(reverse("pinax_forums:thread", args=[self.object.pk]))

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not hookset.can_access(request, self.object):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)
        self.object.inc_views()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if self.can_create_reply():
            return super().post(request, *args, **kwargs)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, FormView, DetailView):

    model = Forum
    context_object_name = "forum"
    form_class = ThreadForm
    template_name = "pinax/forums/post_create.html"

    def can_create_thread(self):
        return self.request.user.has_perm("forums.add_forumthread", obj=self.object)

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.forum = self.object
        thread.author = self.request.user
        thread.save()

        self.object.new_post(thread)

        # subscribe the poster to the thread if requested (default value is True)
        if form.cleaned_data["subscribe"]:
            thread.subscribe(thread.author, "email")

        # all users are automatically subscribed to onsite
        thread.subscribe(thread.author, "onsite")
        return HttpResponseRedirect(reverse("pinax_forums:thread", args=[thread.id]))

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not hookset.can_access(request, self.object):
            raise Http404()
        if self.object.closed:
            messages.error(request, "This forum is closed.")
            return HttpResponseRedirect(reverse("pinax_forums:forum", args=[self.object.id]))
        if not self.can_create_thread():
            messages.error(request, "You do not have permission to create a thread.")
            return HttpResponseRedirect(reverse("pinax_forums:forum", args=[self.object.id]))
        return super().dispatch(request, *args, **kwargs)


class ForumThreadReplyCreateView(LoginRequiredMixin, FormView, DetailView):

    model = ForumThread
    context_object_name = "thread"
    template_name = "pinax/forums/reply_create.html"
    form_class = ReplyForm

    def can_create_reply(self):
        return self.request.user.has_perm("forums.add_forumreply", obj=self.object)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not hookset.can_access(request, self.object):
            raise Http404()

        if thread.closed:
            messages.error(request, "This thread is closed.")
            return HttpResponseRedirect(reverse("pinax_forums:thread", args=[self.object.id]))

        if not self.can_create_reply():
            messages.error(request, "You do not have permission to reply to this thread.")
            return HttpResponseRedirect(reverse("pinax_forums:thread", args=[self.object.id]))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.thread = self.object
        reply.author = self.request.user
        reply.save()

        self.object.new_reply(reply)

        # subscribe the poster to the thread if requested (default value is True)
        if form.cleaned_data["subscribe"]:
            self.object.subscribe(reply.author, "email")

        # all users are automatically subscribed to onsite
        self.object.subscribe(reply.author, "onsite")

        return HttpResponseRedirect(reverse("pinax_forums:thread", args=[self.object.pk]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscribed"] = self.object.subscribed(self.request.user, "email")
        context["first_reply"] = not ForumReply.objects.filter(thread=self.object, author=self.request.user).exists()
        return context

    def get_initial(self):
        quote = self.request.GET.get("quote")  # thread id to quote
        initial = {}
        if quote:
            quote_reply = ForumReply.objects.get(id=int(quote))
            initial["content"] = "\"%s\"" % quote_reply.content
        return initial


class PostEditView(LoginRequiredMixin, UpdateView):

    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.editable(request.user):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("pinax_forums:thread", args=[self.thread_id])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"no_subscribe": True})
        return kwargs


class ThreadEditView(PostEditView):

    model = ForumThread
    form_class = ThreadForm

    @property
    def thread_id(self):
        return self.object.id


class ReplyEditView(PostEditView):

    model = ForumReply
    form_class = ReplyForm

    @property
    def thread_id(self):
        return self.object.thread.id


class SubscribeView(LoginRequiredMixin, DetailView):

    model = ForumThread
    context_object_name = "thread"
    template_name = "pinax/forums/subscribe.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.subscribe(request.user, "email")
        return HttpResponseRedirect(reverse("pinax_forums:thread", args=[self.object.id]))


class UnsubscribeView(LoginRequiredMixin, DetailView):

    model = ForumThread
    context_object_name = "thread"
    template_name = "pinax/forums/unsubscribe.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.unsubscribe(request.user, "email")
        return HttpResponseRedirect(reverse("pinax_forums:thread", args=[self.object.id]))


class ThreadUpdatesView(LoginRequiredMixin, ListView):

    model = ThreadSubscription
    template_name = "pinax/forums/thread_updates.html"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, kind="onsite")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriptions = self.get_queryset().select_related("thread", "user").order_by("-thread__last_modified")
        context["subscriptions"] = subscriptions
        return context

    def post(self, request, *args, **kwargs):
        subscription = get_object_or_404(self.get_queryset(), pk=request.POST["thread_id"])
        subscription.delete()
        return self.get(request, *args, **kwargs)
