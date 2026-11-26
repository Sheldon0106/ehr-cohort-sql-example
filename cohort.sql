-- Count orders placed during the first six hours or before discharge, whichever comes first.
WITH visit_windows AS (
    SELECT visit_id, MIN(duration_min, 360) AS end_min
    FROM visits
),
order_evidence AS (
    SELECT o.visit_id, o.order_id,
           COUNT(a.event_id) AS n_events,
           MAX(CASE WHEN a.status = 'given' THEN 1 ELSE 0 END) AS ever_given
    FROM visit_windows AS w
    JOIN orders AS o
      ON o.visit_id = w.visit_id
     AND o.ordered_min >= 0 AND o.ordered_min < w.end_min
    LEFT JOIN administrations AS a
      ON a.order_id = o.order_id
     AND a.event_min >= o.ordered_min AND a.event_min < w.end_min
    GROUP BY o.visit_id, o.order_id
)
SELECT v.visit_id,
       COUNT(e.order_id) AS orders,
       SUM(CASE WHEN e.ever_given = 1 THEN 1 ELSE 0 END) AS given,
       SUM(CASE WHEN e.n_events > 0 AND e.ever_given = 0 THEN 1 ELSE 0 END) AS explicit_not_given,
       SUM(CASE WHEN e.n_events = 0 THEN 1 ELSE 0 END) AS no_record
FROM visits AS v
LEFT JOIN order_evidence AS e ON e.visit_id = v.visit_id
GROUP BY v.visit_id
ORDER BY v.visit_id;
