# Barcelona Airbnb – Processed Data Quality (After Cleaning)

_Generated: 2026-09-14 21:16:00_

## Overview

- **Total rows:** 19,833
- **Total columns:** 22
- **Exact duplicate rows:** 0

## Missing Values (Top 20)

| column                    |   missing_count |   missing_pct |
|:--------------------------|----------------:|--------------:|
| review_scores_location    |            4858 |         24.49 |
| review_scores_cleanliness |            4855 |         24.48 |
| review_scores_rating      |            4847 |         24.44 |
| host_response_rate        |            2518 |         12.7  |
| host_is_superhost         |              34 |          0.17 |
| beds                      |              34 |          0.17 |
| name                      |              17 |          0.09 |
| bedrooms                  |               3 |          0.02 |
| longitude                 |               0 |          0    |
| host_id                   |               0 |          0    |
| id                        |               0 |          0    |
| latitude                  |               0 |          0    |
| neighbourhood_cleansed    |               0 |          0    |
| accommodates              |               0 |          0    |
| availability_365          |               0 |          0    |
| maximum_nights            |               0 |          0    |
| minimum_nights            |               0 |          0    |
| price                     |               0 |          0    |
| room_type                 |               0 |          0    |
| number_of_reviews         |               0 |          0    |

## Column Types

| dtype   |   column_count | columns                                                                                                                                 |
|:--------|---------------:|:----------------------------------------------------------------------------------------------------------------------------------------|
| Float64 |              1 | price_per_person                                                                                                                        |
| Int64   |              7 | id, host_id, accommodates, minimum_nights, maximum_nights, availability_365, number_of_reviews                                          |
| boolean |              1 | is_entire_home                                                                                                                          |
| float64 |              9 | latitude, longitude, bedrooms, beds, price, host_response_rate, review_scores_rating, review_scores_cleanliness, review_scores_location |
| string  |              4 | name, neighbourhood_cleansed, room_type, host_is_superhost                                                                              |

## High-Cardinality Columns (>100 unique values)

| column            |   unique_count | sample_value            |
|:------------------|---------------:|:------------------------|
| id                |          19833 | 18666                   |
| name              |          19206 | Flat with Sunny Terrace |
| host_id           |           9743 | 71615                   |
| longitude         |           6871 | 2.18555                 |
| latitude          |           5566 | 41.40889                |
| price_per_person  |           1063 | 21.666666666666668      |
| price             |            462 | 130.0                   |
| number_of_reviews |            391 | 1                       |
| availability_365  |            366 | 182                     |
| maximum_nights    |            241 | 730                     |

## Numeric Column Statistics

|                           |   count |             mean |           std |         min |          25% |            50% |            75% |            max |
|:--------------------------|--------:|-----------------:|--------------:|------------:|-------------:|---------------:|---------------:|---------------:|
| id                        |   19833 |      2.09588e+07 |   1.14097e+07 | 18666       |  1.17668e+07 |    2.23758e+07 |    3.15605e+07 |    3.65828e+07 |
| host_id                   |   19833 |      8.64599e+07 |   8.92364e+07 |  3073       |  7.60227e+06 |    4.35655e+07 |    1.60691e+08 |    2.74863e+08 |
| latitude                  |   19833 |     41.3921      |   0.0149338   |    41.3495  | 41.3803      |   41.389       |   41.4022      |   41.464       |
| longitude                 |   19833 |      2.16758     |   0.0180543   |     2.08838 |  2.15698     |    2.16818     |    2.17806     |    2.22941     |
| accommodates              |   19833 |      3.3475      |   2.19629     |     1       |  2           |    2           |    4           |   18           |
| bedrooms                  |   19830 |      1.56757     |   1.01482     |     0       |  1           |    1           |    2           |   16           |
| beds                      |   19799 |      2.25769     |   1.88152     |     0       |  1           |    2           |    3           |   40           |
| price                     |   19833 |    129.625       | 423.999       |     7       | 40           |   65           |  113           | 9120           |
| minimum_nights            |   19833 |      8.5213      |  17.9645      |     1       |  1           |    2           |    4           |  900           |
| maximum_nights            |   19833 | 217270           |   2.15645e+07 |     1       | 60           | 1125           | 1125           |    2.14748e+09 |
| availability_365          |   19833 |    170.54        | 126.603       |     0       | 49           |  160           |  296           |  365           |
| number_of_reviews         |   19833 |     32.818       |  58.3184      |     0       |  1           |    7           |   38           |  645           |
| host_response_rate        |   17315 |     93.5651      |  15.2175      |     0       | 95           |  100           |  100           |  100           |
| review_scores_rating      |   14986 |     91.0969      |   9.61953     |    20       | 88           |   93           |   97           |  100           |
| review_scores_cleanliness |   14978 |      9.25671     |   1.04073     |     2       |  9           |   10           |   10           |   10           |
| review_scores_location    |   14975 |      9.58958     |   0.765803    |     2       |  9           |   10           |   10           |   10           |
| price_per_person          |   19833 |     43.3334      | 208.694       |     0.5625  | 17.5         |   24.875       |   34.5         | 6000           |
