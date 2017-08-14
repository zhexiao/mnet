from rest_framework.exceptions import APIException


class MnetException(APIException):
    """
    自定义Exception
    """
    status_code = 400
    default_detail = 'Unexcepted error.'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return self.detail
