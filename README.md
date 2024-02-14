# Filesystem SQL App

The Filesystem SQL App transforms your filesystem into a relational database, allowing you to interact with it using SQL-like queries. Retrieve details about files, apply conditions, and search for specific files.

## Features

- **SQL-Like Queries:** Use `SELECT` queries to fetch details, apply conditions, and perform advanced operations on your filesystem.

### Installation
```bash
git clone https://github.com/zahidquraishi/fsql.git
cd fsql
python3 fsql.py
```

### Example Queries

- Fetch details of files in a directory:
  ```sql
  SELECT * FROM /path/to/directory
  ```

- Search for specific files with conditions:
  ```sql
  SELECT * FROM /path/to/directory WHERE filename like 'e%'
  ```

- Fetch details of image files in a directory:
  ```sql
  SELECT * FROM /path/to/directory WHERE filetype == 'image'
  ```

- Count and group files by extension in a directory:
  ```sql
  SELECT extension, count(extension) from /path/to/directory group by extension
  ```

## Contributing

We welcome contributions! If you have ideas for improvements, open an issue or submit a pull request.
