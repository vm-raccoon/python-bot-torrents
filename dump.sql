CREATE TABLE exception (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT,
    trash INTEGER
);

CREATE TABLE items (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT,
    url      TEXT,
    selector TEXT,
    value    TEXT,
    trash    INTEGER
);

