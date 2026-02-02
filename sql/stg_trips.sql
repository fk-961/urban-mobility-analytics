-- Staging table for NYC Taxi Trips
-- Purpose:
--   - Enforce types
--   - Add data quality flags
--   - Prepare clean inputs for analytics

DROP TABLE IF EXISTS stg_trips;

CREATE TABLE stg_trips AS
WITH base AS (
    SELECT
        pulocationid,
        dolocationid,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        fare_amount,
        tip_amount,
        total_amount,

        -- Derived metrics
        EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60
            AS trip_duration_minutes,

        -- Time consistency checks
        CASE
            WHEN tpep_pickup_datetime > tpep_dropoff_datetime THEN TRUE
            ELSE FALSE
        END AS is_time_inconsistent,

        -- Financial adjustment detection
        CASE
            WHEN fare_amount < 0
              OR tip_amount < 0
              OR total_amount < 0
            THEN TRUE
            ELSE FALSE
        END AS is_refund_or_adjustment,

        -- Duplicate detection (exact duplicates)
        ROW_NUMBER() OVER (
            PARTITION BY
                tpep_pickup_datetime,
                tpep_dropoff_datetime,
                pulocationid,
                dolocationid,
                passenger_count,
                trip_distance,
                fare_amount,
                tip_amount,
                total_amount
            ORDER BY tpep_pickup_datetime
        ) AS exact_row_number

    FROM raw_trips
)

SELECT
    *,
    exact_row_number > 1 AS is_exact_duplicate
FROM base;
