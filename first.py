import datetime, re
a = ['one','','three']
b={'id':'12345678','fl':a}
print(len(a))
print(b)
print(b['id'])
today = datetime.datetime.today()
print( today.strftime("%d-%m-%Y %H.%M.%S") )
str1 = '50574334'
print(re.findall(r'\d+', str1)[0])