String Parser Documentation
_____________________________
This script is composed of 7 functions:

Tokenize_String -

Breaks down string using NLTK Tokenizer
Returns tokenized string (It comes in a list of words)
All punctuation is filtered out

Generate_Score -

Takes an input of the row (List), and tokenizes everything into one large list
for each word in the row that is in our search string, we add one point to the score
An idea that I had, but haven't implemented - Base the score as a percentage based on how many words are in the
row in its entirety - I would like feedback, if this could increase accuracy, I could easily implement it

Run_Through_Rows -
Goes through the entire CSV, generating a score for each row, if the row
has a high enough score, we hold it. We stop when we have encountered to rows that are 100% the same
(two blank rows)

Get_results -
Checks the score, and if we should carry it.

Add_Row -
Adds the row to its right place in our list holding it, as well as the score.
Lists are sorted DESC

Ship_values -
Puts the values into a JSON file, with each row in ASC order, as well as the
CSV title so we know what the data is

Run -
Calls on these methods and returns the JSON file

___________________________________________________-

Dependencies -

CSV Module
JSON Module
NLTK Word Tokenizer (We could easily write our own if this is too large)
String module - For punctuation


__

I was not sure how to return the JSON, please let me know. ALl forms of criticism would be greatly appreciated

