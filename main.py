import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import pyfiglet

SERVER = "smtp.gmail.com"
PORT = 587
FROM = "jakob.johnson.dev@gmail.com"
TO = "jakob.johnson.dev@gmail.com"
with open("passwd.txt", "r") as f:
    PASS = f.read().strip()

def extract_news(url: str) -> str:
    print("\33[0;49;93m[+] Extracting Hacker News stories...")
    stories = ""
    stories += "<b>HN Top Stories:</b>\n" + " <br>" + "-" * 49 + "<br>"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    for i, tag in enumerate(soup.find_all("td", attrs={"class": "title", "valign": ""})):
        stories += ((str(i + 1) + " :: " + tag.text + "\n" + "<br>")
                    if tag.text != "More" else "backup")
    return stories


def email(body: str) -> dict:
    now = datetime.datetime.now()
    print("\33[0;49;93m[+] Composing email...")
    msg = MIMEMultipart()
    msg["Subject"] = f"Top stories from HN - {str(now.day)}/{str(now.month)}/{str(now.year)}"
    msg["From"] = FROM
    msg["To"] = TO
    msg.attach(MIMEText(body, "html"))
    return msg
 

def send_email(msg: str) -> None:
    print("\33[0;49;93m[+] Initiating Server...")
    server = smtplib.SMTP(SERVER, PORT)
    server.ehlo()
    server.starttls()
    print("\33[0;49;93m[+] Enabled TLS...")
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    print("\33[0;49;93m[+] Sending Email...")
    server.quit()


if __name__ == "__main__":
    content = ""
    print("\33[0;49;31m" + pyfiglet.figlet_format("Hacker News Scraper...", font="5lineoblique"))
    print("\33[4;49;34m- Written by Jakob Johnson\n\n")

    latest_news = extract_news("https://news.ycombinator.com/")
    content += latest_news
    content += "<br>-------------<br>"
    content += "<br><br>End of message"
    msg = email(content)
    send_email(msg)

    print("\33[4;49;32m[*] All Done...\n\n")
