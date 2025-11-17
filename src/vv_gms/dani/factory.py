from vv_gms.dani.bootstrap import bootstrap
from vv_gms.dani.utils.persistance.sync_file import sync_file


class CommandFactory:
    @sync_file()
    def add_courses(self, data):
        return bootstrap(data).add_courses()

    @sync_file()
    def remove_course(self, data):
        return bootstrap(data).remove_course()

    @sync_file()
    def add_assignment(self, data):
        return bootstrap(data).add_assignment()

    @sync_file()
    def calc_stats(self, data):
        return bootstrap(data).calc_stats()

    @sync_file()
    def generate_report(self, data):
        return bootstrap(data).generate_report()