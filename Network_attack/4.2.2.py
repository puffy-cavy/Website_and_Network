#!/usr/bin/python2.7
import dpkt
import sys
import socket


def main():
    if (len(sys.argv) < 2):
        print "error: need argument"
        sys.exit(1)
    filename = sys.argv[1]
    what_array = {}
    result = []
    f = open(filename)
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
    	try: 
    		eth = dpkt.ethernet.Ethernet(buf)
    		if eth.type != dpkt.ethernet.ETH_TYPE_IP:
    			continue
    		ip = eth.data
    		if ip.p != dpkt.ip.IP_PROTO_TCP:
    			continue
    		tcp = ip.data

    		if (tcp.flags & dpkt.tcp.TH_SYN != 0) and (( tcp.flags & dpkt.tcp.TH_FIN ) == 0) and (( tcp.flags & dpkt.tcp.TH_RST ) == 0) and (( tcp.flags & dpkt.tcp.TH_PUSH) == 0) and (( tcp.flags & dpkt.tcp.TH_URG ) == 0) and (( tcp.flags & dpkt.tcp.TH_ECE ) == 0) and (( tcp.flags & dpkt.tcp.TH_CWR ) == 0):
    			src_to_dst = socket.inet_ntoa(ip.src)+";"+socket.inet_ntoa(ip.dst)
    			dst_to_src = socket.inet_ntoa(ip.dst)+";"+socket.inet_ntoa(ip.src)
    			if tcp.flags & dpkt.tcp.TH_ACK == 0: #it's a src
    				if src_to_dst in what_array:
    					what_array[src_to_dst][0] += 1 #increment count
    				else:
    					what_array[src_to_dst] = [] #set count to zero
    					#what_array[src_to_dst].append(dst_to_src)
    					what_array[src_to_dst].append(1)
    					what_array[src_to_dst].append(0)
    			else:
    				if dst_to_src in what_array:
    					what_array[dst_to_src][1] += 1
    				else:
    					what_array[dst_to_src] = [] #set count to zero
    					#what_array[dst_to_src].append(src_to_dst)
    					what_array[dst_to_src].append(0)
    					what_array[dst_to_src].append(1)

    	except dpkt.NeedData as error:
    		continue

    for i in what_array:
    	if what_array[i][0] > what_array[i][1]*3:
    		idx = i.find(';')
    		result.append(i[:idx])
    result = set(result)
    for x in result:
    	print x
    f.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
