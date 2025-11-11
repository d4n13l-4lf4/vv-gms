from vv_gms.dani.models.teacher import Teacher


class TeacherRepository:
    def __init__(self, data):
        self.__data_ = data

    def get_teacher_by_id(self, teacher_id) -> Teacher | None:
        return self.__data_.get(teacher_id)
