# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab

import sys, socket, argparse
from dnslib import DNSRecord, DNSHeader, RR, A, QTYPE
from os import environ



def print_debug_fn(debug):
    if debug:
        return lambda l : print(l)
    else:
        return lambda l : None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process input')
    parser.add_argument("--ip", help="set listen ip address, set to ENV to get it from PUB_IP Env Variable", action="store", type=str, default="0.0.0.0")
    parser.add_argument("--whitelist", help="Whitelisted Domain. use ALL or DNS_ALLOW_ALL=YES Env variable for access all domain", action="store", type=str, default="Empty")
    parser.add_argument("--port", help="set listen port", action="store", type=int, default=53)
    parser.add_argument("--debug", help="enable debug logging", action="store_true")
    args = parser.parse_args()

    debug = print_debug_fn(args.debug)

    debug('IP: %s Port: %s' % (args.ip, args.port))

    if str(args.ip).upper() == "ENV":
        args.ip = environ.get("PUB_IP")
        debug('ENV IP: %s' % (args.ip,))

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", args.port))

    allow_all = False
    w_list = []
    if environ.get("DNS_ALLOW_ALL") == "YES" or args.whitelist == "ALL":
        allow_all = True
        debug('Allowing all IPs')
    else:
        if args.whitelist != "Empty":
            with open(args.whitelist) as f:
                w_list.extend(f.read().splitlines())

    try:
        while True:
            data, addr = udp_sock.recvfrom(1024)
            d = DNSRecord.parse(data)
            for question in d.questions:
                qdom = question.get_qname()
                r = d.reply()
                if (not allow_all) and (w_list != [] and (not any(s[1:] in str(qdom) for s in w_list))):
                    try:
                        realip = socket.gethostbyname(qdom.idna())
                    except Exception as e:
                        if args.debug:
                            print(e)
                        realip = args.ip
                    r.add_answer(RR(qdom,rdata=A(realip),ttl=60))
                    debug("Request: %s --> %s" % (qdom.idna(), realip))
                else:
                    r.add_answer(RR(qdom,rdata=A(args.ip),ttl=60))
                    debug("Request(local): %s --> %s" % (qdom.idna(), args.ip))
                udp_sock.sendto(r.pack(), addr)
    except KeyboardInterrupt:
        debug("done.")
    udp_sock.close()
