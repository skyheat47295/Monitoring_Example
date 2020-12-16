# Version 1.0
#
import subprocess
import smtplib

status, output = subprocess.getstatusoutput('cat /var/log/logstash/logstash-plain.log /var/log/elasticsearch/elasticsearch.log |egrep \'WARN|DEBUG\' |wc -l')
message = """From: no-reply@company.com
To: user@company.com
Subject: logstash2 log

Log error count threshold reached:
""" + output + """ lines"""

# Action
if int(output) > 1:
    try:
        smtpObj = smtplib.SMTP('smtp.company.com')
        smtpObj.sendmail('no-reply@company.com', 'user@company.com', message)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
else:
    print ("Threshold not met")
