#print("hello world {} {0}".format('fff'))

post = '''{{"author": {0},"text": "text","tags": ["mongodb", "python", "pymongo"],"date": "date"}}'''
post = post.format("Robert")

print(post)