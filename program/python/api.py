from __future__ import print_function
import sys
import zerorpc

class Api(object):
    def calc(self, text):
        """based on the input text, return the int result"""
        try:
            return eval(text)
        except Exception as e:
            return 0.0
    def echo(self, text):
        """echo any text"""
        return text

def parse_port():
    return 4242

def main():
    addr = 'tcp://127.0.0.1:' + str(parse_port())
    s = zerorpc.Server(Api())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
