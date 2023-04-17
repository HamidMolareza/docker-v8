from typing import Optional

from on_rails import ResultDetail
from pylity import String


class FailResult(ResultDetail):
    """
    Represents a failed operation with a specific error code.
    This class is used for handled errors.
    """

    def __init__(self, code: int, message: Optional[str] = None):
        super().__init__(title=f"Operation failed with code {code}.",
                         code=code, message=message)

    def __str__(self):
        result = self.title
        if not String.is_none_or_empty(self.message):
            result += f"\n{self.message}\n"
        return result
