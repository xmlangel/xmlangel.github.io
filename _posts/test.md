Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         192.168.1.1     0.0.0.0         UG    0      0        0 eth0
link-local      *               255.255.0.0     U     1000   0        0 eth0
172.17.0.0      *               255.255.0.0     U     0      0        0 docker0
172.18.0.0      *               255.255.0.0     U     0      0        0 br-4025d90e61ca
192.168.1.0     *               255.255.255.0   U     0      0        0 eth0
192.168.33.0    *               255.255.255.0   U     0      0        0 vboxnet0
192.168.57.0    *               255.255.255.0   U     0      0        0 vboxnet1
192.168.80.0    192.168.80.2    255.255.255.0   UG    0      0        0 tun0
192.168.80.2    *               255.255.255.255 UH    0      0        0 tun0	



아오~ 한참을 찾아 다녔습니다. ㅎㅎ
보통 소규모 네트웍에서 서버를 운영시 사설망과 공인망이 공존 하게 됩니다.
즉! 이더넷카트 2개가 eth0 번은 공인망을 eth1번을 사설망을 연결하지요.
각각의 이더넷에 GW를 설정할 경우 문제가 발생합니다.
어떤 GW를 통해 나갈지 찾지를 못하는 거지요.

해결법 1
GW를 eth0 eth1이든 하나로 만들어라! 서버를 운영중이라면 eth0으로 만들어야 겠지요.
GW를 eth0과 eth1에서 각각 설정했다면 삭제 혹은 주석처리하고
# vi /etc/sysconfig/network
GATEWAY=xxx.xxx.xxx.xxx
기본 GW 하나만 설정해 주고 network를 재시작 하자
# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
xxx.xxx.xxx.xxx   *               255.255.255.248 U     0      0        0 eth0
192.168.0.0     *               255.255.255.0   U     0      0        0 eth1
link-local      *               255.255.0.0     U     1002   0        0 eth0
link-local      *               255.255.0.0     U     1003   0        0 eth1
default         xxx.xxx.xxx.xxx   0.0.0.0         UG    0      0        0 eth0

위와같이 설정되면 네트웍에 문제는 없을 것이다.

해결법2
그런데 한가지가 아쉽다.
이더넷 2개로 사설망을 연결한 것은 사설망의 좀 더 빠른 네트웍 속도를 위하여 세팅한 것이데
1번같이 하면... 별 효과가 없어지는 것 아닌가...
그래서 찾아보았다. 라우팅을...
# route add -net 192.168.0.0 netmask 255.255.255.0 gw 192.168.0.1 eth1
사설대역의 GW는 192.168.0.1로 설정하는 라우팅이다.
# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
xxx.xxx.xxx.xxx    *               255.255.255.248 U     0      0        0 eth0
192.168.0.0     192.168.0.1   255.255.255.0   UG    0      0        0 eth1
192.168.0.0     *               255.255.255.0   U     0      0        0 eth1
link-local      *               255.255.0.0     U     1002   0        0 eth0
link-local      *               255.255.0.0     U     1003   0        0 eth1
default         xxx.xxx.xxx.xxx    0.0.0.0         UG    0      0        0 eth0

위와 같이 출력되면 잘 되는 것이다. ㅎㅎ
저는 무식해서 라우팅을 잘 몰랐습니다. 무식하다 놀리시지 마시길.. ㅎㅎ