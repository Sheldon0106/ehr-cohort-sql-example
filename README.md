# Building a visit-level cohort in SQL

How many medication orders placed in the first six hours of a visit have a documented administration in that window? One order can have several administration records. A visit can also have an order with no follow-up record, or no order at all. Counting rows after joining the three tables would confuse these cases.

This small SQLite example uses five invented visits. All identifiers, event times and statuses were written for the example. Run it from the repository root with Python 3 and its standard library:

```sh
python demo.py
```

```text
visit_id  orders  given  explicit_not_given  no_record
V01       2       2      0                   0
V02       2       0      1                   1
V03       1       0      0                   1
V04       0       0      0                   0
V05       1       0      1                   0
```

## Read the result

The three rightmost columns count **orders**. In V01, one order has two recorded doses. The other has an explicit `not_given` event followed by a `given` event. Both orders were administered at least once.

V02 has one order with an explicit `not_given` event and one with no qualifying event. The latter stays in `no_record` because the available records leave its administration status unknown. V04 has no eligible order and still appears in the cohort.

## Query and checks

[`fixture.sql`](fixture.sql) defines the tables and inserts the example rows. Times are minutes from arrival. [`cohort.sql`](cohort.sql) includes orders from minute zero up to the earlier of minute 360 or discharge, excluding the endpoint. An administration counts from its order time through that same window, again excluding the endpoint. The query groups events by order first, then joins the order summaries back to all visits. That preserves one row per visit and lets the three status counts add up to the eligible order count.

Run `python -m unittest discover -v` for the [regression tests](test_cohort.py). They cover repeat doses, missing records, visits without orders and events on both sides of the time boundaries.
