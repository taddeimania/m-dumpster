import unittest

import mock

from dumpster.builder import DumpQueryBuilder


class DumpQueryBuilderTests(unittest.TestCase):

    def setUp(self):
        self.abs_path_patch = mock.patch('os.path.abspath')
        self.abs_path = self.abs_path_patch.start()
        self.abs_path.return_value = "/foo/bar/path"
        self.sut = DumpQueryBuilder("company", 1983, "dbhost", "login", "password", "dbname")

    def tearDown(self):
        mock.patch.stopall()

    def test_dump_dir_returns_abspath_with_path(self):
        self.abs_path.return_value = "/path"
        result = self.sut.dump_dir
        self.assertEqual(result, "/path/dump/")

    @mock.patch('os.path.dirname')
    def test_dump_dir_calls_dirname_with_file_location(self, dirname):
        self.sut.dump_dir
        dirname.assert_called_once_with(mock.ANY)

    @mock.patch('os.path.dirname')
    def test_dump_dir_calls_abspath_with_dirname_return_value(self, dirname):
        self.sut.dump_dir
        self.abs_path.assert_called_once_with(dirname.return_value)

    def test_formatted_base_command_returns_base_command_with_env_login_and_pass(self):
        base_command = self.sut.formatted_base_command
        self.assertEqual(base_command, "mysqldump -h dbhost -u login -ppassword dbname")

    def test_build_mysqldump_string_returns_string_without_no_data_param_by_default(self):
        instructions_list = ['*full_table_dump']
        result = self.sut.build_mysqldump_string(instructions_list)
        self.assertEqual(result, "mysqldump -h dbhost -u login -ppassword dbname full_table_dump > /foo/bar/path/dump/full_table_dump.sql --lock-tables=false")

    def test_build_mysqldump_string_returns_string_with_no_data_param_when_kwarg_exists(self):
        instructions_list = ['#empty_table_dump']
        result = self.sut.build_mysqldump_string(instructions_list, no_data=True)
        self.assertEqual(result, "mysqldump -h dbhost -u login -ppassword dbname empty_table_dump > /foo/bar/path/dump/empty_table_dump.sql --lock-tables=false --no-data")

    def test_build_no_join_mysqldump_string_returns_formatted_dump_string(self):
        instructions_list = ['base_table|company']
        result = self.sut.build_no_join_mysqldump_string(instructions_list)
        self.assertEqual(result, "mysqldump -h dbhost -u login -ppassword dbname base_table --where 'company = 1983' > /foo/bar/path/dump/base_table.sql --lock-tables=false")

    def test_build_join_mysqldump_string_returns_formatted_dump_string(self):
        instructions_list = [
            'base_table_one|joined_table_one_id',
            'joined_table_one|joined_table_two_id',
            'joined_table_two|company'
        ]
        result = self.sut.build_join_mysqldump_string(instructions_list)
        self.assertEqual(
            result,
            "mysqldump -h dbhost -u login -ppassword dbname base_table_one --where 'joined_table_one_id in (select id from joined_table_one where joined_table_two_id in (select id from joined_table_two where company = 1983))' > /foo/bar/path/dump/base_table_one.sql --lock-tables=false"
        )
