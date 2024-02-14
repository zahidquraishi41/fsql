import os
from pathlib import Path
import sqlite3
import time
import stat
import extensions


def create_filesystem_table(con, table_name):
    cur = con.cursor()
    create_table_query = f'''CREATE TABLE {table_name} (
        ino INTEGER,
        dev INTEGER,
        nlink INTEGER,
        uid INTEGER,
        gid INTEGER,
        size INTEGER,
        atime REAL,
        mtime REAL,
        ctime REAL,
        atime_ns INTEGER,
        mtime_ns INTEGER,
        ctime_ns INTEGER,
        dirname TEXT,
        filename TEXT,
        extension TEXT,
        filetype TEXT
    );'''
    cur.execute(create_table_query)


def insert_file_data(cur, table_name, stats, file_path):
    insert_query = f'''INSERT INTO {table_name} VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    path = Path(file_path)
    cur.execute(
        insert_query,
        (stats.st_ino, stats.st_dev, stats.st_nlink, stats.st_uid, stats.st_gid, stats.st_size, stats.st_atime,
         stats.st_mtime, stats.st_ctime, stats.st_atime_ns, stats.st_mtime_ns, stats.st_ctime_ns,
         str(path.parent), path.stem, path.suffix, extensions.get_file_type(path.suffix))
    )


def populate_filesystem_table(con, table_name, target_dir):
    cur = con.cursor()
    paths = os.listdir(target_dir)
    for path in paths:
        full_path = os.path.join(target_dir, path)
        stats = os.stat(full_path)
        insert_file_data(cur, table_name, stats, full_path)


def populate_filesystem_table_recursive(con, table_name, target_dir):
    cur = con.cursor()

    rem_dirs = [target_dir]
    while rem_dirs:
        curr_dir = rem_dirs.pop(0)
        paths = os.listdir(curr_dir)
        for path in paths:
            full_path = os.path.join(curr_dir, path)
            stats = os.stat(full_path)
            insert_file_data(cur, table_name, stats, full_path)
            if stat.S_ISDIR(stats.st_mode):
                rem_dirs.append(full_path)


def validate_select_query(query: str):
    if not query.lower().startswith('select'):
        raise ValueError('Query must start with SELECT keyword.')

    if 'from' not in query.lower():
        raise ValueError(f'FROM keyword is missing.')


def query_split(s: str):
    l = []
    word = ''
    in_quote = False
    for ch in s:
        if ch == '"':
            in_quote = not in_quote

        if ch == ' ' and in_quote:
            word += ch

        elif ch == ' ':
            l.append(word)
            word = ''

        else:
            word += ch
    l.append(word)
    return l


def extract_query_info(query: str):
    words = query_split(query)
    target_dir = words[words.index('from') + 1]
    if target_dir.startswith('"'):
        target_dir = target_dir[1:-1]

    table_name = 'table_' + str(int(time.time()))
    words[words.index('from') + 1] = table_name

    recursive = False
    if words[-1] == 'recursive':
        recursive = True
        words.pop()

    return target_dir, table_name, recursive, ' '.join(words)


def display_help():
    print("Filesystem SQL Help")
    print("=============================")
    print("Commands:")
    print(
        "  - SELECT <columns> FROM <directory_path> [WHERE <condition>] [GROUP BY <column>] [HAVING <condition>]")
    print("      Fetches details of files in the specified directory with optional conditions.")
    print("      Example: SELECT ino, filename FROM /home/user/documents/ WHERE size > 1024 GROUP BY extension HAVING COUNT(*) > 1")
    print()
    print("  - Columns that can be searched or used in conditions: ino, dev, nlink, uid, gid, size, atime, mtime, ctime,")
    print("    atime_ns, mtime_ns, ctime_ns, dirname, filename, extension, filetype.")
    print("  - Add 'recurisve' at the end of query to enable recursive search.")
    print("  - Directory name with spaces must be quotted.")
    print()


def perform_query(user_query):
    connection = sqlite3.connect(':memory:')
    target_directory, table_name, \
        recursive, query = extract_query_info(user_query)
    if not os.path.exists(target_directory):
        raise FileNotFoundError(f'{target_directory} doesn\'t exists.')
    if not os.path.isdir(target_directory):
        raise NotADirectoryError(f'{target_directory} is not a directory.')

    create_filesystem_table(connection, table_name)
    validate_select_query(user_query)
    if recursive:
        populate_filesystem_table_recursive(
            connection, table_name, target_directory
        )
    else:
        populate_filesystem_table(connection, table_name, target_directory)
    result = connection.cursor().execute(query).fetchall()
    connection.close()
    return result


def main():
    while True:
        user_input = input('Enter query: ')
        if user_input == 'exit':
            break
        elif user_input == 'help':
            display_help()
        else:
            try:
                result = perform_query(user_input)
                for e in result:
                    print(e)
            except Exception as e:
                print(e)
        print()


if __name__ == "__main__":
    main()
