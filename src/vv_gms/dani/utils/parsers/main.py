from vv_gms.dani.models.course import Course
from vv_gms.dani.utils.mappers.dict import DictMapper
from vv_gms.dani.utils.parsers.csv_parser import CSVParser

if __name__ == '__main__':
    filename = "/Users/daniel/Documents/Code/vv-gms/tests/resources/data/TC_ADD_COURSE_05.csv"
    courses_converter = DictMapper(Course)
    courses_parser = CSVParser(courses_converter)

    gen = courses_parser.parse(filename)

    for data in gen:
        print(data)