import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comment):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = "7d46120f2b7d00"
    password = "a9866f39b60160"
    message = f"""<h3> New Feedback Submitted </h3>
<ul>
    <li>Customer: {customer}</li>
    <li>Dealer: {dealer}</li>
    <li>Rating: {rating}</li>
    <li>Comments: {comment}</li>
</ul>"""

    sender_email = "from@example.com"
    receiver = "armaanbhatti972@gmail.com"

    msg = MIMEText(message, 'html') # text or html
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['to'] = receiver

    # Send
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver, msg.as_string())
