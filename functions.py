import json
import requests
import csv


def getPostInfo(postHash):
  
  payload = {"PostHashHex":postHash,"ReaderPublicKeyBase58Check":"BC1YLiU9Wpk8c7pVx7GCu8fae6AQhdUrGYcWc1Wz9V56HbCi7RPr887","FetchParents":False,"CommentOffset":0,"CommentLimit":1,"AddGlobalFeedBool":False}

  response = requests.post("https://bitclout.com/api/v0/get-single-post", json = payload)

  postFound = response.json()["PostFound"]
  posterKey = postFound["PosterPublicKeyBase58Check"]
  posterName = postFound["ProfileEntryResponse"]["Username"]
  postTimeStamp = round(postFound["TimestampNanos"] / 1000000000)
  payload = {"PostHashHex":postHash,"ReaderPublicKeyBase58Check":posterKey,"FetchParents":False,"CommentOffset":0,"CommentLimit":5000,"AddGlobalFeedBool":False}

  response = requests.post("https://bitclout.com/api/v0/get-single-post", json = payload)
  postFound = response.json()["PostFound"]
  originalPost = postFound["Body"]
  


  comments = postFound["Comments"]
  
  replies = { 
  "commentList": []
  }

  replyList = [{"Post": originalPost,"Username":posterName,"Diamonds received from post author": 0,
    "PosterPublicKeyBase58Check": posterKey, "PostHashHex":postHash, "TimeStamp": postTimeStamp}]
  for comment in comments:

    replyHash = comment["PostHashHex"]
    replierKey = comment["PosterPublicKeyBase58Check"]
    replyBody = comment["Body"]
    name = comment["ProfileEntryResponse"]["Username"]
    diamondReceivedFromAuthor = comment["PostEntryReaderState"]["DiamondLevelBestowed"]
    postTimeStamp = round(comment["TimestampNanos"] / 1000000000)

    replyList.append({"Post":replyBody,
    "Username": name, "Diamonds received from post author": diamondReceivedFromAuthor,
    "PosterPublicKeyBase58Check": replierKey, "PostHashHex":replyHash, "TimeStamp": postTimeStamp
   
    })
  
  replies["commentList"] = replyList
  with open("sumarisedComments.json","w") as file:
    json.dump(replies, file)
    file.close()


def createCSV(jsonFileToOpen, csvFileToSave):
  with open(jsonFileToOpen, "r") as json_file:
    data = json.load(json_file)
 
    commentData = data['commentList']
    # now we will open a file for writing
    data_file = open(csvFileToSave, 'w')
 
    # create the csv writer object
    csv_writer = csv.writer(data_file)
 
    # Counter variable used for writing
    # headers to the CSV file
    count = 0
 
    for comment in commentData:
      if count == 0:
 
        # Writing headers of CSV file
        header = comment.keys()
        csv_writer.writerow(header)
        count += 1
 
    # Writing data of CSV file
      csv_writer.writerow(comment.values())

  data_file.close()
  json_file.close()

  


