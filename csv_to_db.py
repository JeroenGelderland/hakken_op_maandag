import csv
import database
db = database.Database()

with open('data.csv', newline='') as csvfile:
    query_list = []

    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if not row:
            continue
        else:
            if(row[0] != "src"):       
                db.execute(f"INSERT INTO `marktplaats_images` VALUES(\"{row[0]}\",\"{row[1]}\", \"{row[2]}\", \"{row[3]}\", \"{row[4]}\")")

    

