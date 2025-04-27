DROP TABLE IF EXISTS postgres.pgml.student_activity;

CREATE TABLE postgres.pgml.student_activity (
    idstudent BIGINT DEFAULT 0,
    assign_clicks INT DEFAULT 0,
    quiz_clicks INT DEFAULT 0,
    forum_clicks INT DEFAULT 0,
    resource_clicks INT DEFAULT 0,
    url_clicks INT DEFAULT 0,
    book_clicks INT DEFAULT 0,
    chat_clicks INT DEFAULT 0,
    choice_clicks INT DEFAULT 0,
    data_clicks INT DEFAULT 0,
    feedback_clicks INT DEFAULT 0,
    glossary_clicks INT DEFAULT 0,
    lesson_clicks INT DEFAULT 0,
    scorm_clicks INT DEFAULT 0,
    survey_clicks INT DEFAULT 0,
    wiki_clicks INT DEFAULT 0,
    workshop_clicks INT DEFAULT 0,
    final_grade DECIMAL(5,2) DEFAULT 0.00,
    final_grade_binary BOOLEAN DEFAULT FALSE
);

COPY postgres.pgml.student_activity
FROM '/tmp/student_activity.csv'
DELIMITER ','
CSV HEADER;


SELECT * FROM postgres.pgml.student_activity;


--- view in care datele sunt normalizate si nu exista student care sa aiba nota finala 0
DROP VIEW IF EXISTS postgres.pgml.student_activity_normalized;
CREATE VIEW postgres.pgml.student_activity_normalized AS
SELECT
    (assign_clicks - avg_assign) / NULLIF(stddev_assign, 0) AS assign_clicks_norm,
    (quiz_clicks - avg_quiz) / NULLIF(stddev_quiz, 0) AS quiz_clicks_norm,
    (forum_clicks - avg_forum) / NULLIF(stddev_forum, 0) AS forum_clicks_norm,
    (resource_clicks - avg_resource) / NULLIF(stddev_resource, 0) AS resource_clicks_norm,
    (url_clicks - avg_url) / NULLIF(stddev_url, 0) AS url_clicks_norm,
    final_grade_binary
FROM postgres.pgml.student_activity,
(
    SELECT
        AVG(assign_clicks) AS avg_assign, STDDEV(assign_clicks) AS stddev_assign,
        AVG(quiz_clicks) AS avg_quiz, STDDEV(quiz_clicks) AS stddev_quiz,
        AVG(forum_clicks) AS avg_forum, STDDEV(forum_clicks) AS stddev_forum,
        AVG(resource_clicks) AS avg_resource, STDDEV(resource_clicks) AS stddev_resource,
        AVG(url_clicks) AS avg_url, STDDEV(url_clicks) AS stddev_url
    FROM postgres.pgml.student_activity
) AS stats_values;



/*
SELECT assign_clicks, quiz_clicks, forum_clicks, resource_clicks, url_clicks, feedback_clicks, lesson_clicks, final_grade_binary
FROM postgres.pgml.student_activity
WHERE final_grade !=0;
*/

SELECT * FROM postgres.pgml.student_activity_normalized;


SHOW search_path;
SET search_path TO pgml;

/*
---antrenare alg
SELECT * FROM pgml.train(
    project_name => 'STUDENT_FINAL_GRADE_PREDICTION_RANDOM_FOREST_NORMALIZED'::text,
    task => 'classification'::text,
    relation_name => 'pgml.student_activity_normalized'::text,
    y_column_name => 'final_grade_binary'::text,
    algorithm => 'random_forest'::algorithm
);

-- (dacă extensia suportă 'mlp' - Multi-layer Perceptron)
SELECT * FROM pgml.train(
    project_name => 'STUDENT_FINAL_GRADE_PREDICTION_PERCEPTRON_L2'::text,
    task => 'classification'::text,
    relation_name => 'pgml.student_activity_normalized'::text,
    y_column_name => 'final_grade_binary'::text,
    algorithm => 'linear'::algorithm,
    hyperparams => '{
        "penalty": "l2",
        "fit_intercept": true,
        "max_iter": 1000
    }'::jsonb
);
*/


SELECT * FROM pgml.train(
    project_name => 'student_grade_perceptron',
    task => 'classification',
    relation_name => 'pgml.student_activity_normalized',
    y_column_name => 'final_grade_binary',
    algorithm => 'perceptron',
    hyperparams => '{
        "penalty": "l2",
        "alpha": 0.0001,
        "max_iter": 1000
    }'::jsonb
);

SELECT unnest(enum_range(NULL::pgml.algorithm)) AS available_algorithms;

/*
SELECT final_grade_binary,
       pgml.predict('STUDENT_FINAL_GRADE_PREDICTION_RANDOM_FOREST_NORMALIZED',
           ARRAY[assign_clicks, quiz_clicks, forum_clicks, resource_clicks, url_clicks, feedback_clicks, lesson_clicks]
       ) AS predicted_score,
       CAST(final_grade_binary AS INTEGER) - pgml.predict('STUDENT_FINAL_GRADE_PREDICTION_RANDOM_FOREST_NORMALIZED',
           ARRAY[assign_clicks, quiz_clicks, forum_clicks, resource_clicks, url_clicks, feedback_clicks, lesson_clicks]
       ) AS error
FROM pgml.student_activity_no_nulls;
*/


---predictie alg
SELECT final_grade_binary,
       pgml.predict('student_grade_perceptron',
           ARRAY[
               assign_clicks_norm::DOUBLE PRECISION,
               quiz_clicks_norm::DOUBLE PRECISION,
               forum_clicks_norm::DOUBLE PRECISION,
               resource_clicks_norm::DOUBLE PRECISION,
               url_clicks_norm::DOUBLE PRECISION
           ]::DOUBLE PRECISION[]
       ) AS predicted_score,
       CAST(final_grade_binary AS INTEGER) - pgml.predict('student_grade_perceptron',
           ARRAY[
               assign_clicks_norm::DOUBLE PRECISION,
               quiz_clicks_norm::DOUBLE PRECISION,
               forum_clicks_norm::DOUBLE PRECISION,
               resource_clicks_norm::DOUBLE PRECISION,
               url_clicks_norm::DOUBLE PRECISION
           ]::DOUBLE PRECISION[]
       ) AS error
FROM pgml.student_activity_normalized;


SELECT id, algorithm,
       metrics->>'accuracy' AS accuracy,
       metrics->>'precision' AS precision,
       metrics->>'recall' AS recall,
       -- F1-score
       2 * (
           (metrics->>'precision')::numeric * (metrics->>'recall')::numeric
       ) / NULLIF(
           (metrics->>'precision')::numeric + (metrics->>'recall')::numeric, 0
       ) AS f1_score
FROM pgml.models
WHERE id = 18;
