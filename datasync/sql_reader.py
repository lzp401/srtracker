__author__ = 'victorlu'

import sys


def read_sql_from_file(filepath, *args):
    try:
        sql_file = open(filepath, 'r')
    except:
        print 'Error to get SQL file from %s' % (filepath)
        exit(1)

    sql = sql_file.read()
    sql_file.close()

    if len(args) > 0:
        sql = sql.format(*args)

    return sql


def main(args):
    print read_sql_from_file(args[1], *args[2:])


if __name__ == '__main__':
    main(sys.argv)