import getpass

from dumpster.export_database import execute_database_copy


def main():
    host = raw_input("Enter the host:")
    login = raw_input("Enter the username for this host: ")
    password = getpass.getpass("Enter the password for this host: ")
    join_field = raw_input("Enter the name of the column you'd like to join to: ")
    join_value = raw_input("Enter the value of the column you'd like to export: ")
    database_name = raw_input("Name of remote database to dump: ")

    if host and login and password and join_field and join_value and database_name:
        execute_database_copy(join_field, join_value, host, login, password, database_name)
    else:
        print "Error => not enough information to run the database export"
