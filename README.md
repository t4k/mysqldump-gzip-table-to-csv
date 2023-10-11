# mysqldump-gzip-table-to-csv

## Introduction

This Python script extracts a single table from a gzipped MySQL dump file into CSV format.

MySQL dumps contain a series of INSERT statements and can be difficult to import or manipulate, often requiring significant hardware upgrades. This script provides an easy way to convert these dump files into the universal CSV format.

The script takes advantage of the structural similarities between MySQL INSERT statements and CSV files. It uses Python’s CSV parser to convert the MySQL syntax into CSV, enabling the data to be read and used more easily.

## Usage

Just run the script followed by the filename of a gzipped SQL file and the name of a table in the database.

`python mysqldump_gzip_table_to_csv.py /path/to/db.sql.gz table_name`

## How It Works

The following SQL:

    INSERT INTO `page` VALUES (1,0,'April','',1,0,0,0.778582929065,'20140312223924','20140312223929',4657771,20236,0),
    (2,0,'August','',0,0,0,0.123830928525,'20140312221818','20140312221822',4360163,11466,0);

is turned into the following CSV:

    1,0,April,1,0,0,0.778582929065,20140312223924,20140312223929,4657771,20236,0
    2,0,August,0,0,0,0.123830928525,20140312221818,20140312221822,4360163,11466,0

## Standing on the Shoulders of Giants

- [jamesmishra/mysqldump-to-csv](https://github.com/jamesmishra/mysqldump-to-csv)
- [yashsmehta/mysqldump-to-csv](https://github.com/yashsmehta/mysqldump-to-csv)
