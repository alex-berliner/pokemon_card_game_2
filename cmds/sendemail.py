import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import subprocess

def get_ip_address_info():
    """
    Executes 'ip a' command and returns the output as a string.
    """
    # Run the command with shell=True to handle spaces in the command
    result = subprocess.run(["ip", "a"], capture_output=True, text=True)
    # Check for errors
    if result.returncode != 0:
        raise RuntimeError(f"Error executing 'ip a': {result.stderr}")
    # Return the captured output (already decoded to string)
    r = [x for x in str(result.stdout).split("\n") if "192.168" in x][-1]
    r = r.strip()
    r = r.split(" ")[1]
    r = r.split("/")[0]

    return r

time.sleep(10)

ip = get_ip_address_info()
ssh_string = f"xxx   ssh pi@{ip}"
message = MIMEMultipart()
message["To"] = 'monorail0@gmail.com'
message["From"] = 'Poke Pi'
message["Subject"] = 'IP Address'

title = '<b> Title line here. </b>'
messageText = MIMEText(ssh_string,'html')
message.attach(messageText)

email = 'alexberliner@gmail.com'
password = ''

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo('Gmail')
server.starttls()
server.login(email,password)
fromaddr = 'alexberliner@gmail.com'
toaddrs  = 'monorail0@gmail.com'
server.sendmail(fromaddr,toaddrs,message.as_string())

server.quit()
