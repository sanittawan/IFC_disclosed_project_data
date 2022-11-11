## IFC text data compilation from IFC disclosure website

Developed by: Sanittawan Nikki Tan
Repository available on: [GitHub]() 

The constraint is that the Excel extraction only allows the first 1,000 records to be downloaded at a time. Hence, we have to slice the data up as follows

1. By project type
2. By disclosure dates (for AS, always check the latest disclosure date because sometimes the latest disclosure date is after today)

### IFC IS
- File 1 - Jan 1, 1994 - Dec 31, 2000
- File 2 - Jan 1, 2001 - Dec 31, 2005
- File 3 - Jan 1, 2006 - Dec 31, 2007
- File 4 - Jan 1, 2008 - Dec 31, 2009
- File 5 - Jan 1, 2010 - Dec 31, 2010
- File 6 - Jan 1, 2011 - Dec 31, 2012
- File 7 - Jan 1, 2013 - Dec 31, 2014
- File 8 - Jan 1, 2015 - Dec 31, 2016
- File 9 - Jan 1, 2017 - Dec 31, 2019
- File 10 - Jan 1, 2020 - Nov 30, 2022

### IFC AS
- File 1 - Jan 1, 2009 - Dec 31, 2018
- File 2 - Jan 1, 2019 - Mar 31, 2023

## Command line usage - For periodic data update

Prior to using, make sure to activate your python environment. The list of dependencies can be found below.

To update data, first, go to IFC disclosure website and download the latest data filtering for the project type and disclosure date range. Next, you need to run 2 commands, one for IS and another for AS.

In your shell, navigate to the root of the folder and execute below. Executing below will consolidate Investment Services data

`$ python consolidate_data.py IS`

The consolidated files will be found in .\Investment_Services\Consolidated_data_set

For investment services data, one project can appear in more than one role because the difference comes from document types. One project can have multiple document types. The code for data consolidation produces two files.
1. <date> IFC_Investment_disclosed_projects_text_data.csv - this file will have repeated project IDs among the rows
2. <date> Unique_IFC_Investment_disclosed_projects_text_data.csv - each row contains a unique project ID. Different document types are transposed to be columns.

For Advisory services, execute the following:

`$ python consolidate_data.py AS`

The consolidated files will be found in .\Advisory_Services\Consolidated_data_set with file name <date> IFC_Advisory_disclosed_projects_text_data.csv

## Version & Dependecies

Code in python 3.9.13

pandas==1.5.0
numpy==1.23.3