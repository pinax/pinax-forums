from django import forms

from .models import ForumReply, ForumThread


class PostForm:

    def __init__(self, *args, **kwargs):
        no_subscribe = kwargs.pop("no_subscribe", False)
        super().__init__(*args, **kwargs)
        if no_subscribe:
            del self.fields["subscribe"]


class ThreadForm(PostForm, forms.ModelForm):

    subscribe = forms.BooleanField(required=False)

    class Meta:
        model = ForumThread
        fields = ["title", "content"]


class ReplyForm(PostForm, forms.ModelForm):

    subscribe = forms.BooleanField(required=False)

    class Meta:
        model = ForumReply
        fields = ["content"]
