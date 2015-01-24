
class JAMLParser(object):

    def line_is_company_specific_table(self, instructions_list):
        return instructions_list[0][0] not in ['#', '*']

    def line_is_join_record(self, instructions_list):
        return len(instructions_list) > 1 and self.line_is_company_specific_table(instructions_list)

    def line_is_not_join_record(self, instructions_list):
        return len(instructions_list) == 1 and self.line_is_company_specific_table(instructions_list)

    def line_is_full_table_dump(self, instructions_list):
        return instructions_list[0][0] == "*"

    def line_is_empty_table_dump(self, instructions_list):
        return instructions_list[0][0] == "#"
