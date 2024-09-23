
import csv
from bs4 import BeautifulSoup
import requests
import array
def Match_Name(String,First_Name,Last_Name):
    number=0
    for i in First_Name:
        if(First_Name[number]!=String[number]):
            return False
    number=number+1
    number=0
    for i in Last_Name:
        if(Last_Name[number]!=String[len(String)-len(Last_Name)+number]):
            return False
    number=number+1
    return True
def Find_Rank(Link_Name):
    space1=0
    space2=0
    for i in len(Link_Name):
        if Link_Name[i]==' ':
            space1=space2
            space2=i
    return Link_Name[space1:space2]
def Place():#count how many are above this

    return
       
#///////////////////////////////////////START//////////////////////////////////////////////////
First_Name="Benjamin"
Last_Name="Haut"
#Make the CSV and add the headers
fileName=First_Name+"-"+Last_Name+" Dance Competition Summary"
CSV_File=open(fileName,"a",newline="")
writer=csv.writer(CSV_File)
Payload=("URL","Competion","Group","Rank","Table Name","Round","Couple Number","Place","Number of Participlants")
writer.writerow(Payload)
#Go to the individual Page with each of the 
Payload={"szFirst": First_Name,"szLast": Last_Name,"DoSearch":"Search"}
url="https://results.o2cm.com//individual.asp"
Comment_Line="go to site and get individual answers"
print(requests.post(url,data=Payload).text)
#directly below is what we will use for all atheletes
#Links=BeautifulSoup(requests.post(url,data=Payload).text,"html.parser").findAll("a")
Links=BeautifulSoup(requests.get("https://results.o2cm.com/individual.asp?szLast=Haut&szFirst=Benjamin%20").text,"html.parser").findAll("a")
print(Links)
percentile=array.array('i',[0,0,0,0,0])#we need to find the place and add up all the percentiles
#I dont think we can find the list on the path and we have to save them for each link
print(Links)
print("-------------------------------------")
#go through each link
for link in Links:
    table_Name=link.text#event name and place
    url=link.get("href")
    #Competition=Find_Rank(link)
    r=BeautifulSoup(requests.get(url).text,"html.parser")
    Doc=r.find("select")
    #find the first round
    if(Doc==None):
        Rounds=1
    else:
        Doc=Doc.findAll("option")
        Rounds=len(Doc)
    Doc=r.findAll("td")
    Tables=r.findAll("table")
    #remove everything but the first line
    Competition=Doc[0].text[0:Doc[0].text.find('\n')-1]
    Group=Doc[0].text[0:Doc[0].text.find('\n')-1]
    #get the couple number
    print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,GETTING,STARTED,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    event=url[url.find("=")+1:url.find('&')]
    heatid=url[url.find('&')+8:len(url)]
    index_j=1
    for j in range(1,Rounds+1,1):#this goes through each heat in the event
        print("round j")
        index_j=index_j+1
        percentile=[0,0,0,0,0]#new round new record of marks
        index_i=0
        for i in range(1,len(Tables)-2,1):#test to see if we need to search for a table instead of just going straight to the second/third
            index_i=index_i+1
            # this was wrong and it got the entire event nametable_Name=Tables[index_i].find("td").text
            Doc=r.findAll("a")
            number=0
            for i in Doc:
                if(Match_Name(Doc[number].text,First_Name,Last_Name)):
                    break
                number=number+1
            #we found the couple number location in list
            if(number==len(Doc)):
                #nothing happens print out
                Payload=(url,Competition,Group,table_Name,j,"Couple did not participate in this round","N/A","N/A")
                writer.writerow(Payload)
            else:
                couple_Number=Doc[number].parent.parent.contents[0].text
                print(couple_Number)
                #we gotta find what place they were in
                Doc=r.findAll("table")
                Doc=Doc[index_i].findAll("tr")
                number=0
                for i in Doc:
                    print(Doc[number].text[0:len(couple_Number)])#len is couple number because it varies in size
                    print("------------------------")
                    print(number)
                    if(j>1):#not in the final heat
                        #add values
                        Doc.findall("tr")
                        percentile[Doc[len(Doc)-2].text-1]=percentile[Doc[len(Doc)-2].text-1]+1
                        #add new record into scale
                    if(Doc[number].text[0:len(couple_Number)]==couple_Number):
                        #number will always be 2 greater than the real value, because we include the titles in our calculation
                        #print("if resurlt "+str(Doc[1].text.find("P")==None)
                        if(Doc[1].text.find("P")==None or Doc[1].text.find("P")<0):
                            #we have no place so we go to the order as the place
                            print("this one")
                            print(number-1)
                            number=str(number-1)
                        else:
                            #we have a Finals table with the actual place in here
                            Postion=len(Doc[number].findAll("td"))-2+(table_Name=="Summary")#edge case: summary tables don't have an extra whitespace at the end.
                            print(Doc[number].findAll("td")[Postion].text)
                            number=Doc[number].findAll("td")[Postion].text
                        print(" out of ")
                        print(len(Doc)-2)
                        break
                    number=number+1
                Payload=Payload=(url,Competition,Group,table_Name,j,couple_Number,number,len(Doc)-2)
                writer.writerow(Payload)
            #prepare next request data
            print("Next Page.................................................")
        if(index_j>1):
            print(str(j-1))
            SelectCell=str(index_j-1)
            Payload={"heatid": heatid,"event": event,"selCount":SelectCell}
            r=BeautifulSoup(requests.post("https://results.o2cm.com/scoresheet3.asp",data=Payload).text,"html.parser")
CSV_File.close()