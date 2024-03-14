-- Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Animes table
CREATE TABLE Animes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    episode_count INT,
    author VARCHAR(100),
    release_date DATE
);

-- Table for animes watched by users
CREATE TABLE Watched_Animes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    anime_id INTEGER,
    finish_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (anime_id) REFERENCES Animes(id)
);

-- Inserting example users
INSERT INTO Users (username, password) VALUES
('user1', 'password1'),
('user2', 'password2'),
('user3', 'password3');

-- Inserting example animes
INSERT INTO Animes (name, description, episode_count, author, release_date) VALUES
('Naruto', 'A young ambitious ninja seeks to become the strongest ninja and be recognized by his peers.', 220, 'Masashi Kishimoto', '2002-10-03'),
('One Piece', 'A group of pirates embarks on an epic quest to find the legendary treasure, the One Piece.', 1000, 'Eiichiro Oda', '1999-07-22'),
('Dragon Ball Z', 'Goku and his friends fight to protect Earth against extraterrestrial threats and intergalactic tyrants.', 291, 'Akira Toriyama', '1989-04-26');

-- Inserting example watched animes by users
INSERT INTO Watched_Animes (user_id, anime_id, finish_date) VALUES
(1, 1, '2023-05-10'), -- User 1 finished watching Naruto on May 10, 2023
(1, 2, '2022-12-15'), -- User 1 finished watching One Piece on December 15, 2022
(2, 2, '2023-01-20'); -- User 2 finished watching One Piece on January 20, 2023
