# VBRA_Refbook_formatter
A small piece of software that re-formats the .csv/.xlsx that Waverley Basketball Association's back end produces to be compatible with Refbook.

## Problem outline
Our Basketball refereeing branch uses a program called "Refbook" to roster referees. Each week, a .csv or .xlsx of games would have to be uploaded to the platform with the relevant information.
The association hosting the competition, Waverley Basketball Association (WBA), could create a .xlsx or .csv export of the games each week

However, the formats that WBA's back end would produce and what Refbook required were slightly different, and each week someone would manually edit the values of the .xlsx in excel. This was a time consuming thing to do

## The solution
This small python script cperforms the simple data operations to convert one format to the other. 

It includes a very rudimentary ui written with TKinter

The script was compiled with PyInstaller for anyone wishing to us it, so someone who is non-technical could simply run the .exe and transform any file in seconds, rather than in an hour.


