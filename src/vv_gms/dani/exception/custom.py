
class CustomException(Exception):
    def __init__(self, message):
        self.__message_ = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"Error: {self.__message_}"