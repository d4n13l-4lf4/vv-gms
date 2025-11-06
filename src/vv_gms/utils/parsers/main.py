from vv_gms.models.course import Course
from vv_gms.utils.converters.base import GenericConverter
from vv_gms.utils.parsers.generic_parser import GenericParser

if __name__ == '__main__':
    filename = "/Users/daniel/Documents/Code/vv-gms/src/vv_gms/utils/parsers/data.csv"
    courses_converter = GenericConverter(Course)
    courses_parser = GenericParser(courses_converter)

    gen = courses_parser.parse(filename)

    for data in gen:
        print(data)