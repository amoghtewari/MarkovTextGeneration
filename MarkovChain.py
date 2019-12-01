import json
import re
import random
import sys
import os
import nltk
import glob
nltk.download('punkt')
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()

def fixCaps(word):
    if word.isupper():
        word = word.lower()
    elif word [0].isupper():
        word = word.lower()
    else:
        word = word.lower()
    return word

def retSentences(filename, stopwords):
    f = open(filename, 'r', encoding='utf-8-sig')
    x = f.read()

    x = x.split('\n')
    x = " ".join(x)
    sentences = nltk.tokenize.sent_tokenize(x)
    sentListX = []
    for sentence in sentences:
        sentListX.append(tknzr.tokenize(sentence))
    
    sentList = []
    for sentence in sentListX:
        sent = []
        for word in sentence:
            word = fixCaps(word)
            if(word not in stopwords):
                sent.append(word)
        sentList.append(sent)
    f.close()
    return sentList

def retUnigrams(sentList):
    unigrams = {}
    unigramsX = {}
    for sentence in sentList:
        for i in range(0, len(sentence)):
            word = sentence[i]
            if(word != "." and word != "?" and word != "!"):
                if word in unigrams:
                    unigrams[word]+=1
                else:
                    unigrams[word]=1
    total=0
    for key, val in unigrams.items():
        total = total+val
    for key, val in unigrams.items():
        unigramsX[key]=val/total
    return unigramsX


def retBigrams(sentList):
    bigrams = {}
    bigramsX = {}
    for sentence in sentList:
        for i in range(0, len(sentence)-1):
            word1 = sentence[i]
            word2 = sentence[i+1]
            if(word2 != "." and word2 != "?" and word2 != "!"):
                if word1 in bigrams:
                    if word2 in bigrams[word1]:
                        bigrams[word1][word2]+=1
                    else:
                        bigrams[word1][word2]=1
                else:
                    bigrams[word1] = {word2:1}
    for key, val in bigrams.items():
        total=0
        bigramsX[key]={}
        for k, v in val.items():
            total+=v
        for k,v in val.items():
            bigramsX[key][k]=v/total
    return bigramsX
                    
def retTrigrams(sentList):
    trigrams={}
    trigramsX={}
    for sentence in sentList:
        if(len(sentence)>2):
            for i in range(0, len(sentence)-2):
                bigram = tuple(sentence[i:i+2])
                word3 = sentence[i+2]
                if(word3 != "." and word3 != "?" and word3 != "!"):
                    if bigram in trigrams:
                        if word3 in trigrams[bigram]:
                            trigrams[bigram][word3]+=1
                        else:
                            trigrams[bigram][word3]=1
                    else:
                        trigrams[bigram] = {word3:1}
    for key, val in trigrams.items():
        total=0
        trigramsX[key]={}
        for k, v in val.items():
            total+=v
        for k,v in val.items():
            trigramsX[key][k]=v/total
    
    return trigramsX
    
def pickWord1(unigrams):
    sum = 0.0
    retval = ""
    index = random.random()

    # Get a random word from the mapping
    for k, v in unigrams.items():
        sum += v
        if sum >= index and retval == "":
            retval = k
    return (retval,unigrams[k])

def pickWord2(word1, unigrams, bigrams):
    sum = 0.0
    retval = ""
    index = random.random()
    
    #get mapping for give word
    if(word1 in bigrams):
        mapX = bigrams[word1]
    else:
        retval = pickWord1(unigrams)
    
    # Get a random word from the mapping
    if('mapX' in locals()):
        for k, v in mapX.items():
            sum += v
            if sum >= index and retval == "":
                retval = (k, mapX[k])
    return retval

def pickWordN(word1, word2, unigrams, bigrams, trigrams):
    sum = 0.0
    retval = ""
    index = random.random()
    keyX = tuple([word1, word2])
    #get mapping for give word
    if(keyX in trigrams):
        mapX = trigrams[keyX]
    else:
        if (word2 in bigrams):
            mapX = bigrams[word2]
        else:
            retval = pickWord1(unigrams)
    
    # Get a random word from the mapping
    if('mapX' in locals()):
        for k, v in mapX.items():
            sum += v
            if sum >= index and retval == "":
                retval = (k, mapX[k])
    return retval


def retGenSentences(languageModel1, languageModel2, probFile1, probFile2):
    unigrams1 = languageModel1[0]
    bigrams1 = languageModel1[1]
    trigrams1 = languageModel1[2]
    unigrams2 = languageModel2[0]
    bigrams2 = languageModel2[1]
    trigrams2 = languageModel2[2]

    with open(probFile1, 'w') as file:
        file.write("Unigrams:- \n")
        file.write(json.dumps(unigrams1))
        file.write("\n\n")
        file.write("Bigrams:- \n")
        file.write(json.dumps(bigrams1))
        file.write("\n\n")
        file.write("Trigrams:- \n")
        for key in trigrams1.keys():
            file.write(str(key))
            file.write(str(trigrams1[key]))

    with open(probFile2, 'w') as file:
        file.write("Unigrams:- \n")
        file.write(json.dumps(unigrams2))
        file.write("\n\n")
        file.write("Bigrams:- \n")
        file.write(json.dumps(bigrams2))
        file.write("\n\n")
        file.write("Trigrams:- \n")
        for key in trigrams2.keys():
            file.write(str(key))
            file.write(str(trigrams2[key]))
        
    
    sentence1 = []
    sentence2 = []

    p11=1
    p12=1
    p21=1
    p22=1
    
    while(len(sentence1)<21):
        if(len(sentence1)==0):
            a,b = pickWord1(unigrams1)
            sentence1.append(a.capitalize())
            p11 = p11*b
            try:
                p12 = p12*unigrams2[a]
            except:
                p12 = p12*0.001
        elif(len(sentence1)==1):
            a,b = pickWord2(sentence1[0].lower(), unigrams1, bigrams1)
            sentence1.append(a)
            p11 = p11*b
            try:
                p12 = p12*bigrams2[sentence1[0]][a]
            except:
                p12 = p12*0.001
        else:
            a,b = pickWordN(sentence1[-2], sentence1[-1], unigrams1, bigrams1, trigrams1)
            sentence1.append(a)
            p11 = p11*b
            try:
                p12 = p12*trigrams2[tuple([sentence1[-2], sentence1[-1]])][a]
            except:
                p12 = p12*0.001

    while(len(sentence2)<21):
        if(len(sentence2)==0):
            a,b = pickWord1(unigrams2)
            sentence2.append(a.capitalize())
            p21 = p21*b
            try:
                p22 = p22*unigrams1[a]
            except:
                p22 = p22*0.001
        elif(len(sentence2)==1):
            a,b = pickWord2(sentence2[0].lower(), unigrams2, bigrams2)
            sentence2.append(a)
            p21 = p21*b
            try:
                p22 = p22*bigrams1[sentence2[0]][a]
            except:
                p22 = p22*0.001
        else:
            a,b = pickWordN(sentence2[-2], sentence2[-1], unigrams2, bigrams2, trigrams2)
            sentence2.append(a)
            p21 = p21*b
            try:
                p22 = p22*trigrams1[tuple([sentence2[-2], sentence2[-1]])][a]
            except:
                p22 = p22*0.001

    
    return (" ".join(sentence1)+".", " ".join(sentence2)+".", p11, p12, p21, p22)



def main(directory1, directory2, probFile1, probFile2, resultFile):
    #load stopwords
    f1 = open("EnglishStopwords.txt", 'r')
    stpwrds = f1.read()
    stopwords = stpwrds.split("\n")
    stopwords.append(',')
    stopwords.append(':')
    
    #load directory1 to language model
    os.chdir(directory1)
    files=[]
    for file in glob.glob("*.txt"):
        files.append(file)
    
    wordList=[]
    
    for filename in files:
        wL = retSentences(filename, stopwords)
        wordList = wordList + wL
    
    unigrams1 = retUnigrams(wordList)
    bigrams1 = retBigrams(wordList)
    trigrams1 = retTrigrams(wordList)
    
    #load directory2 to language model
    os.chdir('..')
    os.chdir(directory2)
    files=[]
    for file in glob.glob("*.txt"):
        files.append(file)
    
    wordList=[]
    
    for filename in files:
        wL = retSentences(filename, stopwords)
        wordList = wordList + wL
    
    unigrams2 = retUnigrams(wordList)
    bigrams2 = retBigrams(wordList)
    trigrams2 = retTrigrams(wordList)

    os.chdir('..')
    fW = open(resultFile, "a")
    
    for i in range(0,10):
        s1, s2, p11, p12, p21, p22 = retGenSentences([unigrams1, bigrams1, trigrams1], [unigrams2, bigrams2, trigrams2], probFile1, probFile2)
        fW.write("Model 1 Sentence: \n")
        fW.write(s1+"\n")
        fW.write("Probability of sentence was generated by model 1"+"("+directory1+")"+":- "+str(p11)+ "\n")
        fW.write("Probability of sentence was generated by model 2"+"("+directory2+")"+":- "+str(p12)+ "\n")
        fW.write("Model 2 Sentence: \n")
        fW.write(s2+"\n")
        fW.write("Probability of sentence was generated by model 1"+"("+directory1+")"+":- "+str(p22)+ "\n")
        fW.write("Probability of sentence was generated by model 2"+"("+directory2+")"+":- "+str(p21)+ "\n\n")

    fW.close()


if __name__ == "__main__":
    directory1 = str(sys.argv[1])
    directory2 = str(sys.argv[2])
    probFile1 = str(sys.argv[3])
    probFile2 = str(sys.argv[4])
    resultFile = str(sys.argv[5])

    main(directory1, directory2, probFile1, probFile2, resultFile)