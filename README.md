# VBRA_Refbook_formatter
A small piece of software that re-formats the .csv/.xlsx that Waverley Basketball Association's back end produces to be compatible with Refbook.

## Table of Contents

- [Context and Problem](#Context_and_Problem)
- [Solution](#Solution)
- [TKTinter UI](#TKTinter_UI)
- [Result](#Result)



## Context and Problem
Our Basketball refereeing branch uses a program called "Refbook" to roster referees. Each week, a .csv or .xlsx of games would have to be uploaded to the platform with the game relevant information.
The association hosting the competition, Waverley Basketball Association (WBA), could create a .xlsx or .csv export of these games each week.

However, the formats that WBA's back end would produce and what Refbook required were slightly different, and each week someone would manually edit the values of the .xlsx in excel. This was a time consuming, and would often take up to an hour to do so.

## Solution
This small python script performs the simple data operations to convert one format to the other, using pandas.

It includes a very rudimentary ui written with TKinter

The script was compiled with PyInstaller for anyone wishing to us it, so someone who is non-technical could simply run the .exe and transform any file in seconds, rather than in an hour.

### TKTinter UI
In order to get some practice using TKinter, the UI created shows a preview of both the file being uploaded to the program and the output. 

## Result
The program worked as designed. The data transformation side is simple - both inputs and outputs are of a predictable structure.
Eventually WBA changed their back-end to output the csv in the correct format, and the program was no longer needed.

