# Version 1.2.1
# Changes include functionality for use with multiple python versions ( minor bux fix)

# import section
from __future__ import print_function
import sys
if sys.version_info[0] == 2:
    import commands
elif sys.version_info[0] == 3:
    import subprocess

import smtplib
import re
import xml.etree.ElementTree as ET

# Variable Declaration and load
tree = ET.parse('config.xml')
root = tree.getroot()
hostname = root[0][0].text
sender = root[0][1].text
receivers = root[0][2].text
mail_relay = root[0][3].text
df_command = root[0][4].text
volume_string = []  # list of sensitive volumes
volume_threshold = []  # threshold for sensitive volumes
send_email = False
path_count = 0
if sys.version_info[0] == 2:
    status, output = commands.getstatusoutput(df_command)
elif sys.version_info[0] == 3:
    status, output = subprocess.getstatusoutput(df_command)
output = output + '\n'  # Add an end of line character so that regex works
if sys.version_info[0] == 2 and sys.version_info[1] == 6:  # python version 2.6 deprecated .getiterator
    for volume_path in root.getiterator('volume_path'):
        volume_string.append(volume_path.text)  # populate volume list
else:
    for volume_path in root.iter('volume_path'):
        volume_string.append(volume_path.text)  # populate volume list
if sys.version_info[0] == 2 and sys.version_info[1] == 6:  # python version 2.6 deprecated .getiterator
    for threshold in root.getiterator('threshold'):
        volume_threshold.append(threshold.text)  # populate threshold list
else:
    for threshold in root.iter('threshold'):
        volume_threshold.append(threshold.text)  # populate threshold list
for each_path in volume_string:
    path_match = re.findall('\d+%\t' + volume_string[path_count] + '\n', output)
    path_match_percent = re.findall('\d+', path_match[0])
    raw_percentage = int(path_match_percent[0])
    if raw_percentage >= int(volume_threshold[path_count]):
        send_email = True
    path_count += 1
message = """From: """ + sender + """
To: """ + receivers + """
Subject: """ + hostname + """ df

Sensitive Volume Statistics:
""" + output

# Action
if send_email:
    try:
        smtpObj = smtplib.SMTP(mail_relay)
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
else:
    print ("Threshold not met")
