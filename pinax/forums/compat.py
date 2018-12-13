try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required  # noqa


try:
    from account.mixins import LoginRequiredMixin
except ImportError:
    from django.contrib.auth.mixins import LoginRequiredMixin  # noqa
