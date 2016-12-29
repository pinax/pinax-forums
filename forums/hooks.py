from forums.conf import settings


class ForumsDefaultHookSet(object):

    def can_access(self, request, forum):
        "can the given request access the given forum?"
        return True


class HookProxy(object):

    def __getattr__(self, attr):
        return getattr(settings.FORUMS_HOOKSET, attr)


hookset = HookProxy()
