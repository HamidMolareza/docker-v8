from typing import Optional

from on_rails import ErrorDetail
from pylity import String
from pylity.decorators.validate_func_params import validate_func_params
from schema import And, Or, Schema


class FailResult(ErrorDetail):
    """
    Represents a failed operation with a specific error code.
    This class is used for handled errors.
    """

    @validate_func_params(schema=Schema({
        'code': And(int, error='The code param is required and must be an integer.'),
        'message': Or(None, And(str, lambda s: len(s.strip()) > 0,
                                error='The message must be None or non empty string')),
    }), raise_exception=True)
    def __init__(self, code: int, message: Optional[str] = None):
        super().__init__(title=f"Operation failed with code {code}.",
                         code=code, message=message)

    def __str__(self):
        result = self.title
        if not String.is_none_or_empty(self.message):
            result += f"\n{self.message}\n"
        return result
