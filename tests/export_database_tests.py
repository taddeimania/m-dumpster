import unittest

import mock

from dumpster.export_database import execute_database_copy, attempt_database_connection


class ExecuteDatabaseCopyTests(unittest.TestCase):

    def setUp(self):
        self.dump_database_patch = mock.patch('dumpster.dump_database.DumpDatabase')
        self.dump_database = self.dump_database_patch.start()
        self.attempt_database_connection_patch = mock.patch('dumpster.export_database.attempt_database_connection')
        self.attempt_database_connection = self.attempt_database_connection_patch.start()

    def tearDown(self):
        mock.patch.stopall()

    def test_dump_database_object_instantiated_with_args(self):
        execute_database_copy("company", 1983, "dbhost", "login", "password", "database")
        self.dump_database.assert_called_once_with("company", 1983, "dbhost", "login", "password", "database")

    def test_dump_database_invoked(self):
        execute_database_copy("company", 1983, "dbhost", "login", "password", "database")
        self.dump_database.return_value.dump_database.assert_called_once_with()

    def test_invokes_attempt_database_connection(self):
        execute_database_copy("company", 1983, "dbhost", "login", "password", "database")
        self.attempt_database_connection.assert_called_once_with("dbhost", "login", "password", "database")


class AttemptDatabaseConnectionTests(unittest.TestCase):

    def setUp(self):
        self.popen_patch = mock.patch('subprocess.Popen')
        self.popen = self.popen_patch.start()

    def tearDown(self):
        mock.patch.stopall()

    def test_attempt_database_connection_instantiates_popen_with_args(self):
        attempt_database_connection("dbhost", "login", "password", "database")
        self.popen.assert_called_once_with(['mysql', '-h', 'dbhost', 'database', '-u', 'login', '-ppassword', '-e', 'show tables'], stderr=-2, stdout=-1)

    def test_attempt_database_connection_invokes_communicate_on_popen(self):
        attempt_database_connection("dbhost", "login", "password", "database")
        self.popen.return_value.communicate.assert_called_once_with()

    def test_attempt_raises_if_error_found_in_login_attempt(self):
        self.popen.return_value.communicate.return_value = ["ERROR"]
        with self.assertRaises(Exception):
            attempt_database_connection("dbhost", "login", "password", "database")

    def test_attempt_does_not_raise_if_error_not_found_in_login_attempt(self):
        self.popen.return_value.communicate.return_value = ["riddler"]
        with self.assertRaises(AssertionError):
            with self.assertRaises(Exception):
                attempt_database_connection("dbhost", "login", "password", "database")
