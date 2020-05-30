# Search-Engine

Indexer.py takes all the json files from a certain directory and indexes them after n websites visited.
It sorts those n websites and saves them into partial indexes. 
The output is output_indexerN.txt, with N being how many files it has saved. 
The output ids_identifier.txt stores the ids to their websites.


LL.py holds the Postings class which is represented by LL.


duplicates.py is called to see if any of the websites are duplicates of another in the current index


merge.py gets a buffer of all the partial indexes and saves them into files based off the first letter.
All the "a"'s are together, all the "b"'s, and so. 
It outputs it as 0-9_output_indexer.txt, A-F_output_indexer.txt, and so on
It then tries to find where all those letters are stored in each file. It outputs that as find_letter.txt


search.py


ranker.py


searchinterface.py

Link to output files: https://drive.google.com/open?id=18VBiG8BNT3uWEuGyv2pshH-PG3vg86-J


