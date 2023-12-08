import requests
from bs4 import BeautifulSoup
import mysql.connector


mydb = mysql.connector.connect(
host="0.0.0.0",
user="db_user",
password="db_password",
database="db_name")
mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS rangliste")
mycursor.execute("CREATE TABLE rangliste (rank INT, team VARCHAR(255), members VARCHAR(255), points VARCHAR(255), games VARCHAR(255), games2 VARCHAR(255), sets VARCHAR(255), sets2 VARCHAR(255))")

url = "https://dsab-vfs.de/VFSProject/WebObjects/VFSProject.woa/wa/rangListen?liga=6022&typ=teamrang&saison=3492"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("table", class_="list")
rows = table.find_all("tr")[1:]

for row in rows:
    cols = row.find_all("td")
    rank = cols[0].text
    team = cols[1].text.strip()
    members = cols[3].text.strip()
    points = cols[4].text.strip()
    games = cols[5].text.strip()
    games2 = cols[7].text.strip()
    sets = cols[8].text.strip()
    sets2 = cols[10].text.strip()

    sql = "INSERT INTO rangliste (rank, team, members, points, games, games2, sets, sets2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (rank, team, members, points, games, games2, sets, sets2)
    mycursor.execute(sql, val)


mydb.commit()
mydb.close()
