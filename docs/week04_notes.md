# CourseHub - Buoi 4

- Migration 001: enrollment_events.
- Demo class: RACE-01, capacity = 1.
- POST /enrollments: lock class_sections bang FOR UPDATE.
- Concurrency test: 1 request 201, 1 request 409.
- Performance data: 100000 rows, dataset=performance.
- Index: idx_enrollment_events_dataset_student_time.
- Scan type truoc index: Seq Scan, Execution Time: 9.271 ms, Buffers: 1137 blocks.
- Scan type sau index: Index Scan, Execution Time: 0.111 ms, Buffers: 53 blocks (nhanh hon ~83.5 lan).

Khong commit backend/.env.

---

## Chi tiet do hieu nang va toi uu chi muc

### 1. Truy van kiem thu
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, student_id, class_section_id, event_type, occurred_at
FROM enrollment_events
WHERE dataset = 'performance'
  AND student_id = '22000001'
  AND occurred_at >= TIMESTAMP '2025-12-20 00:00:00'
ORDER BY occurred_at DESC
LIMIT 50;
```

### 2. Kế hoạch trước khi tạo Index
```text
Limit  (cost=2914.51..2914.63 rows=50 width=39) (actual time=9.231..9.241 rows=50.00 loops=1)
  Buffers: shared hit=1137
  ->  Sort  (cost=2914.51..2916.58 rows=828 width=39) (actual time=9.230..9.233 rows=50.00 loops=1)
        Sort Key: occurred_at DESC
        Sort Method: top-N heapsort  Memory: 31kB
        Buffers: shared hit=1137
        ->  Seq Scan on enrollment_events  (cost=0.00..2887.00 rows=828 width=39) (actual time=0.053..9.045 rows=820.00 loops=1)
              Filter: ((occurred_at >= '2025-12-20 00:00:00'::timestamp without time zone) AND ((dataset)::text = 'performance'::text) AND ((student_id)::text = '22000001'::text))
              Rows Removed by Filter: 99180
              Buffers: shared hit=1137
Planning Time: 0.202 ms
Execution Time: 9.271 ms
```

### 3. Kế hoạch sau khi tạo Composite Index
```text
Limit  (cost=0.42..68.00 rows=50 width=39) (actual time=0.048..0.089 rows=50.00 loops=1)
  Buffers: shared hit=53
  ->  Index Scan using idx_enrollment_events_dataset_student_time on enrollment_events  (cost=0.42..1081.73 rows=800 width=39) (actual time=0.047..0.080 rows=50.00 loops=1)
        Index Cond: (((dataset)::text = 'performance'::text) AND ((student_id)::text = '22000001'::text) AND (occurred_at >= '2025-12-20 00:00:00'::timestamp without time zone))
        Index Searches: 1
        Buffers: shared hit=53
Planning Time: 0.146 ms
Execution Time: 0.111 ms
```

### 4. Bang so sanh tong hop
| Chi so quan sat | Truoc index | Sau index | Cai thien |
| :--- | :--- | :--- | :--- |
| **Scan Type** | `Seq Scan` (Quet toan bang) | `Index Scan` | Truc tiep vao vung can doc |
| **Sort Method** | `top-N heapsort (31kB)` | **Khong can Sort** | Tiet kiem RAM/CPU |
| **Rows Removed** | `99,180` dong | **0** dong | Loc chinh xac |
| **Buffers** | `1,137` blocks | `53` blocks | Giam **~95.3%** I/O |
| **Execution Time** | `9.271 ms` | `0.111 ms` | Nhanh hon **~83.5 lan** |
