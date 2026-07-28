import smtplib
import ssl

context = ssl.create_default_context()

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls(context=context)
print("TLS connection successful!")
server.quit()