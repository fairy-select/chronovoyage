# ChronoVoyage

[![PyPI - Version](https://img.shields.io/pypi/v/chronovoyage.svg)](https://pypi.org/project/chronovoyage)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chronovoyage.svg)](https://pypi.org/project/chronovoyage)

![logo](assets/images/logo.jpeg)

-----

## Motivation

I'm trying to write my own database migration framework and discuss database management ideals.

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install chronovoyage
```

## Required dependencies

To use MariaDB, you need the MariaDB development package.

Install via apt:

```shell
sudo apt install libmariadb-dev
```

## License

`chronovoyage` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Roadmap

- Support for Python
    - [x] 3.8
    - [ ] 3.9 or later
- Database support
    - [ ] MySQL
    - [x] MariaDB
    - [ ] PostgreSQL
- Migration file support
    - [x] SQL (.sql)
    - [ ] Shell script (.sh)
- Commands
    - new
        - [ ] create migration directory and config file
    - generate
        - [ ] create migration files from template
    - migrate
        - [x] to latest
        - [ ] to specific version
        - [x] from the beginning
        - [ ] from the middle
        - --dry-run
            - [ ] show executing SQL
        - [ ] detect ddl or dml
    - status
        - [ ] show current migration status
    - rollback
        - [ ] to version
    - test
        - [ ] check if every "migrate -> rollback" operation means do nothing for schema
        - [ ] if dml, the operation means do nothing for data (including autoincrement num)
