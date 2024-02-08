-- Create table for DatabaseUser
CREATE TABLE IF NOT EXISTS user (
    `id`         INTEGER PRIMARY KEY NOT NULL,
    `name`       TEXT NOT NULL,
    `username`   TEXT UNIQUE NOT NULL,
    `password`   TEXT NOT NULL,
    `salt`       TEXT NOT NULL,
    `created_at` TEXT NOT NULL,
    `role`       TEXT NOT NULL
);

-- Create table for DatabaseQuiz
CREATE TABLE IF NOT EXISTS quiz (
    `id`         INTEGER PRIMARY KEY NOT NULL,
    `name`       TEXT NOT NULL,
    `status`     TEXT NOT NULL,
    `created_at` TEXT NOT NULL,
    `updated_at` TEXT NOT NULL,
    `updated_by` INTEGER NOT NULL,
    FOREIGN KEY (updated_by) REFERENCES user(id) ON DELETE NO ACTION
);

-- Create table for DatabaseQuizQuestion
CREATE TABLE IF NOT EXISTS quiz_question (
    `id`      INTEGER PRIMARY KEY NOT NULL,
    `quiz_id` INTEGER NOT NULL,
    `name`    TEXT NOT NULL,
    `order`   INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
);

-- Create table for DatabaseQuizQuestionAnswer
CREATE TABLE IF NOT EXISTS quiz_question_answer (
    `id`          INTEGER PRIMARY KEY NOT NULL,
    `question_id` INTEGER NOT NULL,
    `name`        TEXT NOT NULL,
    `order`       INTEGER NOT NULL,
    `is_correct`  INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES quiz_question(id) ON DELETE CASCADE
);


