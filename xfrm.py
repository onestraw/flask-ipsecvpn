import commands
import re
import uuid
from collections import OrderedDict


def dump_sad():
    """
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

    result format: [[sa 1], [sa 2]]
    """
    output = commands.getoutput('ip xfrm state')
    output = output.split("\n")
    tunnel_sad = []
    sa = []
    for i in output:
        i = i.lstrip()
        if re.match('src', i):
            if len(sa) > 0:
                tunnel_sad.append(sa)
            sa = [i]
        else:
            sa.append(i)
    tunnel_sad.append(sa)
    return tunnel_sad


def del_sa(sa):
    """
        ip xfrm state delete \
                [ src ADDR ] [ dst ADDR ] [ proto XFRM-PROTO ] [ spi SPI ]
    """
    cmd = 'ip xfrm state delete src %s dst %s proto %s spi %s' % (
            sa['src'], sa['dst'], sa['proto'], sa['spi'])
    output = commands.getoutput(cmd)
    return output


def add_sa(sa):
    """
        ip xfrm state add [ src ADDR ] [ dst ADDR ] \
                [ proto XFRM-PROTO ] [ spi SPI ] \
                { enc | auth } ALGO-NAME ALGO-KEYMAT [mode tunnel/transport]
    """
    cmd = 'ip xfrm state \
            add src %s dst %s proto %s spi %s auth %s %s enc %s %s mode %s' % (
            sa['saddr'], sa['daddr'], sa['proto'], sa['spi'], sa['auth_alg'],
            sa['auth_key'], sa['enc_alg'], sa['enc_key'], sa['mode'])
    print cmd
    output = commands.getoutput(cmd)
    return output


def parse_sa2dict(xfrm_sa):
    sa = OrderedDict()
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
    sad_dict_list = [parse_sa2dict(sa) for sa in sad_list]
    return sad_dict_list


def dump_spd():
    """
    `ip xfrm policy` output format
    src 192.168.200.0/24 dst 192.168.100.0/24
        dir out priority 2147481648
        tmpl src 10.22.4.204 dst 10.22.4.104
            proto esp reqid 0 mode tunnel
    src 192.168.100.0/24 dst 192.168.200.0/24
        dir fwd priority 2147481648
        tmpl src 10.22.4.104 dst 10.22.4.204
            proto esp reqid 0 mode tunnel
    src 192.168.100.0/24 dst 192.168.200.0/24
        dir in priority 2147481648
        tmpl src 10.22.4.104 dst 10.22.4.204
            proto esp reqid 0 mode tunnel
    """
    output = commands.getoutput('ip xfrm policy')
    output = output.split("\n")
    spd = []
    sp = []
    for i in output:
        i = i.lstrip()
        if re.match('src', i):
            if len(sp) > 0:
                spd.append(sp)
            sp = [i]
        else:
            sp.append(i)
    spd.append(sp)
    return spd


def del_sp(sp):
    """
        ip xfrm policy del src 192.168.200.0/24 dst 192.168.100.0/24 dir in
    """
    cmd = 'ip xfrm policy del src %s dst %s dir %s' % (
            sp['src'], sp['dst'], sp['dir'])
    print cmd
    output = commands.getoutput(cmd)
    return output


def add_sp(sp):
    """
        add src 192.168.200.0/24 dst 192.168.100.0/24 dir in tmpl \
            src 10.22.4.204 dst 10.22.4.104 proto esp mode tunnel priority 2000
    """
    cmd = 'ip xfrm policy add src %s dst %s dir %s tmpl \
            src %s dst %s proto %s mode %s priority %s' % (
            sp['saddr'], sp['daddr'], sp['dir'], sp['sel-src'], sp['sel-dst'],
            sp['proto'], sp['mode'], sp['priority'])
    print cmd
    output = commands.getoutput(cmd)
    return output


def parse_sp2dict(raw_sp):
    sp = OrderedDict()
    sp['uuid'] = uuid.uuid4().hex
    for i in range(len(raw_sp)):
        data = raw_sp[i].split(" ")
        if i == 2:
            sp['selector-'+data[1]] = data[2]
            sp['selector-'+data[3]] = data[4]
        else:
            for j in range(0, len(data)-1, 2):
                sp[data[j]] = data[j+1]
    return sp


def parse_spd():
    spd_list = dump_spd()
    return [parse_sp2dict(sp) for sp in spd_list]


if __name__ == '__main__':
    print parse_sad()
