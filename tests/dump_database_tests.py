import unittest

import mock

from dumpster.dump_database import DumpDatabase


class DumpDatabaseExportTest(unittest.TestCase):

    def setUp(self):
        self.builder = mock.Mock()
        self.sut = DumpDatabase("company", 1983, "dbhost", "login", "password", "dbname")
        self.sut.builder = self.builder
        self.setup_patches()

    def setup_patches(self):
        self.execute_patch = mock.patch.object(DumpDatabase, 'execute_dump_list')
        self.execute = self.execute_patch.start()
        self.get_file_patch = mock.patch.object(DumpDatabase, 'get_file_to_parse')
        self.get_file = self.get_file_patch.start()

    def tearDown(self):
        self.execute_patch.stop()
        self.get_file_patch.stop()

    def test_invokes_build_join_mysql_string_when_parser_finds_line_is_join(self):
        self.get_file.return_value = [
            "base_table|join_table_fk > join_table|next_join_table_fk > next_join_table|company"
        ]
        self.sut.dump_database()
        expected_args = [
            'base_table|join_table_fk',
            'join_table|next_join_table_fk',
            'next_join_table|company'
        ]
        self.builder.build_join_mysqldump_string.assert_called_once_with(expected_args)

    def test_invokes_build_no_join_mysql_string_when_parser_finds_line_is_not_join(self):
        self.get_file.return_value = ["base_table|company"]
        self.sut.dump_database()
        expected_args = ['base_table|company']
        self.builder.build_no_join_mysqldump_string.assert_called_once_with(expected_args)

    def test_invokes_build_mysqldump_string_when_parser_finds_line_is_full_table_dump(self):
        self.get_file.return_value = ["*BATMAN!!!!!"]
        self.sut.dump_database()
        expected_arg = ['*BATMAN!!!!!']
        self.builder.build_mysqldump_string.assert_called_once_with(expected_arg)

    def test_invokes_build_mysqldump_string_when_parser_finds_line_is_table_schema_only(self):
        self.get_file.return_value = ["#robin"]
        self.sut.dump_database()
        expected_arg = ['#robin']
        self.builder.build_mysqldump_string.assert_called_once_with(expected_arg, no_data=True)

    def test_appends_join_mysql_dump_result_string_when_parser_finds_line_is_join(self):
        self.get_file.return_value = [
            "base_table|join_table_fk > join_table|next_table_fk > next_table|company"
        ]
        self.sut.dump_database()
        self.assertIn(self.builder.build_join_mysqldump_string.return_value, self.sut.dump_list)

    def test_appends_no_join_mysql_dump_result_string_when_parser_finds_line_is_not_join(self):
        self.get_file.return_value = ["base_table|company"]
        self.sut.dump_database()
        self.assertIn(self.builder.build_no_join_mysqldump_string.return_value, self.sut.dump_list)

    def test_appends_mysql_dump_result_string_to_dump_list_when_parser_finds_line_is_full_table_dump(self):
        self.get_file.return_value = ["*BATMAN!!!!!"]
        self.sut.dump_database()
        self.assertIn(self.builder.build_mysqldump_string.return_value, self.sut.dump_list)

    def test_appends_mysql_dump_result_string_to_dump_list_when_parser_finds_line_is_table_schema_only(self):
        self.get_file.return_value = ["#robin"]
        self.sut.dump_database()
        self.assertIn(self.builder.build_mysqldump_string.return_value, self.sut.dump_list)

    @mock.patch('dumpster.dump_database.DumpDatabase.get_mysql_dump_string')
    def test_get_mysql_dump_string_gets_invoked_for_each_line_in_the_file(self, get_mysql_dump_string):
        self.get_file.return_value = ["#joker", "*batman"]
        self.sut.dump_database()
        self.assertEqual(2, get_mysql_dump_string.call_count)


class DumpDatabaseGetFileTests(unittest.TestCase):

    def setUp(self):
        self.sut = DumpDatabase("", "", "", "", "", "")
        self.start_patches()

    def start_patches(self):
        self.abs_path_patch = mock.patch('os.path.abspath')
        self.abs_path = self.abs_path_patch.start()
        self.open_patch = mock.patch('__builtin__.open')
        self.open = self.open_patch.start()
        self.dirname_patch = mock.patch('os.path.dirname')
        self.dirname = self.dirname_patch.start()

    def tearDown(self):
        mock.patch.stopall()

    def test_get_file_to_parse_calls_open_with_path(self):
        self.sut.get_file_to_parse()
        self.open.assert_called_once_with('{}/tablemap.jaml'.format(self.abs_path.return_value))

    def test_get_file_to_parse_returns_file(self):
        result = self.sut.get_file_to_parse()
        self.assertEqual(result, self.open.return_value)

    def test_get_file_to_parse_calls_abspath_on_dirname_result(self):
        self.sut.get_file_to_parse()
        self.abs_path.assert_called_once_with(self.dirname.return_value)

    def test_get_file_to_parse_calls_dirname_with_dunder_file(self):
        self.sut.get_file_to_parse()
        self.dirname.assert_called_once_with(mock.ANY)


class DumpDatabaseExecuteTests(unittest.TestCase):

    @mock.patch('os.system')
    def test_execute_dump_list_calls_os_system_for_each_item_in_dump_list(self, os_system):
        sut = DumpDatabase("", "", "", "", "", "")
        dump_list = ["one", "two", "three"]
        sut.execute_dump_list(dump_list)
        self.assertEqual(3, os_system.call_count)

    @mock.patch('os.system')
    def test_execute_dump_list_calls_os_system_with_instruction_for_each_item_in_dump_list(self, os_system):
        sut = DumpDatabase("", "", "", "", "", "")
        dump_list = ["one", "two", "three"]
        sut.execute_dump_list(dump_list)
        self.assertEqual(mock.call('one'), os_system.call_args_list[0])
        self.assertEqual(mock.call('two'), os_system.call_args_list[1])
        self.assertEqual(mock.call('three'), os_system.call_args_list[2])
