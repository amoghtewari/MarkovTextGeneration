To run,
"
python3 MarkovChain.py R_Sidney_Bowen Mary_W_Shelley PROB-FILE-1.txt PROB-FILE-2.txt RESULT-FILE.txt
"

Implementing and evaluating a simple probabilistic language model. When called the code will take a directory containing your downloaded texts. It will process the supplied texts to collect a set of the unique unigrams, bigrams, and trigrams present in the texts after removing stopwords, and then use this set to calculate an independent probability of each unigram as well as conditional probabilities given preceeding unigrams and bigrams. The resulting distributions are saved to a probability file. The code will then generate a random sample of 10 sequences of at most 20
tokens. These sequences and their probabilities will then be written to a result file.