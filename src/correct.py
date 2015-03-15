import sys,nltk,subprocess
from nltk import compat

def getSuffix(word,type):
    wlen = len(word)
    return word[wlen-type:wlen]

def formatInput(inFile,outFile,mSet):
    outList = []
    predList = []
    ou = open(outFile,'w')
    tr = open(inFile,'r')
    for line in tr:
        print(".")
        # create tags;
        # toTagLine = nltk.word_tokenize(line)
        # tagList = nltk.pos_tag(toTagLine)
        if(line == "\n"):
            continue

        splitLine = line.split()
        tagList = nltk.pos_tag(splitLine)

        splitLineSet = set()
        for item in splitLine:
            splitLineSet.add(str(item.lower()))

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
            continue

        splitLength = len(splitLine)
        prevWord1 = "^bos$"
        prevWord2 = "^bos$"
        prevClassLabel1 = "^cla$$"
        prevClassLabel2 = "^cla$$"
        nextWordClass1 = "^cla$$"
        nextWordClass2 = "^cla$$"
        curWord = ""
        nextWord = ""
        curClassLabel = ""
        suffix2 = ""
        suffix3 = ""
        reconLine = ""

        for i in range(splitLength):
            tagLine = ""
            outTagLine = ""
            if str(splitLine[i]) not in mSet:
                continue

            # handle cur word;
            curWord = str(splitLine[i])
            suffix2 = getSuffix(curWord,2)
            suffix3 = getSuffix(curWord,3)
            curWordTag = tagList[i]
            curClassLabel = str(curWordTag[1])

            #handle prev word;
            if(i == 0):
                prevWord1 = "^bos$"
                prevWord2 = "^bos$"

            else:
                prevWord1 = splitLine[i-1]
                prevWordTag1 = tagList[i-1]
                prevClassLabel1 = str(prevWordTag1[1])
                if (i == 1):
                    prevWord2 = "^bos$"
                else:
                    prevWord2 = splitLine[i-2]
                    prevWordTag2 = tagList[i-2]
                    prevClassLabel2 = str(prevWordTag2[1])

            # handle next;
            if (i  == splitLength - 1):
                nextWord1 = "^eos$"
                nextWord2 = "^eos$"
            else:
                nextWord1 = str(splitLine[i+1])
                nextWordTag1 = tagList[i+1]
                nextWordClass1 = str(nextWordTag1[1])
                if (i == splitLength - 2):
                    nextWord2 = "^eos$"
                else:
                    nextWordTag2 = tagList[i+1]
                    nextWordClass2 = str(nextWordTag2[1])
                    nextWord2 = str(splitLine[i+2])

            # create outTagLine and write;
            # tagLine += " "+"prev2:"+prevWord2+" "+"prevClass2:"+prevClassLabel2+" "+"prev1:"+prevWord1+" "+"prevClass1:"+prevClassLabel1+" "+"curClass:"+curClassLabel +" "+"suffix2:"+suffix2+" "+"suffix3:"+suffix3+" " + "next1:"+nextWord1+" " +"nextClass1:"+nextWordClass1+" "+ "next2:"+nextWord2+" "+"nextClass2:"+nextWordClass2
            tagLine += " "+"prev2:"+prevWord2+" "+"prevClass2:"+prevClassLabel2+" "+"prev1:"+prevWord1+" "+"prevClass1:"+prevClassLabel1+" "+"next1:"+nextWord1+" " +"nextClass1:"+nextWordClass1+" "+ "next2:"+nextWord2+" "+"nextClass2:"+nextWordClass2

            outTagLine = "test" + tagLine
            outList.append(curWord)
            ou.write(outTagLine + "\n")

    tr.close()
    ou.close()
    return outList


def getMegamPrediction(modelFile,formatFile,megamPath):
    # print("megam")
    megamString = megamPath+" -nc -maxi 10 -predict " + modelFile + " multitron " + formatFile
    (stdout,stderr) = subprocess.Popen(megamString,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()
    print(stderr)
    if isinstance(stdout, compat.string_types):
        return stdout
    else:
        return stdout.decode('utf-8')


def reconstructOutput(smout,tFile,mSet):
    # predOut = open("./predErr.txt",'w')
    predTagList = []
    reconList = smout.split("\n")
    # print(reconList[0])
    for reconLine in reconList:
        predTag = reconLine.split("\t")[0]
        predTagList.append(str(predTag))
        # predOut.write(str(predTag) + "\n")
    # predOut.close()


    trList = []
    trf = open(tFile,'r')
    for line in trf:
        trList.append(line)
    trf.close()

    c = 0
    for trLine in trList:
        outLine = ""
        stripLine = trLine.strip("\n")
        trainWords = stripLine.split()
        # iterate words in the list;
        for w in range(len(trainWords)):
            if str(trainWords[w]) in mSet:
                outLine += (" " + predTagList[c])
                c += 1
            else:
                outLine += (" " + trainWords[w])
        print(outLine)
    
    return predTagList


def initSet():
    mainSet = set()
    mainSet.add("its")
    mainSet.add("it\'s")
    mainSet.add("they\'re")
    mainSet.add("their")
    mainSet.add("your")
    mainSet.add("you\'re")
    mainSet.add("too")
    mainSet.add("to")
    mainSet.add("lose")
    mainSet.add("loose")
    return mainSet



if __name__ == '__main__':

    # megamPath = "./megam_0.92/./megam"
    modelFile = sys.argv[1]
    testFile = sys.argv[2]
    megamPath = sys.argv[3]


    testFileFormat = "./hw3.test.format.txt"
    # devFormat = "./hw3.dev.format.txt"

    mainSet = initSet()

    testList = formatInput(testFile,testFileFormat,mainSet)
    mOut = getMegamPrediction(modelFile,testFileFormat,megamPath)
    predList = reconstructOutput(mOut,testFile,mainSet)

    # cc = 0
    # correct = 0
    # incorrect = 0

    # devList = []
    # drf = open(devFormat,'r')
    # devOut = open("./devTags.txt",'w')
    # for dline in drf:
    #     dTag = str(dline.split()[0])
    #     devList.append(dTag)
    #     devOut.write(dTag + "\n")
    # drf.close()
    # devOut.close()

    # if len(predList) != len(testList):
    #     print("HAHAHA=============")


    # if len(predList) != len(devList):
    #     print("PRED: " +str(len(predList)))
    #     print("DEV: " +str(len(devList)))
    #     print("HAHAHA")

    # for i in range(len(devList)):
    #     if predList[i] == devList[i]:
    #         correct += 1
    #     else:
    #         incorrect += 1

    # accuracy = correct / (correct + incorrect)
    # print(str(correct))
    # print(str(incorrect))
    # print(str(accuracy))