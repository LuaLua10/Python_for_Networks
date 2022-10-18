import re, datetime

startTime = datetime.datetime.now()

term1 = re.compile('AUTHPRIV-3-SYSTEM_MSG')
term2 = re.compile('ACLLOG-5-ACLLOG_FLOW_INTERVAL')

fileList = ['sample_log_anonymized.log', 'sample_log_anonymized_1.log']

for log in fileList:
    with open(log, 'r') as f:
        for line in f.readlines():
            if re.search(term1, line) or re.search(term2, line):
                print(line)

endTine = datetime.datetime.now()
elapsedTime = endTine - startTime
print("time Elapsed: " + str(elapsedTime))