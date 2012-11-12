import pexpect
import base64
import argparse
import sys
import os
import stat


# TODO:
# logging
# HTML messages; http://en.wikipedia.org/wiki/MIME
# Reply-To

def main(args):
	if is_file_secure(args.passfile) == False:
		print "File: " + args.passfile + " must be readable only by user running the script"
		exit()
	f = file(args.passfile)
	password = f.read().strip()
	sender = args.sender
	recipient = args.to
	if args.contentfile != None:
		content = file(args.contentfile).read()
	elif args.content != None:
		content = args.content
	else:
		print "You must provide content for the email"
		exit()
	if args.subject == None:
		subject = ""
	else:
		subject = args.subject
	auth_base64 = base64.b64encode('\0'+sender+'\0'+password)
	smtp_session(sender,auth_base64,recipient,subject,content)

def smtp_session(sender,auth_string,recipient,subject,content):
	# OR? openssl s_client -connect smtp.gmail.com:465 -crlf -ign_eof
	#child = pexpect.spawn('openssl s_client -starttls smtp -connect smtp.gmail.com:587 -crlf -ign_eof')
	child = pexpect.spawn('openssl s_client -starttls smtp -connect smtp.gmail.com:587 -crlf -quiet')
	child.logfile = sys.stdout
	child.expect('250 ENHANCEDSTATUSCODES')
	child.sendline('EHLO localhost')
	child.expect('250 ENHANCEDSTATUSCODES')
	child.sendline('AUTH PLAIN ' + auth_string)
	child.expect('235.*Accepted')
	child.sendline('MAIL FROM: <' + sender + '>')
	child.expect('250.*OK')
	child.sendline('RCPT TO: <' + recipient + '>')
	child.expect('250.*OK')
	child.sendline('DATA')
	child.expect('Go ahead')
	child.send('Subject: ' + subject + '\n\n')
	child.sendline(content)
	child.sendline('.')
	child.expect('250.*OK')
	child.sendline('quit')
	child.expect('221.*closing')
	print 'sent'

def is_file_secure(file_name):
	try:
		file_mode = os.stat(file_name).st_mode
		if file_mode & (stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH):
			return False
	except:
		pass
	return True


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Send mail as simply as possible on the command line')
	parser.add_argument('--sender', help='Sender of email',required=True)
	parser.add_argument('--to', help='Recipient of email',required=True)
	parser.add_argument('--passfile', help='File with password of from account in; should have perms of read only for the owner',required=True)
	parser.add_argument('--subject', help='Subject of mail',required=False)
	parser.add_argument('--contentfile', help='Filename containing content of mail',required=False)
	parser.add_argument('--content', help='Content of mail as a command line argument',required=False)
	args = parser.parse_args()
	main(args)


