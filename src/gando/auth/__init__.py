def logged_in(*args, **kwargs):
    request = kwargs.get('request')
    if not request:
        return False

    return request.user.is_authenticated


def user_first_name(*args, **kwargs):
    request = kwargs.get('request')
    if not request or not hasattr(request, 'user') or not hasattr(request.user, 'first_name'):
        return None

    return request.user.first_name


def user_last_name(*args, **kwargs):
    request = kwargs.get('request')
    if not request or not hasattr(request, 'user') or not hasattr(request.user, 'last_name'):
        return None

    return request.user.last_name


def user_username(*args, **kwargs):
    request = kwargs.get('request')
    if not request or not hasattr(request, 'user') or not hasattr(request.user, 'username'):
        return None

    return request.user.username
