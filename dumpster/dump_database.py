import os

from dumpster.builder import DumpQueryBuilder
from dumpster.parser import JAMLParser


class DumpDatabase(object):

    def __init__(self, *args):
        self.dump_list = []
        self.parser = JAMLParser()
        self.builder = DumpQueryBuilder(*args)

    def dump_database(self):
        for line in self.get_file_to_parse():
            print line
            instructions_list = line.replace("\n", "").replace(" ", "").split(">")
            self.dump_list.append(self.get_mysql_dump_string(instructions_list))
        self.execute_dump_list(self.dump_list)

    def get_mysql_dump_string(self, instructions_list):
        if self.parser.line_is_join_record(instructions_list):
            return self.builder.build_join_mysqldump_string(instructions_list)
        elif self.parser.line_is_not_join_record(instructions_list):
            return self.builder.build_no_join_mysqldump_string(instructions_list)
        elif self.parser.line_is_full_table_dump(instructions_list):
            return self.builder.build_mysqldump_string(instructions_list)
        elif self.parser.line_is_empty_table_dump(instructions_list):
            return self.builder.build_mysqldump_string(instructions_list, no_data=True)

    def get_file_to_parse(self):
        table_map_file = "tablemap.jaml"
        file_dir = os.path.abspath(os.path.dirname(__file__))
        return open("{}/{}".format(file_dir, table_map_file))

    def execute_dump_list(self, dump_list):
        for idx, instruction in enumerate(dump_list):
            os.system(instruction)
