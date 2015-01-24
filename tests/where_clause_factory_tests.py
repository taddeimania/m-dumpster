import unittest

import mock

from dumpster.where_clause_factory import WhereClauseFactory


class WhereClauseFactoryTests(unittest.TestCase):

    def setUp(self):
        self.instructions_list = [
            'base_table|join_table_fk',
            'join_table|next_table_fk',
            'next_table|company'
        ]
        self.sut_class = WhereClauseFactory
        self.sut = self.sut_class(1983)

    def test_construct_where_clause_returns_formatted_string(self):
        result = self.sut.construct_where_clause(self.instructions_list)
        expected_result = "(select id from join_table where next_table_fk in (select id from next_table where company = 1983))"
        self.assertEqual(result, expected_result)

    @mock.patch('dumpster.where_clause_factory.WhereClauseFactory.reverse_and_enumerate_instructions')
    def test_create_subquery_calls_reverse_and_enumerate_instructions_for_iteration(self, iterable):
        self.sut.create_subquery(self.instructions_list)
        iterable.assert_called_once_with(self.instructions_list)

    @mock.patch('dumpster.where_clause_factory.WhereClauseFactory.reverse_and_enumerate_instructions')
    @mock.patch('dumpster.where_clause_factory.WhereClauseFactory.create_join_to_field')
    def test_create_subquery_calls_reverse_and_enumerate_instructions_for_iteration(self, join_to_field, iterable):
        iterable.return_value = enumerate(["base_table|company"])
        self.sut.create_subquery(self.instructions_list)
        join_to_field.assert_called_once_with(["base_table", "company"])

    @mock.patch('dumpster.where_clause_factory.WhereClauseFactory.create_join_to_field')
    @mock.patch('dumpster.where_clause_factory.WhereClauseFactory.create_subquery_to_joining_table')
    def test_create_subquery_calls_create_subquery_to_joining_table_with_not_first_in_list(self, *args):
        create_subquery_to_joining_table, create_join_to_field = args
        self.sut.create_subquery(self.instructions_list)
        arg_list = create_subquery_to_joining_table.call_args_list
        self.assertEqual(arg_list[0], mock.call(['join_table', 'next_table_fk'], create_join_to_field.return_value))
        self.assertEqual(arg_list[1], mock.call(['base_table', 'join_table_fk'], create_subquery_to_joining_table.return_value))

    def test_create_join_to_field_returns_formatted_string(self):
        result = self.sut.create_join_to_field(["base_table", "company"])
        expected_result = "select id from base_table where company = 1983"
        self.assertEqual(result, expected_result)

    def test_create_subquery_to_joining_table_returns_formatted_string(self):
        subquery = "select id from next_table where company = 1983"
        table = ['base_table', 'join_table_fk']
        result = self.sut.create_subquery_to_joining_table(table, subquery)
        expected_result = "select id from base_table where join_table_fk in (select id from next_table where company = 1983)"
        self.assertEqual(result, expected_result)

    def test_strip_first_select_removes_the_first_select_from_the_query(self):
        original_subquery = "select id from foo_table where foo_table_id in (select id from base_table where join_table_fk in (select id from join_table where company = 1983))"
        result = self.sut.strip_first_select_from_query(original_subquery)
        expected_subquery = "(select id from base_table where join_table_fk in (select id from join_table where company = 1983))"
        self.assertEqual(result, expected_subquery)
