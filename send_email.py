import smtplib


def send_email(subject, msg, sendto):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('nanyamshukla@gmail.com','nanaezakmins')
        message = 'Subject :{} \n\n {}'.format(subject, msg)
        server.sendmail('nanyamshukla@gmail.com', sendto, message)
        server.quit()
        print("\nSuccess: Email sent\n")
    except:
        print("\nFailure: Email not sent\n")

subject = "Your Query Status"


#send_email(subject, msg)