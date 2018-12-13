from django.conf.urls import url

from .views import (
    ForumsView,
    ForumCategoryView,
    ForumThreadView,
    ForumView,
    PostCreateView,
    ForumThreadReplyCreateView,
    ThreadEditView,
    ReplyEditView,
    SubscribeView,
    ThreadUpdatesView,
    UnsubscribeView,
)

app_name = "pinax_forums"

# Expected that these are mounted under namespace "pinax_forums"
urlpatterns = [
    url(r"^$", ForumsView.as_view(), name="forums"),
    url(r"^categories/(?P<pk>\d+)/$", ForumCategoryView.as_view(), name="category"),
    url(r"^forums/(?P<pk>\d+)/$", ForumView.as_view(), name="forum"),
    url(r"^threads/(?P<pk>\d+)/$", ForumThreadView.as_view(), name="thread"),
    url(r"^forums/(?P<pk>\d+)/posts/create/$", PostCreateView.as_view(), name="post_create"),
    url(r"^threads/(?P<pk>\d+)/reply/$", ForumThreadReplyCreateView.as_view(), name="reply_create"),
    url(r"^posts/(?P<pk>\d+)/edit-thread/$", ThreadEditView.as_view(), name="post_edit_thread"),
    url(r"^posts/(?P<pk>\d+)/edit-reply/$", ReplyEditView.as_view(), name="post_edit_reply"),
    # url(r"^post_edit/(thread|reply)/(\d+)/$", post_edit, name="post_edit"),
    url(r"^threads/(?P<pk>\d+)/subscribe/$", SubscribeView.as_view(), name="subscribe"),
    url(r"^threads/(?P<pk>\d+)/unsubscribe$", UnsubscribeView.as_view(), name="unsubscribe"),
    url(r"^thread_updates/$", ThreadUpdatesView.as_view(), name="thread_updates"),
]
