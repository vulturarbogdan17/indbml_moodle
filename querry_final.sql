DROP TABLE IF EXISTS moodle.public.student_activity;

SELECT * FROM moodle.public.student_activity;

CREATE TABLE moodle.public.student_activity AS
SELECT
    u.id AS idstudent,
    SUM(CASE WHEN m.name = 'assign' THEN 1 ELSE 0 END) AS assign_clicks,
    SUM(CASE WHEN m.name = 'quiz' THEN 1 ELSE 0 END) AS quiz_clicks,
    SUM(CASE WHEN m.name = 'forum' THEN 1 ELSE 0 END) AS forum_clicks,
    SUM(CASE WHEN m.name = 'resource' THEN 1 ELSE 0 END) AS resource_clicks,
    SUM(CASE WHEN m.name = 'url' THEN 1 ELSE 0 END) AS url_clicks,
    SUM(CASE WHEN m.name = 'book' THEN 1 ELSE 0 END) AS book_clicks,
    SUM(CASE WHEN m.name = 'chat' THEN 1 ELSE 0 END) AS chat_clicks,
    SUM(CASE WHEN m.name = 'choice' THEN 1 ELSE 0 END) AS choice_clicks,
    SUM(CASE WHEN m.name = 'data' THEN 1 ELSE 0 END) AS data_clicks,
    SUM(CASE WHEN m.name = 'feedback' THEN 1 ELSE 0 END) AS feedback_clicks,
    SUM(CASE WHEN m.name = 'glossary' THEN 1 ELSE 0 END) AS glossary_clicks,
    SUM(CASE WHEN m.name = 'lesson' THEN 1 ELSE 0 END) AS lesson_clicks,
    SUM(CASE WHEN m.name = 'scorm' THEN 1 ELSE 0 END) AS scorm_clicks,
    SUM(CASE WHEN m.name = 'survey' THEN 1 ELSE 0 END) AS survey_clicks,
    SUM(CASE WHEN m.name = 'wiki' THEN 1 ELSE 0 END) AS wiki_clicks,
    SUM(CASE WHEN m.name = 'workshop' THEN 1 ELSE 0 END) AS workshop_clicks,
    COALESCE(gg.finalgrade, 0) AS final_grade,
    CASE WHEN COALESCE(gg.finalgrade, 0) >= 5 THEN 1 ELSE 0 END AS final_grade_binary
FROM mdl_logstore_standard_log l
JOIN mdl_user u ON l.userid = u.id
JOIN mdl_course_modules cm ON l.contextinstanceid = cm.id
JOIN mdl_modules m ON cm.module = m.id
LEFT JOIN mdl_grade_items gi ON gi.courseid = l.courseid AND gi.itemtype = 'course'
LEFT JOIN mdl_grade_grades gg ON gg.itemid = gi.id AND gg.userid = u.id
WHERE (
    (l.timecreated BETWEEN EXTRACT(EPOCH FROM TO_TIMESTAMP('2023-02-20', 'YYYY-MM-DD'))
                      AND EXTRACT(EPOCH FROM TO_TIMESTAMP('2023-03-19', 'YYYY-MM-DD')))
    OR
    (l.timecreated BETWEEN EXTRACT(EPOCH FROM TO_TIMESTAMP('2024-02-19', 'YYYY-MM-DD'))
                      AND EXTRACT(EPOCH FROM TO_TIMESTAMP('2024-03-17', 'YYYY-MM-DD')))
) AND gg.finalgrade != 0
GROUP BY u.id, gg.finalgrade;


DROP VIEW IF EXISTS moodle.public.student_activity_normalized;
CREATE VIEW moodle.public.student_activity_normalized AS
SELECT
    (assign_clicks - avg_assign) / NULLIF(stddev_assign, 0) AS assign_clicks_norm,
    (quiz_clicks - avg_quiz) / NULLIF(stddev_quiz, 0) AS quiz_clicks_norm,
    (forum_clicks - avg_forum) / NULLIF(stddev_forum, 0) AS forum_clicks_norm,
    (resource_clicks - avg_resource) / NULLIF(stddev_resource, 0) AS resource_clicks_norm,
    (url_clicks - avg_url) / NULLIF(stddev_url, 0) AS url_clicks_norm,
    final_grade_binary
FROM moodle.public.student_activity,
(
    SELECT
        AVG(assign_clicks) AS avg_assign, STDDEV(assign_clicks) AS stddev_assign,
        AVG(quiz_clicks) AS avg_quiz, STDDEV(quiz_clicks) AS stddev_quiz,
        AVG(forum_clicks) AS avg_forum, STDDEV(forum_clicks) AS stddev_forum,
        AVG(resource_clicks) AS avg_resource, STDDEV(resource_clicks) AS stddev_resource,
        AVG(url_clicks) AS avg_url, STDDEV(url_clicks) AS stddev_url
    FROM moodle.public.student_activity
) AS stats_values;

SELECT * FROM student_activity_normalized;