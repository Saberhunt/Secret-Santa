import copy
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

''' Edit this with the people participating and their respective email.
Make sure the emails correspond to the order in which the names are entered '''
names = ['']
emails = ['']
pricelimit = '$50'


# Function to assign pairs
def secret_santa(names):
    my_list = names
    choose = copy.copy(my_list)
    result = []
    for i in my_list:
        names = copy.copy(my_list)
        names.pop(names.index(i))
        chosen = random.choice(list(set(choose)&set(names)))
        result.append((i,chosen))
        choose.pop(choose.index(chosen))
    return result

ss_result = secret_santa(names)
final = zip(ss_result,emails)



''' Generic setup for the email
Sends a message to each recepient with who they drew and the specified price limit '''
for x in final:
    fromAdd = " " # Enter the email address you want to send from here
    toAdd = x[1]
    msg = MIMEMultipart()
    msg['From'] = fromAdd
    msg['To'] = toAdd
    msg['Subject'] = "SECRET EMAIL FOR SECRET SANTA!"
 
    body1 = "Hey, "+str(x[0][0])
    body2 = '''!\n This is an automated email from the Secret Santa Program!\n\nYou drew\n.......\n........\n........\n'''+str(x[0][1])+"!!\n\nRule Number 1: Please do not tell anyone!\n"
    body3 = "Rule Number 2: The budget is " + pricelimit + "! \nWhat are you waiting for? Go ahead and get something nice for "+str(x[0][1])+"!\n\n\n"
    body = body1 + body2 + body3
    msg.attach(MIMEText(body, 'plain'))
    
    # Attaches the specified image to the end of the email
    filename = "SecretSanta.jpg"
    attachment = open("SecretSanta.jpg", "rb")
 

    # Opens connection to server
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 

    # Attempts to send email
    server = smtplib.SMTP('smtp.gmail.com', 587) # Defaulted to gmail server, if you use a different email address, you will have to find the SMTP server for it
    server.starttls()
    server.login(fromAdd, " ") # INSERT YOUR EMAIL PASSWORD HERE
    text = msg.as_string()
    server.sendmail(fromAdd, toAdd, text)
    server.quit()
    print ("mail sent to", x[1]) # Confirmation message