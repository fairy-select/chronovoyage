# ChronoVoyage

[![PyPI - Version](https://img.shields.io/pypi/v/chronovoyage.svg)](https://pypi.org/project/chronovoyage)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chronovoyage.svg)](https://pypi.org/project/chronovoyage)

-----

Documentation is [here](https://chronovoyagemigration.net/).

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
