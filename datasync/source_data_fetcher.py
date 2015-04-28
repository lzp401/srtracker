__author__ = 'victorlu'

import cx_Oracle
import psycopg2
import csv
import time
import os
import sys
import srtracker_conf
import sql_reader


def pgconn():
    return psycopg2.connect(
        database=srtracker_conf.pg_config['database'],
        user=srtracker_conf.pg_config['user'],
        password=srtracker_conf.pg_config['password'],
        host=srtracker_conf.pg_config['host']
    )


def csv_import(data):
    now = time.time()

    sys.stdout.write('Importing data to CSV')

    csvfile = os.tmpfile()
    writer = csv.writer(csvfile, delimiter=srtracker_conf.csv_file_conf['delimiter'])
    writer.writerows(data)

    sys.stdout.write(' - Done [%fs Used]\n' % (time.time() - now))

    return csvfile


def pg_init(conn, fd):
    cur = conn.cursor()
    now = time.time()

    sys.stdout.write('Import CSV data to temp table ')

    # Create temp table to import CSV file to
    sql = sql_reader.read_sql_from_file(
        srtracker_conf.pg_config['sql'][0],
        srtracker_conf.pg_config['temp_table'],
    )
    cur.execute(sql)

    # Import CSV file into temp table
    sql = sql_reader.read_sql_from_file(
        srtracker_conf.pg_config['sql'][1],
        srtracker_conf.pg_config['temp_table'],
        srtracker_conf.csv_file_conf['delimiter']
    )

    cur.copy_expert(sql, fd)
    fd.close()
    cur.close()

    sys.stdout.write('- Done [%fs Used]\n' % (time.time() - now))

    return


def main(rownum = None):
    print "Login to source database %s" % srtracker_conf.oracl_config['host']

    # print srtracker_conf.oracl_conn_str()
    oralconn = cx_Oracle.connect(srtracker_conf.oracl_conn_str())
    oralcur = oralconn.cursor()
    oralcur.arraysize = 1000

    oracl_param = 'and rownum <= {0}'.format(rownum) if rownum else ''

    sql = sql_reader.read_sql_from_file(srtracker_conf.oracl_config['sql'], oracl_param)

    now = time.time()
    sys.stdout.write('Fetching data ')
    oralcur.execute(sql)
    sys.stdout.write('- Done [%fs Used]\n' % (time.time() - now))

    duration = time.time()
    print 'Start to sync'
    results = oralcur.fetchmany()
    pgsql_insert_params = []

    now = time.time()
    print 'Dumping source data...'

    totalrows = oralcur.rowcount

    sys.stdout.write('\rDumping progress: %d/%d' % (0, totalrows))
    sys.stdout.flush()

    rowcount = 0

    while len(results) > 0:

        for row in results:
            pgsql_insert_params.append((row[0], row[1], row[2].read(), row[3], row[4], row[5], row[6], row[7]))
            rowcount += 1
            sys.stdout.write('\rDumping progress: %d/%d' % (rowcount, totalrows))
            sys.stdout.flush()

        results = oralcur.fetchmany()

    oralcur.close()
    oralconn.close()

    sys.stdout.write(' - Done [%fs Used]\n' % (time.time() - now))
    print 'Logout from source database %s' % srtracker_conf.oracl_config['host']

    csv_fd = csv_import(pgsql_insert_params)

    print('Login to target database %s' % srtracker_conf.pg_config['host'])

    postgconn = pgconn()
    postgconn.autocommit = True
    postgcur = postgconn.cursor()

    pg_init(postgconn, csv_fd)

    sql = sql_reader.read_sql_from_file(
        srtracker_conf.pg_config['sql'][2],
        srtracker_conf.pg_config['temp_table']
    )

    now = time.time()

    sys.stdout.write('Performing sync data ')
    postgcur.execute(sql)
    sys.stdout.write('- Done[%fs Used]\n' % (time.time() - now))

    postgcur.close()
    postgconn.close()
    print 'Logout from target database %s' % srtracker_conf.pg_config['host']

    print 'Sync finish [%fs Used Total]' % (time.time() - duration)



if __name__ == '__main__':
    main(*sys.argv[1:])
