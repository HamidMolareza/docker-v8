from on_rails import ResultDetail


class FailResult(ResultDetail):
    def __init__(self, code: int):
        super().__init__(title=f"Operation failed with code {code}.", code=code)
