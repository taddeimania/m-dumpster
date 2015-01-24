#MySQL Related Data Exporter

This program is intended to retrieve records from a MySQL DB table based on data found in another table.

The typical use case would be a database containing many tennant's information which can be aggregated by a single field
(example: company_id).  This program allows you to easily define those relationships and it creates
a .sql dump file of each table you define.

Syntax:

python src/main.py

#JAML

This program uses a custom format for knowing which database tables to pull down and how to join to your defined field.
There are currently 4 ways to tell the program how to pull down a database table:

TABLE_NAME|TARGET_FIELD_COLUMN - This will do a straight pull down of a database table for the given target field.

TABLE_NAME|JOINING_COLUMN > JOINING_TABLE|TARGET_FIELD_COLUMN - This will get all records for the first table and join
the tables linearly until it reaches the table that joines on your target field.

*TABLE_NAME - This will do a full table dump regardless of parameters (WARNING: Use this sparingly)

\#TABLE_NAME - This will extract a table's schema with no data in it. This might be important - you'll learn quickly if you need to do this.
