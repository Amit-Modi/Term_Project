# for python 2

import smtplib
import imaplib
import email

def remove_html_tags(text):
	tag = False
	quote = False
	out = ""

	for c in text:
			if c == '<' and not quote:
				tag = True
			elif c == '>' and not quote:
				tag = False
			elif (c == '"' or c == "'") and tag:
				quote = not quote
			elif not tag:
				out = out + c

	return out

def remove_extra_space(text):
	return ' '.join(text.split())

def get_documents(EMAIL_ID, PWD, SMTP_SERVER, SMTP_PORT):
	try:
		# print ('trying to login')
		mail = imaplib.IMAP4_SSL(SMTP_SERVER)
		# print ('found mail')
		mail.login(EMAIL_ID,PWD)
		# print ('loged in')
		mail.select('inbox')
		# print ('mail seleced')

		tpe, data = mail.search(None, 'ALL')
		mail_ids = data[0]

		id_list = mail_ids.split()   
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])

		# print (first_email_id, latest_email_id)
		for i in range(latest_email_id,first_email_id, -1):
			typ, data = mail.fetch(i, '(RFC822)' )
			for response_part in data:
				# print (response_part)
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1])
					email_subject = msg['subject']
					email_from = msg['from']
					if email_from == "Ukasha Noor <ukashanoor.iiitk@gmail.com>":
						print ('From : ' + email_from + '\n')
						print ('Subject : ' + email_subject + '\n')
						if msg.is_multipart():
								# if payload.is_multipart(): ...
								doc = " ".join([payload.get_payload() for payload in msg.get_payload()])
						else:
							doc = msg.get_payload()
						doc = remove_html_tags(doc)
						doc = get_document_vector(doc)
						print ("doc:\n" + doc + '\n')


	except Exception as e:
		print (str(e))


if __name__ == '__main__':
	import getpass
	SMTP_SERVER = "imap.gmail.com" # input("SMTP_SERVER : ")
	SMTP_PORT = 993 # int(input("SMTP_PORT : "))
	EMAIL_ID = input("Email id : ")
	PWD = getpass.getpass()
	# print (type(SMTP_SERVER))
	# print (type(SMTP_PORT))
	# print (type(EMAIL_ID))
	# print (type(PWD))
	get_documents(EMAIL_ID, PWD, SMTP_SERVER, SMTP_PORT)