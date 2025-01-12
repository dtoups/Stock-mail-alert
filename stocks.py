import datetime
import time

import smtplib

import stocks_object
import credentials

STOCKS_TO_WATCH = ["AAPL", "AMD", "INTC", "VNA.DE", "MBG.DE", "F", "KO"]


def mail_alert(message):
    # Building connection
    conn = smtplib.SMTP(credentials.SERVER, credentials.SERVER_PORT)
    conn.starttls()
    conn.login(user=credentials.MY_EMAIL, password=credentials.PW)
    # Send mail
    conn.sendmail(from_addr=credentials.MY_EMAIL, to_addrs=credentials.RECIPIENT_MAIL, msg=message)
    # Close connection
    conn.close()


def tracking_main(stocks):
    stock_list  = [stocks_object.StockObject(stock) for stock in stocks]
    day         = datetime.date.today()

    while True:
        print(f"\n{datetime.datetime.now()}")

        for stock in stock_list:
            if not stock.ignore:
                # Tracking
                tmp = track_single(stock)

                # A return value means there has been a major shift in price so a mail was already sent.
                # Tracking for that stock will be paused until the next day
                if tmp is not None:
                    stock.ignore()

        # When a new day starts, reset all sleep-flags to False
        if datetime.date.today() != day:
            day = datetime.date.today()
            for stock in stock_list:
                stock.new_day()
        time.sleep(900)


def track_single(stock):
    percentage = stock.get_current_percentage()

    print(f"{stock.full_name}: {stock.get_current_price()}")
    # print("{:.2f}".format(round(percentage, 2)))

    if percentage >= 1.05:
        mail_text = f"{stock.full_name} is up by {percentage}% from {stock.last_close} to {stock.get_current_price()}"
        msg = 'Subject: {}\n\n{}'.format(f"Major GAIN for {stock.full_name}", mail_text)
        mail_alert(msg)
        return stock

    if percentage <= 0.95:
        mail_text = f"{stock.full_name} is down by" \
                    f"{1 - percentage}% from {stock.last_close} to {stock.get_current_price()}"
        msg = 'Subject: {}\n\n{}'.format(f"Major LOSS for {stock.full_name}", mail_text)
        mail_alert(msg)
        return stock
    return None


if __name__ == '__main__':
    tracking_main(STOCKS_TO_WATCH)
