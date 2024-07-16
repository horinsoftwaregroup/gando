ENDUSER_FAIL = 'enduser_fail'
BASE_ENDUSER_FAIL_MESSAGE = ("Your request has failed for some reason. "
                             "Please do not repeat this request for the next 24 hours. "
                             "If the request is still not answered correctly after 24 hours, "
                             "contact support. "
                             "Thank you for your patience.")
BASE_ENDUSER_FAIL_STATUSCODE = 500
BASE_ENDUSER_FAIL_CODE = 'FAIL'

ENDUSER_ERROR = 'enduser_error'
BASE_ENDUSER_ERROR_MESSAGE = ("Your request form is incorrect. "
                              "Please do not repeat the request without revising the input data or "
                              "your request type. Please check the correct way to submit "
                              "the request according to the available guides and then try again.")
BASE_ENDUSER_ERROR_STATUSCODE = 400
BASE_ENDUSER_ERROR_CODE = 'error'

ENDUSER_WARNING = 'enduser_warning'
BASE_ENDUSER_WARNING_MESSAGE = ("be careful!!! "
                                "Your request may not have been answered in the best possible way."
                                " Reconsider sending your input data or how to send your request.")
BASE_ENDUSER_WARNING_STATUSCODE = 200
BASE_ENDUSER_WARNING_CODE = 'warning'
