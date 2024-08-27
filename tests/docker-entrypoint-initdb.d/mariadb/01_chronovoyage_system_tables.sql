CREATE TABLE test.chronovoyage_periods
(
    `id`          INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `period_name` VARCHAR(14)   NOT NULL UNIQUE COMMENT 'バージョン名 (%Y%m%d%H%M%S)',
    `language`    VARCHAR(3)    NOT NULL COMMENT '言語種別 (ddl/dml)',
    `description` VARCHAR(4096) NOT NULL COMMENT '説明',
    `created_at`  DATETIME      NOT NULL DEFAULT NOW()
) COMMENT 'マイグレーションバージョン管理';
