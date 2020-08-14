import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendConf(to):
    from_addr='victor@twk.com.mx'
    to_addr=['apuleyo3@gmail.com' , to]
    msg=MIMEMultipart()
    msg['From']=from_addr
    msg['To']=" ,".join(to_addr)
    msg['subject']='C1 Assessment'
    body='You have completed an assessment on our website'
    msg.attach(MIMEText(body,'plain'))
    #FILL WITH YOU OWN CREDENTIALS
    email='---------'
    password='-------'
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)
    text=msg.as_string()
    mail.sendmail(from_addr,to_addr,text)
    mail.quit()
