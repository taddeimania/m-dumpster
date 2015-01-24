
class WhereClauseFactory(object):

    base_where_in_clause = "{} in ({})"
    base_where_clause = "{} = {}"
    base_select = "select id from {} where {}"

    def __init__(self, join_value):
        self.join_value = join_value

    def construct_where_clause(self, instructions_list):
        subquery = self.create_subquery(instructions_list)
        return self.strip_first_select_from_query(subquery)

    def create_subquery(self, instructions_list):
        subquery = ""
        for index, table in self.reverse_and_enumerate_instructions(instructions_list):
            table = table.split("|")
            if not index:
                subquery = self.create_join_to_field(table)
            else:
                subquery = self.create_subquery_to_joining_table(table, subquery)
        return subquery

    def reverse_and_enumerate_instructions(self, instructions_list):
        return enumerate(reversed(instructions_list))

    def create_join_to_field(self, table):
        return self.base_select.format(table[0], self.base_where_clause.format(table[1], self.join_value))

    def create_subquery_to_joining_table(self, table, subquery):
        return self.base_select.format(table[0], self.base_where_in_clause.format(table[1], subquery))

    def strip_first_select_from_query(self, subquery):
        return subquery[subquery.index("("):]
