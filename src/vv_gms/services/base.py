from abc import ABC, abstractmethod

class ICourseService(ABC):
    @abstractmethod
    def add_courses(self, filename: str):
        pass