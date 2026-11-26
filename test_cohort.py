import sqlite3
import unittest

from demo import cohort, load_fixture


class CohortTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        load_fixture(self.db)

    def by_visit(self):
        return {visit: counts for visit, *counts in cohort(self.db)}

    def test_one_row_per_visit_and_order_counts_reconcile(self):
        rows = list(cohort(self.db))
        visits = self.db.execute("SELECT visit_id FROM visits ORDER BY visit_id")
        self.assertEqual([row[0] for row in rows], [visit for visit, in visits])
        for _, orders, given, explicit_not_given, no_record in rows:
            self.assertEqual(orders, given + explicit_not_given + no_record)

    def test_multiple_administration_events_count_as_one_order(self):
        # V01 includes a repeat dose and a missed dose followed by a given dose.
        self.assertEqual(self.by_visit()["V01"], [2, 2, 0, 0])

    def test_absent_record_explicit_nonadministration_and_no_order(self):
        counts = self.by_visit()
        self.assertEqual(counts["V02"], [2, 0, 1, 1])
        self.assertEqual(counts["V04"], [0, 0, 0, 0])

    def test_six_hour_and_discharge_boundaries_are_exclusive(self):
        counts = self.by_visit()
        self.assertEqual(counts["V03"], [1, 0, 0, 1])
        self.assertEqual(counts["V05"], [1, 0, 1, 0])

    def test_prearrival_order_and_event_before_order_are_excluded(self):
        self.db.execute("INSERT INTO orders VALUES ('X', 'V04', -1)")
        self.db.execute("INSERT INTO orders VALUES ('Y', 'V04', 20)")
        self.db.execute("INSERT INTO administrations VALUES ('P', 'X', 10, 'given')")
        self.db.execute("INSERT INTO administrations VALUES ('Q', 'Y', 19, 'given')")
        self.assertEqual(self.by_visit()["V04"], [1, 0, 0, 1])

    def test_arrival_and_same_minute_event_are_included(self):
        self.db.execute("INSERT INTO orders VALUES ('X', 'V04', 0)")
        self.db.execute("INSERT INTO administrations VALUES ('P', 'X', 0, 'given')")
        self.assertEqual(self.by_visit()["V04"], [1, 1, 0, 0])


if __name__ == "__main__":
    unittest.main()
