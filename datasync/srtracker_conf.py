__author__ = 'victorlu'

import os


sql_file_path = os.path.dirname(os.path.realpath(__file__)) + '/sqls/%s'

pg_config = {
    'temp_table': 'source_data',
    'sql': (
        sql_file_path % 'pg_is_firstboot.sql',
        sql_file_path % 'pg_init.sql',
        sql_file_path % 'pg_copy_data.sql',
        sql_file_path % 'pg_apply_source.sql'
    )
}

oracl_config = {
    'sql': sql_file_path % 'oracl_query_source.sql',
}

csv_file_conf = {
    'delimiter': '|',
}


def oracl_conn_str():
    return '%s/%s@%s:%d/%s' % (
        oracl_config['user'],
        oracl_config['password'],
        oracl_config['host'],
        oracl_config['port'],
        oracl_config['sid']
    )
