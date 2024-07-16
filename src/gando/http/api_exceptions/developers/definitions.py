DEVELOPER_EXCEPTION = 'developer_exception'
BASE_DEVELOPER_EXCEPTION_MESSAGE = ("Your request has encountered a problem for some reason. "
                                    "Please inform the software backend team as soon as possible "
                                    "so that it can be investigated and resolved.")
BASE_DEVELOPER_EXCEPTION_STATUSCODE = 500
BASE_DEVELOPER_EXCEPTION_CODE = 'developer_exception'

DEVELOPER_ERROR = 'developer_error'
BASE_DEVELOPER_ERROR_MESSAGE = ("The method of sending your request is incorrect. "
                                "Please refer to the relevant documents to know the correct way "
                                "to send the request and try again.")
BASE_DEVELOPER_ERROR_STATUSCODE = 400
BASE_DEVELOPER_ERROR_CODE = 'developer_error'

DEVELOPER_WARNING = 'developer_warning'
BASE_DEVELOPER_WARNING_MESSAGE = ("Your request has been answered, "
                                  "but there are certainly concerns. "
                                  "Please refer to the relevant documents for optimal use of "
                                  "this application to resolve these concerns.")
BASE_DEVELOPER_WARNING_STATUSCODE = 200
BASE_DEVELOPER_WARNING_CODE = 'developer_warning'
