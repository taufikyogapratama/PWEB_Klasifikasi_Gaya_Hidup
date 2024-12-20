-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 20, 2024 at 02:32 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

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
-- Table structure for table `aturan`
--

CREATE TABLE `aturan` (
  `Id_Aturan` int NOT NULL,
  `ID_Pertanyaan` int NOT NULL,
  `Kondisi` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Hasil_Klasifikasi` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Nasihat` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `aturan`
--

INSERT INTO `aturan` (`Id_Aturan`, `ID_Pertanyaan`, `Kondisi`, `Hasil_Klasifikasi`, `Nasihat`) VALUES
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
-- Table structure for table `hasil`
--

CREATE TABLE `hasil` (
  `ID_Hasil` int NOT NULL,
  `Nama` varchar(100) NOT NULL,
  `Umur` int NOT NULL,
  `Berat_Badan` float NOT NULL,
  `Tinggi_Badan` float NOT NULL,
  `Olahraga` varchar(50) DEFAULT NULL,
  `Tidur` varchar(50) DEFAULT NULL,
  `Stres` varchar(50) DEFAULT NULL,
  `Makanan` varchar(50) DEFAULT NULL,
  `Hidrasi` varchar(50) DEFAULT NULL,
  `Timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `hasil`
--

INSERT INTO `hasil` (`ID_Hasil`, `Nama`, `Umur`, `Berat_Badan`, `Tinggi_Badan`, `Olahraga`, `Tidur`, `Stres`, `Makanan`, `Hidrasi`, `Timestamp`) VALUES
(1, 'zilong', 18, 59, 170, 'Sehat', 'Sehat', 'Tidak Sehat', 'Sehat', 'Sehat', '2024-12-20 13:52:23');

-- --------------------------------------------------------

--
-- Table structure for table `pertanyaan`
--

CREATE TABLE `pertanyaan` (
  `ID_Pertanyaan` int NOT NULL,
  `Teks_Pertanyaan` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Kategori` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pertanyaan`
--

INSERT INTO `pertanyaan` (`ID_Pertanyaan`, `Teks_Pertanyaan`, `Kategori`) VALUES
(4, 'Seberapa sering Anda berolahraga dalam seminggu?', 'Olahraga'),
(5, 'Berapa jam rata-rata Anda tidur per hari?', 'Tidur'),
(6, 'Seberapa sering Anda merasa stres dalam sebulan?', 'Stres'),
(7, 'Seberapa sering Anda makan makanan cepat saji dalam seminggu?', 'Makanan'),
(8, 'Berapa banyak air yang Anda minum dalam sehari?', 'Hidrasi');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `aturan`
--
ALTER TABLE `aturan`
  ADD PRIMARY KEY (`Id_Aturan`),
  ADD KEY `FK_Aturan_Pertanyaan` (`ID_Pertanyaan`);

--
-- Indexes for table `hasil`
--
ALTER TABLE `hasil`
  ADD PRIMARY KEY (`ID_Hasil`);

--
-- Indexes for table `pertanyaan`
--
ALTER TABLE `pertanyaan`
  ADD PRIMARY KEY (`ID_Pertanyaan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `aturan`
--
ALTER TABLE `aturan`
  MODIFY `Id_Aturan` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT for table `hasil`
--
ALTER TABLE `hasil`
  MODIFY `ID_Hasil` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `pertanyaan`
--
ALTER TABLE `pertanyaan`
  MODIFY `ID_Pertanyaan` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `aturan`
--
ALTER TABLE `aturan`
  ADD CONSTRAINT `FK_Aturan_Pertanyaan` FOREIGN KEY (`ID_Pertanyaan`) REFERENCES `pertanyaan` (`ID_Pertanyaan`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
