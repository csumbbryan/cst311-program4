#!/usr/bin/python

"""Network Provisioner for CST311 Programming Assignment 4"""
__author__ = "Team 2"
__credits__ = [
  "Henry Garkanian",
  "Ivan Soria",
  "Kyle Stefun",
  "Bryan Zanoli"
]

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import subprocess
from mininet.term import makeTerm #Added per requirements for Group Chat
import time

#Runs the certificate_generation script to enable TLS based communication on chat server
subprocess.run(["sudo", "-E", "python3", "certificate_generation.py"])

#CONSTANTS: 
H1IP = '10.0.1.11/24'
H2IP = '10.0.1.12/24'
H3IP = '10.0.2.13/24'
H4IP = '10.0.2.14/24'
R3ETH0IP = '10.0.1.1/24'
R3ETH1IP = '192.168.0.1/30'
R4ETH0IP = '192.168.0.2/30'
R4ETH1IP = '192.168.1.1/30'
R5ETH1IP = '192.168.1.2/30'
R5ETH0IP = '10.0.2.1/24'
SUBNET1ROUTE = 'via 10.0.1.1'
SUBNET2ROUTE = 'via 10.0.2.1'
ROUTER3STATIC1 = 'ip route add 192.168.1.0/30 via 192.168.0.2 dev r3-eth1'
ROUTER3STATIC2 = 'ip route add 10.0.2.0/24 via 192.168.0.2 dev r3-eth1'
ROUTER4STATIC1 = 'ip route add 10.0.1.0/24 via 192.168.0.1 dev r4-eth0'
ROUTER4STATIC2 = 'ip route add 10.0.2.0/24 via 192.168.1.2 dev r4-eth1'
ROUTER5STATIC1 = 'ip route add 192.168.0.0/30 via 192.168.1.1 dev r5-eth1'
ROUTER5STATIC2 = 'ip route add 10.0.1.0/24 via 192.168.1.1 dev r5-eth1'
#

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    #Moved below two lines from under r5 lines to above to ensure switches are created first
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    #Specified IP for router
    r5 = net.addHost('r5', cls=Node, ip=R5ETH0IP)
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    #Specified IP for router
    r4 = net.addHost('r4', cls=Node, ip=R4ETH0IP)
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    #Specified IP for router
    r3 = net.addHost('r3', cls=Node, ip=R3ETH0IP)
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    #Updated IP Addresses via constants and added routes via constants
    h1 = net.addHost('h1', cls=Host, ip=H1IP, defaultRoute=SUBNET1ROUTE)
    h2 = net.addHost('h2', cls=Host, ip=H2IP, defaultRoute=SUBNET1ROUTE)
    h3 = net.addHost('h3', cls=Host, ip=H3IP, defaultRoute=SUBNET2ROUTE)
    h4 = net.addHost('h4', cls=Host, ip=H4IP, defaultRoute=SUBNET2ROUTE)

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s2, r5)
    net.addLink(s1, r3)
    #Added secondary ethernet configuration here
    net.addLink(r3, r4,intfName1='r3-eth1',params1={'ip':R3ETH1IP},intfName2='r4-eth0')
    net.addLink(r4, r5,intfName1='r4-eth1',params1={'ip':R4ETH1IP},intfName2='r5-eth1',params2={'ip':R5ETH1IP})

    info( '*** Starting network\n')
    net.build()
    #Adding Static Routes:
    net['r3'].cmd(ROUTER3STATIC1)
    net['r3'].cmd(ROUTER3STATIC2)
    net['r4'].cmd(ROUTER4STATIC1)
    net['r4'].cmd(ROUTER4STATIC2)
    net['r5'].cmd(ROUTER5STATIC1)
    net['r5'].cmd(ROUTER5STATIC2)
    
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    
    makeTerm(h4, title='Node', term='xterm', display=None, cmd='sudo python ./tpa4_chat_server_tls.py; bash')
    time.sleep(.2)
    makeTerm(h1, title='Node', term='xterm', display=None, cmd='sudo python ./tpa4_chat_client_tls.py; bash')
    makeTerm(h2, title='Node', term='xterm', display=None, cmd='sudo python ./tpa4_chat_client_tls.py; bash')
    makeTerm(h3, title='Node', term='xterm', display=None, cmd='sudo python ./tpa4_chat_client_tls.py; bash')

    CLI(net)
    net.stop()
    net.stopXterms()
    
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()