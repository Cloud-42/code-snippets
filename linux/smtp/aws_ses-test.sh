# openssl s_client -crlf -quiet -starttls smtp -connect email-smtp.eu-west-1.amazonaws.com:587 < unix-ses-test.tx
# remove line above before applying
EHLO ireland-smtp
AUTH LOGIN
~~ base 64 SMTP username ~~
~~ base 64 SMTP password ~~
MAIL FROM: app@domain.com
RCPT TO: chris@cloud42.io
DATA
#X-SES-CONFIGURATION-SET: YourSESConfigSet
From: APP <app@domain.com>
To: chris@cloud42.io
Cc: chris@cloud42.io
Subject: Hello from Amazon SES SMTP Test for UNIX
.
QUIT
