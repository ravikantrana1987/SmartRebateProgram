USE [master]
GO
/****** Object:  Database [RebateProgram]    Script Date: 04-03-2025 08:38:36 ******/
CREATE DATABASE [RebateProgram]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'RebateProgram', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\RebateProgram.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'RebateProgram_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\RebateProgram_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [RebateProgram] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [RebateProgram].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [RebateProgram] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [RebateProgram] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [RebateProgram] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [RebateProgram] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [RebateProgram] SET ARITHABORT OFF 
GO
ALTER DATABASE [RebateProgram] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [RebateProgram] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [RebateProgram] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [RebateProgram] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [RebateProgram] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [RebateProgram] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [RebateProgram] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [RebateProgram] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [RebateProgram] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [RebateProgram] SET  DISABLE_BROKER 
GO
ALTER DATABASE [RebateProgram] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [RebateProgram] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [RebateProgram] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [RebateProgram] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [RebateProgram] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [RebateProgram] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [RebateProgram] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [RebateProgram] SET RECOVERY FULL 
GO
ALTER DATABASE [RebateProgram] SET  MULTI_USER 
GO
ALTER DATABASE [RebateProgram] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [RebateProgram] SET DB_CHAINING OFF 
GO
ALTER DATABASE [RebateProgram] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [RebateProgram] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [RebateProgram] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [RebateProgram] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'RebateProgram', N'ON'
GO
ALTER DATABASE [RebateProgram] SET QUERY_STORE = ON
GO
ALTER DATABASE [RebateProgram] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [RebateProgram]
GO
/****** Object:  Table [dbo].[category]    Script Date: 04-03-2025 08:38:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[category](
	[category_id] [int] IDENTITY(1,1) NOT NULL,
	[category_name] [varchar](150) NOT NULL,
	[description] [varchar](200) NOT NULL,
	[is_active] [bit] NOT NULL,
 CONSTRAINT [PK_category] PRIMARY KEY CLUSTERED 
(
	[category_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[manufacturer]    Script Date: 04-03-2025 08:38:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[manufacturer](
	[manufacturer_id] [int] IDENTITY(1,1) NOT NULL,
	[manufacturer_name] [nvarchar](150) NOT NULL,
 CONSTRAINT [PK_manufacturer] PRIMARY KEY CLUSTERED 
(
	[manufacturer_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[product]    Script Date: 04-03-2025 08:38:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[product](
	[product_id] [int] IDENTITY(1,1) NOT NULL,
	[product_name] [nvarchar](150) NOT NULL,
	[description] [nvarchar](200) NOT NULL,
	[category_id] [int] NOT NULL,
	[unit_price] [numeric](18, 2) NOT NULL,
	[is_active] [bit] NOT NULL,
	[manufacturer_id] [int] NOT NULL,
 CONSTRAINT [PK_product] PRIMARY KEY CLUSTERED 
(
	[product_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RebateProgram]    Script Date: 04-03-2025 08:38:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[RebateProgram](
	[rebate_program_id] [int] IDENTITY(1,1) NOT NULL,
	[program_name] [varchar](150) NOT NULL,
	[start_date] [date] NOT NULL,
	[end_date] [date] NOT NULL,
	[minimum_sales_value] [numeric](18, 2) NOT NULL,
 CONSTRAINT [PK_RebateProgram] PRIMARY KEY CLUSTERED 
(
	[rebate_program_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[category] ON 

INSERT [dbo].[category] ([category_id], [category_name], [description], [is_active]) VALUES (1, N'Insecticides', N'Insecticides are chemicals used to kill or control insects that can harm plants, animals, or humans.', 1)
INSERT [dbo].[category] ([category_id], [category_name], [description], [is_active]) VALUES (3, N'Fungicides', N'Fungicides are chemicals used to prevent or control fungal infections in plants, crops, or surfaces.', 1)
INSERT [dbo].[category] ([category_id], [category_name], [description], [is_active]) VALUES (4, N'Herbicides', N'Herbicides are chemicals used to control or kill unwanted plants, particularly weeds.', 1)
INSERT [dbo].[category] ([category_id], [category_name], [description], [is_active]) VALUES (5, N'Seed Treatments', N'Seed treatments are protective coatings or chemicals applied to seeds to prevent disease, pests, and enhance germination.', 1)
SET IDENTITY_INSERT [dbo].[category] OFF
GO
SET IDENTITY_INSERT [dbo].[manufacturer] ON 

INSERT [dbo].[manufacturer] ([manufacturer_id], [manufacturer_name]) VALUES (1, N'AgriTech')
SET IDENTITY_INSERT [dbo].[manufacturer] OFF
GO
SET IDENTITY_INSERT [dbo].[product] ON 

INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (1, N'NovaShieldTech® Ultra', N'NovaShieldTech® Ultra', 1, CAST(100.00 AS Numeric(18, 2)), 1, 1)
INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (2, N'PestBusterTech® Max', N'PestBusterTech® Max', 1, CAST(150.50 AS Numeric(18, 2)), 1, 1)
INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (3, N'CropGuardian® Elite', N'CropGuardian® Elite', 1, CAST(125.85 AS Numeric(18, 2)), 1, 1)
INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (5, N'FungiSafeTech® Pro', N'FungiSafeTech® Pro', 3, CAST(110.25 AS Numeric(18, 2)), 1, 1)
INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (6, N'SporeBlock® XT', N'SporeBlock® XT', 3, CAST(225.15 AS Numeric(18, 2)), 1, 1)
INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (7, N'WeedTerminatorTech® Plus', N'WeedTerminatorTech® Plus', 4, CAST(154.25 AS Numeric(18, 2)), 1, 1)
INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (8, N'SeedField® Control', N'SeedField® Control', 4, CAST(254.25 AS Numeric(18, 2)), 1, 1)
INSERT [dbo].[product] ([product_id], [product_name], [description], [category_id], [unit_price], [is_active], [manufacturer_id]) VALUES (9, N'SeedArmor® 500', N'SeedArmor® 500', 5, CAST(145.25 AS Numeric(18, 2)), 1, 1)
SET IDENTITY_INSERT [dbo].[product] OFF
GO
ALTER TABLE [dbo].[product]  WITH CHECK ADD  CONSTRAINT [FK_product_category] FOREIGN KEY([category_id])
REFERENCES [dbo].[category] ([category_id])
GO
ALTER TABLE [dbo].[product] CHECK CONSTRAINT [FK_product_category]
GO
ALTER TABLE [dbo].[product]  WITH NOCHECK ADD  CONSTRAINT [FK_product_manufacturer] FOREIGN KEY([manufacturer_id])
REFERENCES [dbo].[manufacturer] ([manufacturer_id])
GO
ALTER TABLE [dbo].[product] CHECK CONSTRAINT [FK_product_manufacturer]
GO
USE [master]
GO
ALTER DATABASE [RebateProgram] SET  READ_WRITE 
GO
