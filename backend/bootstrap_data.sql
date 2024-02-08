-- Insert queries for DatabaseUser table
INSERT INTO user (id, name, username, password, salt, created_at, role)
VALUES
    (1, 'Admin',   'admin',   '62bf5eb5963e4cedeb9398122a08c9898bce33129ddb353a3dc27b901beb24f4', 'dda5fcac24f82be513a76f60ee27aae1', '2024-02-05T19:58:52.973293', 'editor'),
    (2, 'Teacher', 'teacher', '1a9c85505f939f8173c768b4cc35628ef3bd14a62fb7d2d08726b9b32fec26e9', '3a671e8879fe33e51e9ef6c8f7c003e1', '2024-02-02T19:58:52.973293', 'viewer'),
    (3, 'Student', 'student', '228cccd967095e0352b0963e9629f211da87859615ca88af986a9dc5ce253925', 'f8b0bb8d90b6e298b4cbae7fbe6ffe56', '2024-02-04T19:58:52.973293', 'restricted')
ON CONFLICT(id) DO NOTHING;

-- Login Details
-- Admin   - admin:password
-- Teacher - teacher:password
-- Student - student:password

-- Insert queries for DatabaseQuiz table
INSERT INTO quiz (id, name, status, created_at, updated_at, updated_by)
VALUES
    (1, 'General Knowledge', 'published', '2024-02-05T19:58:52.973293', '2024-02-05T19:58:52.973293', 1)
ON CONFLICT(id) DO NOTHING;

-- Insert queries for DatabaseQuizQuestion table
INSERT INTO quiz_question (id, quiz_id, name, `order`)
VALUES
    (1,  1, 'What is the capital city of Australia?',                 1),
    (2,  1, 'Which planet is known as the "Red Planet"?',             2),
    (3,  1, 'Who wrote the play "Romeo and Juliet"',                  3),
    (4,  1, 'In which year did the Titanic sink',                     4),
    (5,  1, 'What is the largest mammal on Earth',                    5),
    (6,  1, 'Which country is known as the "Land of the Rising Sun"', 6),
    (7,  1, 'What is the chemical symbol for gold',                   7),
    (8,  1, 'Who painted the famous artwork "Starry Night"',          8),
    (9,  1, 'Which element has the chemical symbol "O"',              9),
    (10, 1, 'What is the largest ocean on Earth',                     10)
ON CONFLICT(id) DO NOTHING;

-- Insert queries for DatabaseQuizQuestionAnswer table
INSERT INTO quiz_question_answer (id, question_id, name, `order`, is_correct)
VALUES
    (1 , 1, 'Sydney',    1, 0),
    (2 , 1, 'Canberra',  2, 1),
    (3 , 1, 'Melbourne', 3, 0),
    (4 , 1, 'Brisbane',  4, 0),

    (5 , 2, 'Venus',   1, 0),
    (6 , 2, 'Mars',    2, 1),
    (7 , 2, 'Jupiter', 3, 0),
    (8 , 2, 'Saturn',  4, 0),

    (9 , 3, 'Charles Dickens',     1, 0),
    (10, 3, 'William Shakespeare', 2, 1),
    (11, 3, 'Jane Austen',         3, 0),
    (12, 3, 'Mark Twain',          4, 0),

    (13, 4, '1905', 1, 0),
    (14, 4, '1912', 2, 1),
    (15, 4, '1920', 3, 0),
    (16, 4, '1931', 4, 0),

    (17, 5, 'Elephant',   1, 0),
    (18, 5, 'Blue Whale', 2, 1),
    (19, 5, 'Giraffe',    3, 0),
    (20, 5, 'Polar Bear', 4, 0),

    (21, 6, 'China',       1, 0),
    (22, 6, 'Japan',       2, 1),
    (23, 6, 'South Korea', 3, 0),
    (24, 6, 'Vietnam',     4, 0),

    (25, 7, 'Au', 1, 1),
    (26, 7, 'Ag', 2, 0),
    (27, 7, 'Fe', 3, 0),
    (28, 7, 'Cu', 4, 0),

    (29, 8, 'Pablo Picasso',     1, 0),
    (30, 8, 'Vincent van Gogh',  2, 1),
    (31, 8, 'Leonardo da Vinci', 3, 0),
    (32, 8, 'Claude Monet',      4, 0),

    (33, 9, 'Oxygen', 1, 1),
    (34, 9, 'Osmium', 2, 0),
    (35, 9, 'Odium',  3, 0),
    (36, 9, 'Octane', 4, 0),

    (37, 10, 'Atlantic Ocean', 1, 0),
    (38, 10, 'Indian Ocean',   2, 0),
    (39, 10, 'Southern Ocean', 3, 0),
    (40, 10, 'Pacific Ocean',  4, 1)
ON CONFLICT(id) DO NOTHING;
