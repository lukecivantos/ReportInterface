import shutil
import io

def createFile(card, fileDate, file):
    fileDate = fileDate.split("-")
    year,month,day = fileDate
    name = "app/static/uploads/" + card + "-" + day + "-" + month + "-" + year + ".xls"
    shutil.copy2('app/static/uploads/template.txt', name)


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
            elif line[8] == "HPT 171":
                if int(float(line[9])) % 32 == 0:
                    a.write("BOS WD\t")
                elif int(float(line[9])) % 42 == 0:
                    a.write("BOS WE\t")
                else:
                    a.write("This is a Cambridge ticket, either the customer purchased a program or donated on top of the purchase.\t")
            elif line[8] == "Alumni Dinner 2019":
                if int(float(line[9])) == 35:
                    a.write("ALUMNI DIN\t")
                else:
                    a.write("Alumni probably purchased dinner and added a donation?\t")
            elif line[8] == "HPT 171 Man of the Year":
                a.write("MOY\t") #250
            elif line[8] == "HPT 171 Woman of the Year":
                a.write("WOY\t") #100
            elif line[8] == "Membership":
                if int(float(line[9])) >= 2500 and int(float(line[9])) < 5000:
                    a.write("FR BFS\t")
                elif int(float(line[9])) >= 1000 and int(float(line[9])) < 2500:
                    a.write("PATRON\t")
                elif int(float(line[9])) >= 600 and int(float(line[9])) < 1000:
                    a.write("FR BEN\t")
                elif int(float(line[9])) >= 400 and int(float(line[9])) < 600:
                    a.write("FR SUP\t")
                elif int(float(line[9])) >= 200 and int(float(line[9])) < 400:
                    if int(float(line[9])) == 300:
                        a.write("LIKELY KICKLINE - COULD BE FRIEND - CHECK VENDINI\t")
                    else: 
                        a.write("FR FRIEND\t")
                elif int(float(line[9])) >= 200:
                    a.write("FR PAT\t")
                elif int(float(line[9])) == 60: 
                    a.write("FR TORCH\t")
                else:
                    a.write("UNKOWN: CHECK VENDINI\t")
            else:
                a.write("This is a catch all. I don't know what they purchased and they likely were a group sale (with discount) or purchased a ticket and donated on top of it. \t")
            a.write(line[4] + "\t")
            a.write(line[9] + "\t")
            a.write(line[13] + "\t")
            a.write(line[14] + "\r\n")

    a.close()
    return name
