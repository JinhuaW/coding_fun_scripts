mail_from = "jinhua.wu@alcatel-sbell.com.cn"

from email.mime.text import MIMEText

def send_mail(mailContent, subject, From, To):
	import smtplib
	msg = mailContent
	msg['Subject'] = subject
	msg['From'] = From
	msg['To'] = To
	try:
		s = smtplib.SMTP('135.251.206.35') 
		s.sendmail(From, To.split(','), msg.as_string())
		print "Sending mail success!"
	except smtplib.SMTPException:
		print "Sending mail failed!"

def send_mail_plain(mail_content, subject, From, To):
	message = MIMEText(mail_content, 'plain', 'utf-8')
	send_mail(message, subject, From, To)

