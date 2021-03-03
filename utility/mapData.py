def mapUser(userName, mapList):
    if userName not in mapList:
        mapList.append(userName)
    return mapList.index(userName), mapList

def mapResult(result, mapList=["Success", "Fail"]):
    if result not in mapList:
        mapList.append(result)
    return mapList.index(result), mapList
