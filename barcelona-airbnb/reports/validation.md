# Barcelona Airbnb – Data Contract Validation

_Generated: 2026-09-14 21:08:08_

## Summary

- **Total checks:** 12
- **Passed:** 10
- **Failed:** 2

## Details

| check                       | passed   | message                     |   failing_rows |
|:----------------------------|:---------|:----------------------------|---------------:|
| min_rows[1000]              | True     | 19,833 rows                 |              0 |
| no_nulls[id]                | True     | no nulls                    |              0 |
| unique[id]                  | True     | all unique                  |              0 |
| no_nulls[host_id]           | True     | no nulls                    |              0 |
| range[latitude]             | True     | all within [41.0, 41.6]     |              0 |
| range[longitude]            | True     | all within [1.9, 2.3]       |              0 |
| range[price]                | True     | all within [0, 10000]       |              0 |
| range[accommodates]         | True     | all within [1, 30]          |              0 |
| range[minimum_nights]       | False    | 1 values outside [1, 365]   |              1 |
| allowed_values[room_type]   | True     | all allowed                 |              0 |
| range[host_response_rate]   | True     | all within [0, 100]         |              0 |
| range[review_scores_rating] | False    | 14986 values outside [0, 5] |          14986 |
