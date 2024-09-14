# noinspection SqlResolveForFile

@id = 3;

DELETE
FROM user
WHERE id >= @id;

ALTER TABLE table_name
    AUTO_INCREMENT = @id;
