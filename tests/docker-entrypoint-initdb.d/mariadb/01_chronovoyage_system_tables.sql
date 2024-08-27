CREATE TABLE test.chronovoyage_periods
(
    `id`          INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `period_name` VARCHAR(14)   NOT NULL UNIQUE COMMENT 'バージョン名 (%Y%m%d%H%M%S)',
    `language`    VARCHAR(3)    NOT NULL COMMENT '言語種別 (ddl/dml)',
    `description` VARCHAR(4096) NOT NULL COMMENT '説明',
    `has_come`    BOOLEAN       NOT NULL DEFAULT FALSE COMMENT 'TRUE: 反映済みである, FALSE: 未反映・ロールバック済みである',
    `is_verified` BOOLEAN       NOT NULL DEFAULT FALSE COMMENT 'go.sql と return.sql のデータ整合性が検証済みである'
) COMMENT 'マイグレーションバージョン管理';
