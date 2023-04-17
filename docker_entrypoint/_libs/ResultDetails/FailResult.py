from typing import Optional

from on_rails import ResultDetail


class FailResult(ResultDetail):
    """
    Represents a failed operation with a specific error code.
    This class is used for handled errors.
    """

    def __init__(self, code: int, message: Optional[str] = None):
        super().__init__(title=f"Operation failed with code {code}.",
                         code=code, message=message)
