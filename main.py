from functions import *
from operator import getitem

arg = input("Input post link: ")

postIndex = arg.find("posts")
postHash = arg[postIndex+ 6: postIndex + 70]


getPostInfo(postHash)
createCSV("sumarisedComments.json", "UnsortedComments.csv")

arg = int(input("How you want to sort it? \n1. Based on Diamonds author gave\n\n2. Based on timestamp\n\nInput 1 or 2: "))



file = open("sumarisedComments.json", "r")
commentDict = json.load(file)
file.close()

if arg == 1:
    count = 0
    testDict = {}
    for comment in commentDict["commentList"]:
        testDict[count] = comment
        count = count + 1

   
    marklist = sorted(testDict.items(), key=lambda x:getitem(x[1], 'Diamonds received from post author'), reverse=False)
    sortedStats = dict(marklist)

    commentList = []
    for num in sortedStats:
        commentList.append(sortedStats[num])
    
    sortByDiamond = {"commentList": commentList}
    file = open("SortedByDiamond.json", "w")
    json.dump(sortByDiamond, file)
    file.close()

    createCSV("SortedByDiamond.json", "SortedByDiamond.csv")
    print("Done!")
if arg == 2:
    count = 0
    testDict = {}
    for comment in commentDict["commentList"]:
        testDict[count] = comment
        count = count + 1

   
    marklist = sorted(testDict.items(), key=lambda x:getitem(x[1], 'TimeStamp'), reverse=False)
    sortedStats = dict(marklist)

    commentList = []
    for num in sortedStats:
        commentList.append(sortedStats[num])
    
    sortByTimeStamp = {"commentList": commentList}
    file = open("SortByTimeStamp.json", "w")
    json.dump(sortByTimeStamp, file)
    file.close()

    createCSV("SortByTimeStamp.json", "SortedByTimeStamp.csv")
    print("Done!")




        