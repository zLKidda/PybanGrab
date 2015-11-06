import socket

def retBanner(ip, port):
    #  what this method does is it gets the IP and Port and tries to connect to the
    #  ip on that port and then will save the next 1024 bytes of data to the variable banner
    #  it will then return the banner to the method that called it
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = str(s.recv(1024)).strip('\n')
        print("\n[+] banner from port", port, " = ", banner)
        return banner
    except:
        return


def checkVulns(banner,port,ip):
    # opens the file
    # iterates threw the file using the method readline()
    # each line is compared against the banner
    # if match found then the surver is vulnerable and the port exploit will be printed
    f = open("vuln_banners.txt",'r')  # r = read only mode

    server = f.readline().strip('\n')
    comment =  f.readline().strip('\n')

    while(server != "#EOF#"):
        if server in banner:
            print("[+] Server is vulnerable: ", banner, "on port", port)
            temp = ("[+] " + comment)
            print(temp)
        server = f.readline().strip('\n')
        comment =  f.readline().strip('\n')


def main():
    #   This is going to find the ports that the user wants to scan and then the ip address/es to scan
    #   after this then this will scan the ports and retrive a banner
    #   the banner will be compaired to a file
    portList = [21, 22, 25, 80, 110, 443]  # FTP, SSH, SMTP, HTTP, POP, HTTPS
    portTemp = input("Do you want to add custom ports to scan yes/no\n")
    if portTemp == "yes" and "y" and "Yes" and "y" and "YES":
        allPorts = input("Do you want to scan a range of ports yes/no\n")
        if allPorts == "yes" and "y" and "Yes" and "y" and "YES":
            start = int(input("please enter the start range for the ports\n"))
            end = int(input("please enter the end range for the ports\n"))
            templist = []
            for i in range(start,end):
                if i not in portList:
                    templist.append(i)
            portList = portList + templist
        port2append = input("Please enter the additional ports separated by a space\n")
        addPorts = port2append.split(" ")
        portList = portList + addPorts
        print(portList)

    temp = input("[-] Do you want to target a range of ip's or a single target: range or single\n")
    if temp in ['r', 'R', 'range', 'Range', 'RANGE']:
        min= int(input("Please enter the minimum ip in the range to scan e.g 0\n"))
        max= int(input("Please enter the maximum ip in the range to scan e.g 150\n"))
        for x in range(min, max):
            ip = input("Please enter the ip without the numbers after the last dot\n")
            if ip == "":
                ip = '192.168.150.' + str(x)

            for port in portList:
                banner = retBanner(ip, port)
                if banner:
                    checkVulns(banner,port,ip)

    if temp in ['s', 'S', 'Single', 'single', 'SINGLE', 'sin']:
        ip = input("Please enter the ip of the target\n")
        if ip == "":
            ip = '192.168.150.132'

        for port in portList:
            banner = retBanner(ip, port)
            if banner:
                print('[+]', ip, ':', banner)
                checkVulns(banner,port,ip)
    else:
        print("please choose a real answer")
        main()


if __name__ == "__main__":
    main()
