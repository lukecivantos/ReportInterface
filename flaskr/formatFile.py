import shutil
import io

def createFile(card, fileDate, file):
    fileDate = fileDate.split("-")
    year,month,day = fileDate
    name = "flaskr/uploads/" + card + "-" + day + "-" + month + "-" + year + ".xls"
    shutil.copy2('flaskr/uploads/template.txt', name)

    a = open(name, 'a')
    text = file.read()
    text = text.decode('ascii')
    lines = text.split('\r\n')
    words = [None]*len(lines)
    counter = 0
    for line in lines:
        words[counter] = line.split("\t")
        counter += 1

    for line in words:
        if len(line) > 1:
            if words.index(line) == 0:
                a.write("Account\t")
            elif line[8] == "HPT 170: Intermission Impossible":
                if int(float(line[9])) % 32 == 0:
                    a.write("BOS WD\t")
                elif int(float(line[9])) % 42 == 0:
                    a.write("BOS WE\t")
                else:
                    a.write("group/donation\t")
            elif line[8] == "Alumni Dinner 2018":
                if int(float(line[9])) == 35:
                    a.write("ALUMNI DIN\t")
                else:
                    a.write("probably dinner with donation?\t")
            elif line[8] == "HPT 170: Man of the Year":
                a.write("MOY\t")
            elif line[8] == "HPT 170: Woman of the Year":
                a.write("WOY\t")
            elif line[8] == "HPT 170 Donors":
                if int(float(line[9])) >= 2500 and int(float(line[9])) < 5000:
                    a.write("FR BFS\t")
                elif int(float(line[9])) >= 1000 and int(float(line[9])) < 2500:
                    a.write("PATRON\t")
                elif int(float(line[9])) >= 500 and int(float(line[9])) < 1000:
                    a.write("FR BEN\t")
                elif int(float(line[9])) >= 250 and int(float(line[9])) < 500:
                    if int(float(line[9])) == 280:
                        a.write("Probably FR Kickline\t")
                    else:
                        a.write("FR SUP\t")
                elif int(float(line[9])) >= 125 and int(float(line[9])) < 250:
                    if int(float(line[9])) == 125:
                        a.write("FR PAT or BOWS\t")
                    else:
                        a.write("FR PAT\t")
            elif line[8] == "HPT 170 Alumni Memberships":
                if int(float(line[9])) == 280:
                    a.write("FR Kickline\t")
                elif int(float(line[9])) >= 125:
                    a.write("FR PAT\t")
                else:
                    a.write("group/donation\t")
            else:
                a.write("group/donation\t")
            a.write(line[4] + "\t")
            a.write(line[9] + "\t")
            a.write(line[13] + "\t")
            a.write(line[14] + "\r\n")

    a.close()
"""
w = file
x = card
y = raw_input("Whats the day?\n")
z = raw_input("Whats the month?\n")

w_words = w.split("/")
w2 = w_words[3] + "/" + w_words[4]
w2 = w2[:-1]



name = "Desktop/" + x + "-" + y + "-" + z + "-2018.xls"

shutil.copy2('template.txt', name)

a = open(name, 'a')
b = open(w2, 'r')

text = b.read()
lines = text.split("\r\n")
words = [None]*len(lines)
counter = 0
for line in lines:
    words[counter] = line.split("\t")
    counter += 1

for line in words:
    if len(line) > 1:
        if words.index(line) == 0:
            a.write("Account\t")
        elif line[8] == "HPT 170: Intermission Impossible":
            if int(float(line[9])) % 32 == 0:
                a.write("BOS WD\t")
            elif int(float(line[9])) % 42 == 0:
                a.write("BOS WE\t")
            else:
                a.write("group/donation\t")
        elif line[8] == "Alumni Dinner 2018":
            if int(float(line[9])) == 35:
                a.write("ALUMNI DIN\t")
            else:
                a.write("probably dinner with donation?\t")
        elif line[8] == "HPT 170: Man of the Year":
            a.write("MOY\t")
        elif line[8] == "HPT 170: Woman of the Year":
            a.write("WOY\t")
        elif line[8] == "HPT 170 Donors":
            if int(float(line[9])) >= 2500 and int(float(line[9])) < 5000:
                a.write("FR BFS\t")
            elif int(float(line[9])) >= 1000 and int(float(line[9])) < 2500:
                a.write("PATRON\t")
            elif int(float(line[9])) >= 500 and int(float(line[9])) < 1000:
                a.write("FR BEN\t")
            elif int(float(line[9])) >= 250 and int(float(line[9])) < 500:
                if int(float(line[9])) == 280:
                    a.write("Probably FR Kickline\t")
                else:
                    a.write("FR SUP\t")
            elif int(float(line[9])) >= 125 and int(float(line[9])) < 250:
                if int(float(line[9])) == 125:
                    a.write("FR PAT or BOWS\t")
                else:
                    a.write("FR PAT\t")
        elif line[8] == "HPT 170 Alumni Memberships":
            if int(float(line[9])) == 280:
                a.write("FR Kickline\t")
            elif int(float(line[9])) >= 125:
                a.write("FR PAT\t")
            else:
                a.write("group/donation\t")
        else:
            a.write("group/donation\t")
        a.write(line[4] + "\t")
        a.write(line[9] + "\t")
        a.write(line[13] + "\t")
        a.write(line[14] + "\r\n")

a.close()
b.close()
"""
