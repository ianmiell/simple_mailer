#simple mailer

##Summary

As simple a gmail mailer as I could write.

I wanted to send mails from a server from my gmail account to alert me to things on my server with as little fuss as possible.

After searching for some time for something suitable which required minimal installation, and after following various googled webpage guides and failing to make anything work I decided it would be simpler and more instructive to write my own smtp client.

I'm sure something like this has been written by someone smarter than me, but the deed is done now.

This is not written with security, efficiency or scalability in mind.

##To run
   python simple_mailer.py -h
   usage: simple_mailer.py [-h] --sender SENDER --to TO --passfile PASSFILE
                           [--subject SUBJECT] [--contentfile CONTENTFILE]
                           [--content CONTENT]
   
   Send mail as simply as possible on the command line
   
   optional arguments:
     -h, --help            show this help message and exit
     --sender SENDER       Sender of email
     --to TO               Recipient of email
     --passfile PASSFILE   File with password of from account in; should have
                           perms of read only for the owner
     --subject SUBJECT     Subject of mail
     --contentfile CONTENTFILE
                           Filename containing content of mail
     --content CONTENT     Content of mail as a command line argument


##Requirements
python modules:
    pexpect
    base64
    argparse
    sys
    os
    stat

