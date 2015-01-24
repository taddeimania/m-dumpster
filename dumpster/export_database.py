import subprocess
from datetime import datetime

from dumpster import dump_database


def execute_database_copy(join_field, join_value, host, login, password, database):
    attempt_database_connection(host, login, password, database)
    start_time = datetime.now()
    print "Getting Database for {} = {}".format(join_field, join_value)
    dump_database.DumpDatabase(join_field, join_value, host, login, password, database).dump_database()
    end_time = datetime.now()
    total_time = end_time - start_time
    print "\n\nFinished dumping database in {}s".format(total_time.seconds)


def attempt_database_connection(host, login, password, database):
    login_attempt = subprocess.Popen(
        ['mysql', '-h', host, database, '-u', login, '-p{}'.format(password), '-e', 'show tables'],
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    ).communicate()[0]

    if "ERROR" in login_attempt:
        raise Exception(login_attempt)
