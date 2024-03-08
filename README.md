#Resume_parse


-Parse_resume.py
This file has all the functions needed as well as the main function to run the test on the sample resumes.

-parse_note.ipynb
This file was used as a scratch paper to brainstorm/try different things.
Note: messy file..


Extract function
-initial function from original github was creating discrepancies
-Rewrote new function that made the text file cleaner.

name
-Initial version from the original github produced 30~ errors 
-Tried many different regular expressions but the best one I found was simply getting the first two words.
-Creates error if name is 3 words or more, if there is a page number, etc..

phone & email
-using the regex from the OG github, new regex from online didn't help

website
-does not work at all,,, gave up for now.. 

College
-Tried regular expression 
r"(?<!\bEDUCATION\s)(?:\b(?:University|College|Institute|School) of \b\w+|\b\w+ (?:University|College|Institute|School))\b"
But did not end up working correctly. Produced outputs like: "Education University"

-Instead found a data of US universities
-https://gist.github.com/zonca/d0c26460597704feb132#file-us_universities-csv
-us_universities.csv
-Cleaned the data, process in data_prep.ipynb, text file list in college_names

-Within this, tried two method
-One generic one, a simple search
-Second which normalized the resume text and college list to reduce errors.
-This method didn't product any output.. (debugging may make the outputs nice though)

..
pyresparser
-https://github.com/OmkarPathak/pyresparser/tree/master/pyresparser
-tried importing the premade model but due to version errors, I could not use it
