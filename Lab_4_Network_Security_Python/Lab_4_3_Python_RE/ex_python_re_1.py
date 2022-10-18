import re, datetime

startTime = datetime.datetime.now()

with open('sample_log_anonymized.log', 'r') as f:
    for line in f.readlines():
        if re.search('AUTHPRIV-3-SYSTEM_MSG', line):
            print(line)

endTine = datetime.datetime.now()
elapsedTime = endTine - startTime
print("time Elapsed: " + str(elapsedTime))