FLOAT_TYPE = 'Float'
INTEGER_TYPE = 'Integer'
STRING_TYPE = 'String'
UUID_TYPE = 'UUID'
BOOLEAN_TYPE = 'Boolean'
DATETIME_TYPE = 'DateTime'
DATE_TYPE = 'Datetime'
TIME_TYPE = 'Time'
EMAIL_TYPE = 'Email'
LINK_TYPE = 'Link'
PASSWORD_TYPE = 'Password'
USERNAME_TYPE = 'Username'
PROPORTION_TYPE = 'Proportion'
IMAGE_TYPE_Default = 'Image'
BLURBASE64_TYPE = 'BlurBase64'
TEXT_TYPE = 'Text'
IMAGE_TYPE = {
    'directory_name': STRING_TYPE,
    'alt': STRING_TYPE,
    'height': INTEGER_TYPE,
    'width': INTEGER_TYPE,
    'size': INTEGER_TYPE,
    'proportion': PROPORTION_TYPE,
    'file_format': STRING_TYPE,
    'src': IMAGE_TYPE_Default,
    'blurbase64': BLURBASE64_TYPE,
    'description': TEXT_TYPE
}


def response_template_render(**kwargs):
    return {
        'success': kwargs.get('success', True),
        'status_code': kwargs.get('status_code', 200),
        'has_warning': kwargs.get('has_warning', False),
        'exception_status': kwargs.get('exception_status', False),
        'monitor': kwargs.get('monitor', {}),
        'messenger': kwargs.get('messenger', []),
        'many': kwargs.get('many', False),
        'data': kwargs.get('data', {'result': {}}),
        'messages': {
            'warning': kwargs.get('warning', []),
            'error': kwargs.get('error', []),
        }
    }


def response_template_render_many_false(**kwargs):
    return response_template_render(**kwargs)


def response_template_render_many_true(**kwargs):
    kwargs['many'] = True
    kwargs['data'] = kwargs.get('data', {})
    kwargs['data']['count'] = INTEGER_TYPE
    kwargs['data']['next'] = LINK_TYPE
    kwargs['data']['previous'] = LINK_TYPE
    return response_template_render(**kwargs)


RESPONSE_BODY_401 = response_template_render(
    success=False, status_code=401, exception_status=True, error=[
        {
            'not_authenticated': 'Authentication credentials were not provided.'
        }
    ])
