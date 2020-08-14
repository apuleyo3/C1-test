CREATE TABLE `Users` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `email` varchar(30) UNIQUE NOT NULL
);

CREATE TABLE `Submission` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_id` integer NOT NULL,
  `status` boolean NOT NULL,
  `created` timestamp
);

CREATE TABLE `Category` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(20) NOT NULL
);

CREATE TABLE `Questions` (
  `id` integer UNIQUE PRIMARY KEY AUTO_INCREMENT,
  `category_id` integer,
  `q_text` text NOT NULL,
  `q_ans` varchar(30)
);

CREATE TABLE `Answers` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_id` integer,
  `q_id` integer,
  `sb_id` integer,
  `q_ans` varchar(30),
  `created` timestamp NOT NULL
);

CREATE TABLE `Qoption` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `q_id` integer,
  `q_text` text NOT NULL
);

CREATE TABLE `Feedback` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_id` integer,
  `feed` text NOT NULL
);

ALTER TABLE `Submission` ADD FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`);

ALTER TABLE `Questions` ADD FOREIGN KEY (`category_id`) REFERENCES `Category` (`id`);

ALTER TABLE `Answers` ADD FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`);

ALTER TABLE `Answers` ADD FOREIGN KEY (`q_id`) REFERENCES `Questions` (`id`);

ALTER TABLE `Answers` ADD FOREIGN KEY (`sb_id`) REFERENCES `Submission` (`id`);

ALTER TABLE `Qoption` ADD FOREIGN KEY (`q_id`) REFERENCES `Questions` (`id`);

ALTER TABLE `Feedback` ADD FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`);
