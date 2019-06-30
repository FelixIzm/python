from requests_html import HTMLSession
import json

session = HTMLSession()
payload = {'json': '1', 'xmlParam': '<request firstRecordPosition="0" maxNumRecords="50" countResults="true"><record f23="P~одесская обл" entity="Человек Награждение"></record><record f23="P~одесская обл" entity="Человек Представление"></record><record f23="P~одесская обл" entity="Человек Картотека"></record><record f23="P~одесская обл" entity="Человек Юбилейная Картотека"></record></request>'}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

r = session.post("http://podvignaroda.ru/Image3/newsearchservlet", data=payload, headers=headers)
#print(len(json.loads(r.text)['records']))
print(r.text)