import typing


class CustomException(Exception):
    def __init__(self, message: typing.Optional[str] = None) -> None:
        self.message = message or ""


class MissingParameter(CustomException):
    def __init__(self, parameter: str) -> None:
        super().__init__(f'Missing required parameter: "{parameter}"!')


class WrongParameterValueType(CustomException):
    def __init__(self, parameter: str) -> None:
        super().__init__(f'Wrong value of parameter: "{parameter}"!')
