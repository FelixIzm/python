import sys
import argparse
 
 
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('name', nargs='?')
 
    return parser
 
 
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
 
    # print (namespace)
 
    if namespace.name:
        print ("Привет, {}!".format (namespace.name) )
    else:
        print ("Привет, мир!")