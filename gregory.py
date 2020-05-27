import pyodbc
import requests

#Gegevens om te connecteren met de SQL Server
server = '10.1.20.46'
database = 'Telraam'

#Vul username en password in !!
username = ' '
password = ' '

#Connectie met de SQL server
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

#Aanmaken van de cursor
cursor = cnxn.cursor()

#lijst die we bijhouden waar alle segmenten (arrays) worden in opgeslagen
listSegments = []

#Methode die de segmenten van de API van telramen ophaalt
def retrievedata():
    #Get request sturen
    r = requests.get('https://telraam-api.net/v0/segments/active')
    j = r.json()

    global listSegments
    listSegments = []

    #Verdiepen in het features element
    for segment in j["features"]:
        #Benodigde gegevens opslaan in een variabele
        seg = []
        id = segment["properties"]["id"]
        speed = segment["properties"]["speed"]
        pedestrian = segment["properties"]["pedestrian"]
        bike = segment["properties"]["bike"]
        car = segment["properties"]["car"]
        lorry = segment["properties"]["lorry"]

        #Variabeles toevoegen aan een array
        seg.append(id)
        seg.append(speed)
        seg.append(pedestrian)
        seg.append(bike)
        seg.append(car)
        seg.append(lorry)

        #segment toevoegen aan de lijst van segmenten
        listSegments.append(seg)

#Methode uitvoeren
retrievedata()


#Voor segment in de lijst van segmenten...
for item in listSegments:

    #List comprehension die alle None values omzet in 0
    item = [0 if v is None else v for v in item]

    print("Appending following line: ")
    print("ID: " + str(item[0]) + " Speed: " + str(item[1]) + " Pedestrians: " + str(item[2]) + " Bikes: " + str(item[3]) + " Cars: " + str(item[4]) + " Lorries: " + str(item[5]))

    #Toevoegen aan de database
    cursor.execute('INSERT INTO Telraam.dbo.telraam_segments (id, speed, pedestrian, bike, car, lorry) VALUES(%s, %s, %s, %s, %s, %s)' %
                   (int(item[0]), int(item[1]), int(item[2]), int(item[3]), int(item[4]),int(item[5])))

    print("Committing to SQL server")
    #Committing...
    cnxn.commit()