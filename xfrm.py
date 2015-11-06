import commands
import re
import os
import uuid

'''
`ip xfrm state ` output format:
src 10.22.4.204 dst 10.22.4.104
	proto esp spi 0x00001100 reqid 0 mode tunnel
	replay-window 0 
	auth-trunc hmac(sha1) 0x636c6531706f756574706f756574706f31323334 96
	enc cbc(aes) 0x636c655f636c655f636c655f636c655f636c655f636c655f
	sel src 0.0.0.0/0 dst 0.0.0.0/0 
src 10.22.4.104 dst 10.22.4.204
	proto esp spi 0x00001000 reqid 0 mode tunnel
	replay-window 0 
	auth-trunc hmac(sha1) 0x636c6531706f756574706f756574706f31323334 96
	enc cbc(aes) 0x636c655f636c655f636c655f636c655f636c655f636c655f
	sel src 0.0.0.0/0 dst 0.0.0.0/0 
'''
def dump_sad():
	'''
	  result format: [[sa 1], [sa 2]]
	'''
	output = commands.getoutput('ip xfrm state')
	output = output.split("\n")
	tunnel_sad = []
	sa = []
	for i in output:
		i = i.lstrip()
		if re.match("src", i):
			if len(sa) > 0:
				tunnel_sad.append(sa)
			sa = [i]
		else:
			sa.append(i)
	tunnel_sad.append(sa)
	return tunnel_sad
	
def del_sa(sa):
	'''
	  ip xfrm state delete [ src ADDR ] [ dst ADDR ] [ proto XFRM-PROTO ] [ spi SPI ]
	'''
	cmd = 'ip xfrm state delete src %s dst %s proto %s spi %s' %(sa['src'], sa['dst'], sa['proto'], sa['spi'])
	output = commands.getoutput(cmd)
	return output

def add_sa(sa):
	'''
	  ip xfrm state add [ src ADDR ] [ dst ADDR ] [ proto XFRM-PROTO ] [ spi SPI ] { enc | auth } ALGO-NAME ALGO-KEYMAT [mode tunnel/transport]
	'''
	cmd = 'ip xfrm state add src %s dst %s proto %s spi %s auth %s %s enc %s %s mode %s' %(
			sa['saddr'], sa['daddr'], sa['proto'], sa['spi'], sa['auth_alg'], 
			sa['auth_key'], sa['enc_alg'], sa['enc_key'], sa['mode'])
	print cmd
	output = commands.getoutput(cmd)
	return output

def parse_sa2dict(xfrm_sa):
	sa = dict()
	sa['uuid'] = uuid.uuid4().hex
	for i in range(len(xfrm_sa)):
		data = xfrm_sa[i].split(" ")
		if i == 5:
			sa[data[0]+"-"+data[1]] = data[2]
			sa[data[0]+"-"+data[3]] = data[4]
		elif i > 2:
			sa[data[0]] = data[1]
			sa[data[0]+"-key"] = data[2]
		else:
			for j in range(0, len(data)-1, 2):
				sa[data[j]] = data[j+1]
	return sa
	
def parse_sad():
	sad_list = dump_sad()
	sad_dict_list = []
	for sa in sad_list:
		sad_dict_list.append(parse_sa2dict(sa))
	return sad_dict_list

if __name__ == '__main__':
	print parse_sad()

