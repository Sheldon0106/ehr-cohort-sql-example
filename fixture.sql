-- Invented identifiers and event times. All times are minutes from arrival.
PRAGMA foreign_keys = ON;

CREATE TABLE visits (
    visit_id TEXT PRIMARY KEY,
    duration_min INTEGER NOT NULL CHECK (duration_min > 0)
);
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    visit_id TEXT NOT NULL REFERENCES visits,
    ordered_min INTEGER NOT NULL
);
CREATE TABLE administrations (
    event_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES orders,
    event_min INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('given', 'not_given'))
);

INSERT INTO visits VALUES
    ('V01', 600), ('V02', 200), ('V03', 420), ('V04', 480), ('V05', 100);
INSERT INTO orders VALUES
    ('A10', 'V01', 0), ('A11', 'V01', 80),
    ('A20', 'V02', 10), ('A21', 'V02', 90),
    ('A30', 'V03', 15), ('A31', 'V03', 360),
    ('A50', 'V05', 99), ('A51', 'V05', 100);
INSERT INTO administrations VALUES
    ('E01', 'A10', 0, 'given'),
    ('E02', 'A10', 20, 'given'),
    ('E03', 'A11', 100, 'not_given'),
    ('E04', 'A11', 112, 'given'),
    ('E05', 'A20', 30, 'not_given'),
    ('E06', 'A30', 360, 'given'),
    ('E07', 'A31', 361, 'given'),
    ('E08', 'A50', 99, 'not_given'),
    ('E09', 'A50', 100, 'given');
