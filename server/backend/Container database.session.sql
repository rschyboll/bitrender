SELECT COUNT(
        CASE
            WHEN "subtask"."finished" = false THEN "subtask"."id"
            ELSE NULL
        END
    ) "not_running"
FROM subtask
GROUP BY "subtask"."frame_id"
HAVING COUNT(
        CASE
            WHEN "subtask"."finished" = false THEN "subtask"."id"
            ELSE NULL
        END
    ) = 0