import smtplib
import json


class Email:
    def __init__(self):
        """Initializes parameters from json file in login/email_account.json"""
        json_file = open("login/email_account.json")
        settings = json.load(json_file)
        self.smtp_server_domain_name = settings["smtp_server_address"]
        self.port = settings["port"]
        self.user = settings["user"]
        self.password = settings["password"]

    def send_message(self, recipient, subject, message):
        server = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port)
        server.login(self.user, self.password)
        server.sendmail(self.user, recipient, f"Subject: {subject}\n{message}")
        server.quit()
