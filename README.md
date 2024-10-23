# ChronoVoyage

[![PyPI - Version](https://img.shields.io/pypi/v/chronovoyage.svg)](https://pypi.org/project/chronovoyage)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chronovoyage.svg)](https://pypi.org/project/chronovoyage)

![logo](https://raw.githubusercontent.com/noritakaIzumi/chronovoyage/main/assets/images/logo.jpeg)

-----

## Table of Contents

- [Installation](#Installation)
- [License](#License)

## Installation

To use MariaDB version, you need the MariaDB development package (`libmariadb-dev` in apt).

```shell
pip install chronovoyage[mariadb]
```

## Usage

First, you should name and initialize a directory.

```shell
chronovoyage init my-project --vendor mariadb
cd my-project
```

Edit `config.json`.

```json
{
  "$schema": "https://raw.githubusercontent.com/noritakaIzumi/chronovoyage/main/schema/config.schema.json",
  "vendor": "mariadb",
  "connection_info": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "mariadb",
    "password": "password",
    "database": "test"
  }
}
```

Create migration template directory.

```shell
chronovoyage add ddl initial_migration
```

If you create DML,

```shell
chronovoyage add dml second_migration
```

Write up sql to `go.sql`, and rollback sql to `return.sql`.

Then, migrate.

```shell
chronovoyage migrate
```

## For more information

We have a documentation for more details.

https://chronovoyagemigration.net/

## License

`chronovoyage` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Roadmap

- Support for Python
    - [x] 3.8
    - [x] 3.9 or later
- Database support
    - [ ] MySQL
    - [x] MariaDB
    - [ ] PostgreSQL
- Migration file support
    - [x] SQL (.sql)
    - [ ] Shell script (.sh)
- Commands
    - ~~new~~ init
        - [x] create migration directory and config file
    - ~~generate~~ add
        - [x] create migration files from template
    - migrate
        - [x] to latest
        - [x] to specific version
        - [x] from the beginning
        - [x] from the middle
        - --dry-run
            - [ ] show executing SQL
        - [ ] detect ddl or dml
    - ~~status~~ current
        - [x] show current migration status
    - rollback
        - [x] to version
    - test
        - [ ] check if every "migrate -> rollback" operation means do nothing for schema
        - [ ] if dml, the operation means do nothing for data (including autoincrement num)
- Other
    - [x] CLI logging
    - [x] Documentation
