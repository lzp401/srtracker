__author__ = 'victorlu'

import cx_Oracle
import psycopg2
import csv
import time
import datetime
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

def oraclconn():
    return cx_Oracle.connect(srtracker_conf.oracl_conn_str())


def csv_import(data):
    now = time.time()

    sys.stdout.write('Importing data to CSV')

    csvfile = os.tmpfile()
    writer = csv.writer(csvfile, delimiter=srtracker_conf.csv_file_conf['delimiter'])
    writer.writerows(data)
    csvfile.flush()
    csvfile.seek(0)
    sys.stdout.write(' - Done [%fs Used]\n' % (time.time() - now))

    return csvfile


def pg_init(conn, fd):
    cur = conn.cursor()
    now = time.time()

    sys.stdout.write('Import CSV data to temp table ')

    # Create temp table to import CSV file to
    sql = sql_reader.read_sql_from_file(
        srtracker_conf.pg_config['sql'][1],
        srtracker_conf.pg_config['temp_table'],
    )
    cur.execute(sql)

    # Import CSV file into temp table
    sql = sql_reader.read_sql_from_file(
        srtracker_conf.pg_config['sql'][2],
        srtracker_conf.pg_config['temp_table'],
        srtracker_conf.csv_file_conf['delimiter']
    )

    cur.copy_expert(sql, fd)
    fd.close()
    cur.close()

    sys.stdout.write('- Done [%fs Used]\n' % (time.time() - now))

    return


def fetch_source(conn, firstboot=False, rownum=None):
    cur = conn.cursor()

    # if it is first boot, fetch all matched data from source database, else, fetch the last day's data
    if not firstboot:
        date_str = datetime.date.strftime(datetime.date.today(), '%d-%m-%Y %H:%M:%S')
        date_str = ' and CREATEDDATE >= TO_DATE(\'{0}\', \'dd-mm-yyyy HH24:MI:SS\') '.format(date_str)
    else:
        date_str = ''

    rownum_srt = 'and rownum <= {0}'.format(rownum) if rownum else ''
    sql = sql_reader.read_sql_from_file(srtracker_conf.oracl_config['sql'], date_str, rownum_srt)

    now = time.time()
    sys.stdout.write('Fetching data ')
    cur.execute(sql)
    sys.stdout.write('- Done [%fs Used]\n' % (time.time() - now))

    return cur


def dump_data(cur):
    now = time.time()
    print 'Dumping source data...'

    sys.stdout.write('\rDumping progress: %d/%d' % (0, totalrows))
    sys.stdout.flush()

    results = cur.fetchmany()
    rowcount = 0
    params = []

    while len(results) > 0:

        for row in results:
            params.append((row[0], row[1], row[2].read(), row[3], row[4], row[5], row[6]))
            rowcount += 1
            sys.stdout.write('\rDumping progress: %d' % rowcount)
            sys.stdout.flush()

        results = cur.fetchmany()

    cur.close()

    return params


def apply_data(conn, fd):
    pg_init(conn, fd)

    sql = sql_reader.read_sql_from_file(
        srtracker_conf.pg_config['sql'][3],
        srtracker_conf.pg_config['temp_table']
    )

    now = time.time()

    sys.stdout.write('Performing sync data ')
    conn.cursor().execute(sql)
    sys.stdout.write('- Done[%fs Used]\n' % (time.time() - now))


def check_firstboot(conn):
    cur = conn.cursor()

    sql = sql_reader.read_sql_from_file(srtracker_conf.pg_config['sql'][0])
    cur.execute(sql)

    is_firstboot = cur.rowcount == 0
    cur.close()

    print('First boot status: %s' % is_firstboot)

    return is_firstboot



def main(rownum = None):
    print "Login to source database %s" % srtracker_conf.oracl_config['host']

    # print srtracker_conf.oracl_conn_str()
    oracl_conn = oraclconn()
    postgconn = pgconn()
    postgconn.autocommit = True

    is_firstboot = check_firstboot(postgconn)


    duration = time.time()
    print 'Start to sync'
    cur = fetch_source(oracl_conn, is_firstboot, rownum)

    params = dump_data(cur)
    oracl_conn.close()
    print 'Logout from source database %s' % srtracker_conf.oracl_config['host']

    csv_fd = csv_import(params)

    print('Login to target database %s' % srtracker_conf.pg_config['host'])
    apply_data(postgconn, csv_fd)

    postgconn.close()
    print 'Logout from target database %s' % srtracker_conf.pg_config['host']

    print 'Sync finish [%fs Used Total]' % (time.time() - duration)



if __name__ == '__main__':
    main(*sys.argv[1:])
