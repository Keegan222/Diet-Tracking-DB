-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 07, 2022 at 11:49 PM
-- Server version: 8.0.28
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `comp_3753`
--

-- --------------------------------------------------------

--
-- Table structure for table `food_analysis`
--

CREATE TABLE `food_analysis` (
  `record_id` int NOT NULL,
  `calories` int NOT NULL,
  `fats` int NOT NULL,
  `sugars` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `food`
--


CREATE TABLE `food` (
  `id_number` int NOT NULL,
  `food_name` text COLLATE utf8mb4_general_ci NOT NULL,
  `food_category` enum('Vegetables and Fruit','Grain Products','Milk Products','Meat and Alternatives','Fats, Oils, and Sweets') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `calories` int NOT NULL,
  `sugars` int NOT NULL,
  `fats` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Table structure for table `food_records`
--

CREATE TABLE `food_records` (
  `id_number` int NOT NULL,
  `owner_email` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `duration` double NOT NULL,
  `meal_type` enum('Breakfast','Lunch','Dinner','Snack','Other') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `food_ids` text COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `goal_analysis`
--

CREATE TABLE `goal_analysis` (
  `record_id` int NOT NULL,
  `food_category_variety` enum('Good','Medium','Poor') COLLATE utf8mb4_general_ci NOT NULL,
  `average_breakfast_time` float NOT NULL,
  `average_lunch_time` float NOT NULL,
  `average_dinner_time` float NOT NULL,
  `calories_per_day` float NOT NULL,
  `fats_per_day` float NOT NULL,
  `sugars_per_day` float NOT NULL,
  `status` enum('In Progress','Finished','Failed') COLLATE utf8mb4_general_ci NOT NULL,
  `progression_percentage` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `goal_records`
--

CREATE TABLE `goal_records` (
  `id_number` int NOT NULL,
  `owner_email` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `goal_type` enum('Total amount of a nutrition type under a value','Total amount of a nutrition type over a value','Total amount of a nutrition type within a range','Total occurrences of a food category in meals over a certain value','Total occurrences of a food category in meals under a certain value','Total occurrences of a food category in meals within a range') COLLATE utf8mb4_general_ci NOT NULL,
  `nutrition_category` enum('Vegetables and Fruit','Grain Products','Milk Products','Meat and Alternatives','Fats, Oils, and Sweets','Calories','Sugars','Fats') COLLATE utf8mb4_general_ci NOT NULL,
  `lower_bound` int COLLATE utf8mb4_general_ci NOT NULL,
  `upper_bound` int COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_data`
--

CREATE TABLE `user_data` (
  `first_name` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `middle_name` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `last_name` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `email_address` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `premium` tinyint(1) NOT NULL,
  `password_hash` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `food_analysis`
--
ALTER TABLE `food_analysis`
  ADD UNIQUE KEY `record_id` (`record_id`);

--
-- Indexes for table `food`
--
ALTER TABLE `food`
  ADD PRIMARY KEY (`id_number`);

--
-- Indexes for table `food_records`
--
ALTER TABLE `food_records`
  ADD PRIMARY KEY (`id_number`);

--
-- Indexes for table `goal_records`
--
ALTER TABLE `goal_records`
  ADD PRIMARY KEY (`id_number`);

--
-- Indexes for table `user_data`
--
ALTER TABLE `user_data`
  ADD PRIMARY KEY (`email_address`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `foods`
--
ALTER TABLE `food`
  MODIFY `id_number` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `food_records`
--
ALTER TABLE `food_records`
  MODIFY `id_number` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `goal_records`
--
ALTER TABLE `goal_records`
  MODIFY `id_number` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
