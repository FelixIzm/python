from grab import Grab
g  = Grab()
resp = g.go('https://obd-memorial.ru/html/search.htm?f=измайлов&n=&s=&y=&r=&p=1')
print(resp.code)
print(resp.cookies.__getitem__('3fbe47cd30daea60fc16041479413da2'))