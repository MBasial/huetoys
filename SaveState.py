def main():
    from pprint import pprint
    from phue import Bridge
    print('Saving bridge state to api_end.txt.')
    b = Bridge('192.168.1.110')
#    b = Bridge()
    b.connect()
    pprint(b.get_api(), stream=open('api_end.txt','w'))

if __name__ == '__main__':
    main()

