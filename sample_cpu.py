# Version 1.0
#
import commands
import smtplib

status, output = commands.getstatusoutput('vmstat 20 1 |awk \'!(NR<=6) {print $16}\'')
message = """From: no-reply@company.com
To: user@company.com
Subject: important.host CPU utilization

CPU threshold reached:
""" + output + """%"""

# Action
if int(output) < 99:
    try:
        smtpObj = smtplib.SMTP('smtp.company.com')
        smtpObj.sendmail('no-reply@company.com', 'user@company.com', message)
    except:
        pass
