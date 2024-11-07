import argparse
import os
import smtplib
import socket
from json import loads
from urllib.request import urlopen

FILE_STORE = ".data"

if __name__ == '__main__':
    # Process command line arguments
    arg_parser = argparse.ArgumentParser(description='Send an email with external IP')
    arg_parser.add_argument('--from', type=str, required=True)
    arg_parser.add_argument('--to', type=str, required=True, )
    arg_parser.add_argument('--user', type=str, required=True)
    arg_parser.add_argument('--password', type=str, required=True)
    arg_parser.add_argument('--smtp_host', type=str, required=True)
    arg_parser.add_argument('--smtp_port', type=int, required=True)

    # Parse the command line arguments
    args = arg_parser.parse_args()
    from_addr = vars(args)['from']
    to_addrs = vars(args)['to']
    user = vars(args)['user']
    password = vars(args)['password']
    smtp_host = vars(args)['smtp_host']
    smtp_port = vars(args)['smtp_port']

    # Get public IP
    data = loads(urlopen("http://httpbin.org/ip").read())
    print("The public IP is : %s" % data["origin"])
    send_email = True
    # Check if IP changed
    if os.path.exists(FILE_STORE):
        with open(FILE_STORE) as f:
            last_ip = f.read()
            if last_ip == data["origin"]:
                print("Email already sent!!!")
                send_email = False
    else:
        with open(FILE_STORE, 'w', encoding='utf-8') as f:
            f.write(data["origin"])
    if send_email:
        try:
            server_ssl = smtplib.SMTP_SSL(smtp_host, smtp_port)
            server_ssl.ehlo()

            server_ssl.login(user=user, password=password)
            message_subject = "IP {0} ".format(socket.gethostname()) + data["origin"]
            message_text = "Script"
            message = "From: %s\r\n" % from_addr + "To: %s\r\n" % to_addrs + "Subject: %s\r\n" % message_subject + "\r\n" + message_text

            server_ssl.sendmail(from_addr=from_addr, to_addrs=to_addrs, msg=message)
            print("Successfully sent email!")

        except smtplib.SMTPException as e:
            print("Something went wrong...")
            print(e)
