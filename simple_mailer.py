import pexpect
import base64
import argparse
import sys

# TODO:
# subject
# password file's perms
# content 

def main(args):
	f = file(args.passfile)
	password = f.read().strip()
	sender = args.sender
	recipient = args.to
	auth_base64 = base64.b64encode('\0'+sender+'\0'+password)
	smtp_session(sender,auth_base64,recipient)

def smtp_session(sender,auth_string,recipient):
	child = pexpect.spawn('openssl s_client -starttls smtp -connect smtp.gmail.com:587 -crlf -ign_eof')
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
	child.send('stuff1\n.\n')
	child.expect('250.*OK')
	child.sendline('quit')
	child.expect('221.*closing')
	print 'sent'

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Send mail as simply as possible on the command line')
	parser.add_argument('--sender', help='sender of email',required=True)
	parser.add_argument('--to', help='recipient of email',required=True)
	parser.add_argument('--passfile', help='file with password of from account in; should have perms of read only for the owner',required=True)
	args = parser.parse_args()
	main(args)


