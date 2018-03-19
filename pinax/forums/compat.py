try:
    from account.decorators import LoginRequired
except ImportError:
    from django.contrib.auth.decorators import login_required # noqa