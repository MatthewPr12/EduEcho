CREATE KEYSPACE IF NOT EXISTS user_feedbacks WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 2 };

USE user_feedbacks;


CREATE TABLE IF NOT EXISTS course_comments (
    course_id UUID,
    replied_to_id UUID,
    comment_id UUID,
    user_id UUID,

    comment_text TEXT,
    likes INT,
    dislikes INT,
    is_deleted BOOLEAN,
    is_edited BOOLEAN,

    timestamp TIMESTAMP,
    
    PRIMARY KEY ((course_id, replied_to_id), comment_id)
);


CREATE TABLE IF NOT EXISTS user_assessments (
    course_id UUID,
    user_id UUID,
    comment_id UUID,
    assessment_type INT,
    PRIMARY KEY ((course_id, user_id, comment_id), assessment_type)
);