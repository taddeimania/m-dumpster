import os

from dumpster.where_clause_factory import WhereClauseFactory


class DumpQueryBuilder(object):
    base_command = "mysqldump -h {} -u {} -p{} {}"
    base_string = "{} {} --where '{}{}' > {}{}.sql --lock-tables=false"

    def __init__(self, join_field, join_value, host, login, password, database):
        self.host = host
        self.login = login
        self.password = password
        self.join_field = join_field
        self.join_value = join_value
        self.database = database

    @property
    def dump_dir(self):
        return os.path.abspath(os.path.dirname(__file__)) + "/dump/"

    @property
    def formatted_base_command(self):
        return self.base_command.format(self.host, self.login, self.password, self.database)

    def build_mysqldump_string(self, instructions_list, no_data=False):
        table_name = instructions_list[0][1:]
        formatted_string = self.formatted_base_command + " {} > {}{}.sql --lock-tables=false".format(
            table_name, self.dump_dir, table_name)
        return "".join([formatted_string, " --no-data"]) if no_data else formatted_string

    def build_no_join_mysqldump_string(self, instructions_list):
        instruction = instructions_list.pop()
        instruction = instruction.split("|")
        return self.base_string.format(
            self.formatted_base_command,
            instruction[0],
            "{} = ".format(self.join_field),
            self.join_value,
            self.dump_dir,
            instruction[0]
        )

    def build_join_mysqldump_string(self, instructions_list):
        table_name = ""
        main_column = ""
        for index, instructions in enumerate(instructions_list):
            main_column, table_name = self.get_non_join_field_tables_and_column(
                index,
                instructions,
                main_column,
                table_name
            )
        where_clause = WhereClauseFactory(self.join_value).construct_where_clause(instructions_list)
        return self.base_string.format(
            self.formatted_base_command, table_name, main_column, where_clause, self.dump_dir, table_name)

    def get_non_join_field_tables_and_column(self, index, instructions, main_column, table_name):
        table = instructions.split("|")
        if not index:
            table_name = table[index]
            main_column = table[1] + " in "
        return main_column, table_name
