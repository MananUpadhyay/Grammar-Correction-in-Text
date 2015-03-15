import nltk,subprocess,sys
from nltk.corpus import brown

def getSuffix(word,type):
    wlen = len(word)
    return word[wlen-type:wlen]

def format(out,tr):
    outList = []
    ou = open(out,'w')
    # tr = open(train,'r')
    for line in tr:
        # print(".")
        # Skipping
        splitLineSet = set()
        for itemTuple in line:
            splitLineSet.add(str(itemTuple[0]))

        if ("its" not in splitLineSet and
                    "it\'s" not in splitLineSet and
                    "too" not in splitLineSet and
                    "to" not in splitLineSet and
                    "your" not in splitLineSet and
                    "you\'re" not in splitLineSet and
                    "their" not in splitLineSet and
                    "they\'re" not in splitLineSet and
                    "loose" not in splitLineSet and
                    "lose" not in splitLineSet):
            # print("skipped")
            continue

        splitLength = len(line)
        prevWord1 = "^bos$"
        prevWord2 = "^bos$"
        prevClass = "^cla$$"
        curWord = ""
        nextWord = ""
        curClassLabel = ""
        suffix2 = ""
        suffix3 = ""

        for i in range(splitLength):
            tagLine = ""
            outTagLine = ""
            splitLine = line[i]
            # handle cur;
            if ("its" != splitLine[0] and
                        "it\'s" != splitLine[0] and
                        "too" != splitLine[0] and
                        "to" != splitLine[0] and
                        "your" != splitLine[0] and
                        "you\'re" != splitLine[0] and
                        "their" != splitLine[0] and
                        "they\'re" != splitLine[0] and
                        "loose" != splitLine[0] and
                        "lose" != splitLine[0]):
                # print("skipped Word")
                continue

            # handle cur word;
            curWord = str(splitLine[0])
            suffix2 = getSuffix(curWord,2)
            suffix3 = getSuffix(curWord,3)
            curWordTag = splitLine[1]
            curClassLabel = str(curWordTag)

            #handle prev word;
            if(i == 0):
                prevWord1 = "^bos$"
                prevWord2 = "^bos$"
            elif (i == 1):
                prevWord2 = "^bos$"
            else:
                prevTuple1 = line[i-1]
                prevWord1 = str(prevTuple1[0])
                prevWordTag1 = str(prevTuple1[1])

                prevTuple2 = line[i-2]
                prevWord2 = str(prevTuple2[0])
                prevWordTag2 = str(prevTuple2[1])

                prevClassLabel1 = str(prevWordTag1)
                prevClassLabel2 = str(prevWordTag2)

            # handle next;
            if (i  == splitLength - 1):
                nextWord1 = "^eos$"
                nextWord2 = "^eos$"
            else:
                nextTuple1 = line[i+1]
                nextWord1 = str(nextTuple1[0])
                nextWordTag1 = str(nextTuple1[1])
                nextWordClass1 = str(nextWordTag1)

                if (i == splitLength - 2):
                    nextWord2 = "^eos$"
                else:
                    nextTuple2 = line[i+2]
                    nextWord2 = str(nextTuple2[0])
                    nextWordTag2 = str(nextTuple2[1])
                    nextWordClass2 = str(nextWordTag2)


            # create outTagLine and write;
            # tagLine += " "+"prev2:"+prevWord2+" "+"prevClass2:"+prevClassLabel2+" "+"prev1:"+prevWord1+" "+"prevClass1:"+prevClassLabel1+" "+"curClass:"+curClassLabel +" "+"suffix2:"+suffix2+" "+"suffix3:"+suffix3+" " + "next1:"+nextWord1+" " +"nextClass1:"+nextWordClass1+" "+ "next2:"+nextWord2+" "+"nextClass2:"+nextWordClass2
            tagLine += " "+"prev2:"+prevWord2+" "+"prevClass2:"+prevClassLabel2+" "+"prev1:"+prevWord1+" "+"prevClass1:"+prevClassLabel1+" "+"next1:"+nextWord1+" " +"nextClass1:"+nextWordClass1+" "+ "next2:"+nextWord2+" "+"nextClass2:"+nextWordClass2

            outTagLine = curWord + tagLine
            outList.append(outTagLine)
            ou.write(outTagLine + "\n")

    # tr.close()
    ou.close()
    return outList


def readData():
    sentences = [ (sent)
                  for genre in brown.categories()
                  for sent in brown.tagged_sents(categories = genre)
    ]
    return sentences


def generateModel(formatFile,modelFile,megamPath):
    megamString = megamPath+" -nc multitron "+formatFile +" > "+modelFile
    p = subprocess.Popen(megamString,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0]


if __name__ == '__main__':

    train_out = "./hw3.train.brown.out"

    modelFile = sys.argv[1]
    megamPath = sys.argv[2]

    sentTagged = readData()
    trainList = format(train_out,sentTagged)
    generateModel(train_out,modelFile,megamPath)



