##
# Task1
##
list1 = ['a', 'b', 'c', 'd', 'e', 'f']
list2 = [1, 2, 3, 4]
dictionary = {}
i = 0
if len(list1) >= len(list2):
    while i < len(list1):
        if i < len(list2):
            dictionary[list1[i]] = list2[i]
        else:
            dictionary[list1[i]] = None
        i += 1
else:
    while i < len(list1):
        dictionary[list1[i]] = list2[i]
        i += 1
print(dictionary)

##
# Task2
##

word = "otto"
if word == word[::-1]:
    print("YEAH!")
else:
    print("NOPE")

##
# Task3
##

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
result = list(set(a) & set(b))
print(result)

##
# Task4
##
resultList = {}
resultIps = []
count = 0
with open("access.log", "r") as logfile:
    data = logfile.readlines()
    for value in data:
        ipAddress = value.split(' - - ')[0]
        if ipAddress in resultList:
            resultList[ipAddress] += 1
        else:
            resultList[ipAddress] = 1
while count < 10:
    maxVal = max(resultList, key=lambda val: resultList[val])
    resultIps.append(maxVal)
    del resultList[maxVal]
    count += 1
print(resultIps)
