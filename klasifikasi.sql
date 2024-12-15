-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 15, 2024 at 05:02 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `klasifikasi`
--

-- --------------------------------------------------------

--
-- Table structure for table `Aturan`
--

CREATE TABLE `Aturan` (
  `Id_Aturan` int(11) NOT NULL,
  `ID_Pertanyaan` int(11) NOT NULL,
  `Kondisi` varchar(50) NOT NULL,
  `Hasil_Klasifikasi` varchar(50) NOT NULL,
  `Nasihat` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Aturan`
--

INSERT INTO `Aturan` (`Id_Aturan`, `ID_Pertanyaan`, `Kondisi`, `Hasil_Klasifikasi`, `Nasihat`) VALUES
(53, 4, '>= 3', 'Sehat', 'Teruskan kebiasaan berolahraga Anda!'),
(54, 4, '< 3', 'Tidak Sehat', 'Cobalah untuk berolahraga lebih sering, minimal 3 kali seminggu.'),
(55, 5, '>= 7', 'Sehat', 'Tidur cukup sangat penting. Lanjutkan kebiasaan tidur Anda!'),
(56, 5, '< 7', 'Tidak Sehat', 'Cobalah tidur lebih dari 7 jam setiap malam.'),
(57, 6, '<= 3', 'Sehat', 'Stres rendah sangat baik, terus pertahankan!'),
(58, 6, '> 3', 'Tidak Sehat', 'Kelola stres Anda dengan teknik relaksasi seperti meditasi atau olahraga.'),
(59, 7, '<= 2', 'Sehat', 'Hindari makanan cepat saji dan pilih makanan sehat.'),
(60, 7, '> 2', 'Tidak Sehat', 'Kurangi konsumsi makanan cepat saji, sebaiknya tidak lebih dari 2 kali seminggu.'),
(61, 8, '>= 8', 'Sehat', 'Konsumsi air yang cukup sangat baik untuk tubuh Anda!'),
(62, 8, '< 8', 'Tidak Sehat', 'Pastikan Anda minum minimal 8 gelas air per hari untuk hidrasi yang optimal.');

-- --------------------------------------------------------

--
-- Table structure for table `Pertanyaan`
--

CREATE TABLE `Pertanyaan` (
  `ID_Pertanyaan` int(11) NOT NULL,
  `Teks_Pertanyaan` varchar(255) NOT NULL,
  `Kategori` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Pertanyaan`
--

INSERT INTO `Pertanyaan` (`ID_Pertanyaan`, `Teks_Pertanyaan`, `Kategori`) VALUES
(4, 'Seberapa sering Anda berolahraga dalam seminggu?', 'Olahraga'),
(5, 'Berapa jam rata-rata Anda tidur per hari?', 'Tidur'),
(6, 'Seberapa sering Anda merasa stres dalam sebulan?', 'Stres'),
(7, 'Seberapa sering Anda makan makanan cepat saji dalam seminggu?', 'Makanan'),
(8, 'Berapa banyak air yang Anda minum dalam sehari?', 'Hidrasi');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Aturan`
--
ALTER TABLE `Aturan`
  ADD PRIMARY KEY (`Id_Aturan`),
  ADD KEY `FK_Aturan_Pertanyaan` (`ID_Pertanyaan`);

--
-- Indexes for table `Pertanyaan`
--
ALTER TABLE `Pertanyaan`
  ADD PRIMARY KEY (`ID_Pertanyaan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Aturan`
--
ALTER TABLE `Aturan`
  MODIFY `Id_Aturan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT for table `Pertanyaan`
--
ALTER TABLE `Pertanyaan`
  MODIFY `ID_Pertanyaan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Aturan`
--
ALTER TABLE `Aturan`
  ADD CONSTRAINT `FK_Aturan_Pertanyaan` FOREIGN KEY (`ID_Pertanyaan`) REFERENCES `Pertanyaan` (`ID_Pertanyaan`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
