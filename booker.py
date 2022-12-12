from lxml import etree
from PIL import Image
from io import BytesIO, StringIO
from threading import Thread
import pytesseract
import os
import numpy
import re
import requests
import random
import time

apt_dates = {
    "2021-05-25",
}
# apt_dates = {
#     "2021-05-20",
#     "2021-05-21",
# }
apt_times = {
    ("08:30 - 08:45", "1"),
    ("08:45 - 09:00", "2"),
    ("09:00 - 09:15", "3"),
    ("09:15 - 09:30", "4"),
    ("09:30 - 09:45", "5"),
    ("09:45 - 10:00", "6"),
    ("10:00 - 10:15", "7"),
    ("10:15 - 10:30", "8"),
}

name = "Rajesh Vohra"
passport = "576313368x"
email = "rajesh.s.vohra@gmail.com"
telephone = "07850121333"
location_id = 4 # Hounslow
service_id = 9 # OCI
number_of_threads = 10

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Origin": "https://www.hcilondon.gov.in",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.hcilondon.gov.in/appointment.php",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.",
}

def run():
    while True:
        try:
            session = requests.Session()

            base_url = "https://www.hcilondon.gov.in"
            url = f"{base_url}/appointment.php"
            page = session.get(url)

            htmlparser = etree.HTMLParser()

            html = page.content.decode("utf-8")

            tree = etree.parse(StringIO(html), htmlparser)

            captcha_img_path = tree.xpath('//img[@alt="Enter Verification code"]')[0].get("src")
            captcha_img_url = f"{base_url}/{captcha_img_path}"
            captcha_img_bytes = BytesIO(session.get(captcha_img_url).content)
            captcha_img = Image.open(captcha_img_bytes)
            captcha_img.save("captcha.jpg")
            captcha_text = pytesseract.image_to_string(captcha_img)

            regex = re.compile(r'\d{4}')
            captcha_code = regex.match(captcha_text)
            if captcha_code:
                captcha_code = captcha_code[0]
            else:
                continue

            csrf_token = tree.xpath('//input[@name="csrf_token"]')[0].get("value")
            apt_type = "Submission"
            apt_date = random.sample(apt_dates, 1)[0]
            apt_time_selection = random.sample(apt_times, 1)[0]
            apt_time = apt_time_selection[0]
            apt_time_value = apt_time_selection[1]

            payload = {
                "csrf_token": csrf_token,
                "apttype": apt_type,
                "locationid": location_id,
                "serviceid": service_id,
                "aptdate": apt_date,
                "apttime": apt_time,
                "apttimevalue": apt_time_value,
                "name": name,
                "passport": passport,
                "email": email,
                "telephone": telephone,
                "name1": "Kabeer Vohra",
                "passport1": "530055071x",
                "name2": "",
                "passport2": "",
                "verif_box": captcha_code,
            }

            print(payload)

            post_url = f"{base_url}/appointment_inter.php"
            result = session.post(post_url, data=payload)

            with open("response.html", "wb") as h:
                h.write(result.content)

            if b"has been exceeded. Please change the date and try again." not in result.content and b"No verification code entered" not in result.content and b"The data is incomplete" not in result.content:
                print("SUCCESS")
                os._exit(1)

        except Exception:
            continue

for x in range(number_of_threads):
    Thread(target = run).start()
    time.sleep(1)
