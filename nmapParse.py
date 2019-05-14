import sys, getopt

def main(argv):
    infile = ''
    service = ''
    try:
        opts, args = getopt.getopt(argv,'hs:i:')
    except getopt.GetoptError:
        print('nmapParse.py -s <service name or port/protocol> -i <input file>\n')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Simple utility to filter the output of nmap scans.')
            print('nmapParse.py -s <service name or port/protocol> -i <input file>\n')
            print('Examples:')
            print('nmapParse.py -s Tomcat -i scan.txt')
            print('nmapParse.py -s 22/tcp -i scan.txt')
            sys.exit()
        elif opt in ("-s"):
            service = arg
        elif opt in ("-i"):
            infile = arg

    with open(infile) as f:
        content = f.readlines()

    serviceIndex = []
    ipIndex = []

    for x in range(len(content)):
        if service in content[x]:
            serviceIndex.append(x)
            for z in range(x, 0, -1):
                if 'Nmap scan report' in content[z]:
                    ipIndex.append(z)
                    break
    
    finalList = {}
    for x in range(len(serviceIndex)):
        if ipIndex[x] in finalList:
            finalList[ipIndex[x]].append(serviceIndex[x])
        else:
            finalList[ipIndex[x]] = [serviceIndex[x]]
    
    for key in finalList:
        print(content[key].strip())
        for value in finalList[key]:
            print(content[value].strip())
        print('\n')
    
    print("Found %d unique IP addresses running a total of %d instances of %s." % (len(finalList), len(serviceIndex), service))
    
if __name__ == "__main__":
   main(sys.argv[1:])
