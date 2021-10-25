# !!!!! BEFORE RUNNING THIS PROGRAM PLS GO TO CONFIG.PY FILE AND CHANGE THE EMAIL AND PASSWORD TO YOUR EMAIL AND PASSWORD !!!!
import requests
from bs4 import BeautifulSoup
import smtplib
from config import your_email, your_password


# Paste the product link that you want to keep track of
url = input(
    "********** Please paste the product link that you want to keep track of **********\n")

# put here your budget to buy the product
minimum_amount_to_buy_the_product = float(
    input("**************** Enter the budget of the product ****************\n"))

# ! put your user agent here :- search in google -> my user agent and copy that highlighted text and paste it here
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'From': your_email}


def check_price():
    # we will use headers here so that amazon does not block us

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    # getting the product title from amazon and removing the white spaces through strip() method
    global title
    title = soup.find(id="productTitle").get_text()
    title_stripped = title.strip()

    # getting the product price and removing the comma in the price -> ","
    # ! this id -> priceblock_dealprice is changed everyday to a different id by amazon so that no one can scrap their website
    # ! so before running this program, pls check that this id is correct or not
    price_string = soup.find(id="priceblock_dealprice").get_text()

    actual_price = ""

    # checking if the price has comma or not
    if "," in price_string:

        # splitting the price_string by ","
        p_splitted = price_string.split(",")

        # output -> ['₹1', '999.00'] so we need the first and the last element

        temp_price = f"{p_splitted[0]}{p_splitted[1]}"
        # output -> ₹1999.00 <- now we have to remove the "₹" symbol

        # -> ["₹","1999.00"] so we are taking the second element here and converting it into a floating point
        actual_price = float(temp_price.split("₹")[1])

    else:
        actual_price = float(price_string.split("₹")[1])

        # conditions
        # if the product price is less than the minimum amount then our program should automatically send an email to the user
    if actual_price <= minimum_amount_to_buy_the_product:
        send_email()


def send_email():
    try:

        # SMTP => Simple Mail Transfer Protocol
        # creates a secure SMTP_SSL session
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        # You have to login with your account in order to send a mail
        smtp.login(your_email, your_password)

        # sending the mail
        # here the receiver email is my email address so that when the price goes down this will send me a mail
        Subject = f"!!!!!!! Your product -> {title}'s price is down in amazon !!!!!!"

        Message = f'Subject: {Subject}\n\n Checkout here -> {url}'

        # sending the mail
        smtp.sendmail(your_email, your_email, Message)

        splitted_receiver_email_id = your_email.split('@')

        # it will only print the name on the email_address
        print(
            f"Messsage sent Successfully to {splitted_receiver_email_id[0]} ")

        # terminating the session
        smtp.quit()

    except:
        print("Something went wrong in sending the mail!")


check_price()
