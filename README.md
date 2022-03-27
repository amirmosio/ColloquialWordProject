# ColloquialWordProject
Collecting persian colloquial word dataset and language model


# Colloquial detection

First we combine colloquial data set with formal dataset from wikipedia.
Then we use something like word2vec to build a language model for both formal and colloquial words.
After that we can process colloquial data set and check words that does not appear in formal dataset and find the nearest words to find initial weak synonyms, so we can use them in further process to find the best synonym.

So here we need to database, one for formal words and text and one for colloquial corpses:
 - wikipedia seems a good candidate for formal dataset
 - twitter dataset for colloquial data
 
Using these two datasets:
 - [Persian wikipedia corpus for formal dataset](https://github.com/Text-Mining/Persian-Wikipedia-Corpus)
 - [Persian twitter corpus for colloquial dataset](https://iasbs.ac.ir/~ansari/lscp/)
 - [Persian stop words for preprocessing](https://github.com/amirshnll/persian-stop-word)