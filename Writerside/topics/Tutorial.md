# Tutorial

## Initialize

First, you should name and initialize a directory.

```shell
chronovoyage init my-project --vendor mariadb
cd my-project
```

Edit `config.json`.

<code-block lang="json" src="mariadb/config.json"/>

Create migration template directory.

<tabs>
<tab title="DDL">
<code-block lang="shell">
chronovoyage add ddl initial_migration
</code-block>
</tab>
<tab title="DML">
<code-block lang="shell">
chronovoyage add dml initial_migration
</code-block>
</tab>
</tabs>

## Write sql

Write "up" sql to `go.sql`, and "rollback" sql to `return.sql`.

- `initial_migration/go.sql`

<code-block lang="sql" src="mariadb/go.sql"/>

- `initial_migration/return.sql`

<code-block lang="sql" src="mariadb/return.sql"/>

## Migrate

```shell
chronovoyage migrate
```
