keysCSV = file("keys.csv", "rU")
apikeys = dict()
for row in keysCSV:
    row = row.split(',')
    apikeys[row[0]] = row[1:]

def getKey(api):
    return apikeys[api][0][:-1]
