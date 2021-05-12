---
layout: post
title:  "Ubnutu route 설정"
date:   2017-07-21 10:50:13 +0900
categories: linux update
comments: true
tags :
- Ubuntu
- route
- IP
---

라우팅(Routing) - 패킷(Packet)이 목적지까지 갈 수 있도록 경로를 올바르게 설정해 주는 작업.
* 목차
{:toc}

모든 검증은 ubuntu 16.04 에서 했다. 그리고 권한은 root 권한을 가지고 작업을 해야 한다.

# Route table


HOST A가 HOST B에게 데이터를 전송하고자 할 때, 두 호스트가 같은 로컬 네트워크 상에 있다면, IP 프로토콜은 출발지와 도착지 호스트의 IP 주소를 ARP 를 사용해서 물리적 주소로 변환한다. 그리고 그 물리적 주소들은 (프레임을 만들기 위해) IP 데이터그램에 추가되고, 프레임을 이용해 두 호스트는 서로 간에 직접 통신을 한다. 그런데 두 호스트가 같은 로컬 네트워크 상에 있지 않으면 직접 통신할 수 없고 라우터를 거쳐서 통신해야 한다.

라우터는 특정한 경로(ROUTE)가 알려져 있지 않은 로컬 네트워크 밖의 호스트와 통신할 때 사용된다.
두 호스트가 같은 로컬 네트워크에 있지 않다면, 호스트 A는 라우터의 라우팅 표를 체크하여 호스트 B의 로컬 네트워크에 연결될 수 있는지 살펴본다. 만약 일치하는 것을 찾지 못하면 데이터는 "디폴트 게이트웨이"로 보내진다.

대부분 패킷을 목적지까지 전달하기 위해 한 라우터 만을 경유하지는 않는다. 라우터는 다른 라우터로 가는 경로를 알고 있다.

## route 명령는 아래와 같은 옵션들이 있다.

- 라우팅 테이블을 확인하거나 수정할 수 있다.

- 활성화되어 있는 네트워크 인터페이스를 통해 정적 라우트를 설정할 수 있다.

명령어 옵션

    -F : display Forwarding Information Base(FIB) (default)

    -C : display routing cache instead of FIB --cache

    -n : don't resolve names. --numeric

    -e : display other/more information. --extended

    del : delete a route.

    add : add a new route.

    -net : 목적지 네트워트

    -host : 목적지 호스트

    netmask : 네트워크 라우트를 추가할 때, 사용 될 넷마스크

    gw : route packets via a gateway

    dev if : force the route to be associated with the specified device.

## 라우팅 테이블 (Routing Table)

route 명령이 수행되었을 때 보여주는 테이블이다. 

- Destination : 목적지 네트워트 또는 목적지 호스트 주소

- Gateway : 게이트웨이 주소, 설정되어 있지 않다면 *

- Genmask : The netmask for the destination net; '255.255.255.255' for a host destination and '0.0.0.0' for the default route.

- Flags : 
{% highlight bash %}
    U (route is Up) 라우트 동작 상태

    H (target is a Host) 목적지 호스트 

    G (use Gateway) 게이트웨이 사용

    R (Reinstate route for dynamic routing)

    D (dynamically installed by Daemon or redirect) 데몬 또는 ICMP Redirect Message에 의해 
    동적으로 설치된 상태
    
    M (Modified from routing daemon or redirect) 데몬 또는 ICMP Redirect Message에 의해 변경된 상태 
    
    A (installed by Addrconf)
    
    C (Cache entry)
    
    ! (reject route) 라우트 거부
{% endhighlight %}

- Metric : Target까지의 거리를 홉(Hop) 단위로 계산, 최근 커널에서는 사용하지 않으나 라우팅 데몬에 의해 사용

- Ref : 현재 라우트에 대한 레퍼런스 수, 리눅스 커널에서는 사용되지 않음

- Use : 라우트 탐색 수

- iface : 패킷이 전달되는 인터페이스

### 사용 예제
virtual box 를 가지고 테스트를 해보려고 한다.

VirtualBox 2개를 생성한다.
- 각 VirtualBox 에는 2개의 네트워크 카드를 장착한다.

- A Host 정보
{% highlight bash %}
root@local-vm-ubuntu:~# ifconfig
enp0s3    Link encap:Ethernet  HWaddr 08:00:27:fd:dc:d4
          inet addr:192.168.0.108  Bcast:192.168.0.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fefd:dcd4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:44855 errors:0 dropped:68 overruns:0 frame:0
          TX packets:1312 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:4875291 (4.8 MB)  TX bytes:86635 (86.6 KB)

enp0s8    Link encap:Ethernet  HWaddr 08:00:27:8f:3c:58
          inet addr:192.168.99.100  Bcast:192.168.99.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fe8f:3c58/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:10295 errors:0 dropped:0 overruns:0 frame:0
          TX packets:6267 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:855770 (855.7 KB)  TX bytes:995967 (995.9 KB)
root@local-vm-ubuntu:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         dlinkrouter     0.0.0.0         UG    0      0        0 enp0s3
192.168.0.0     *               255.255.255.0   U     0      0        0 enp0s3
192.168.99.0    *               255.255.255.0   U     0      0        0 enp0s8
{% endhighlight %}
- B Host 정보
{% highlight bash %}
root@local-vm-ubuntu-02:~# ifconfig
enp0s3    Link encap:Ethernet  HWaddr 08:00:27:7b:f4:f4
          inet addr:192.168.0.110  Bcast:192.168.0.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fe7b:f4f4/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:44831 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1199 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:4828633 (4.8 MB)  TX bytes:75710 (75.7 KB)

enp0s8    Link encap:Ethernet  HWaddr 08:00:27:a2:e4:dc
          inet addr:192.168.99.110  Bcast:192.168.99.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fea2:e4dc/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:733 errors:0 dropped:0 overruns:0 frame:0
          TX packets:362 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:69794 (69.7 KB)  TX bytes:42493 (42.4 KB)

root@local-vm-ubuntu-02:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         dlinkrouter     0.0.0.0         UG    0      0        0 enp0s3
192.168.0.0     *               255.255.255.0   U     0      0        0 enp0s3
192.168.99.0    *               255.255.255.0   U     0      0        0 enp0s8
{% endhighlight %}

A 에서 B로 Ping 를 날려보면 정삭적으로 Ping 이 가는것을 확인 할 수 있다.

{% highlight bash %}
root@local-vm-ubuntu:~# ping 192.168.99.110
PING 192.168.99.110 (192.168.99.110) 56(84) bytes of data.
64 bytes from 192.168.99.110: icmp_seq=1 ttl=64 time=0.499 ms
{% endhighlight %}

#### 라우팅 정보삭제
그러면 라우팅 정보를 삭제해보겠다.

{% highlight bash %}
route del -net 192.168.99.0 netmask  255.255.255.0 dev enp0s8
{% endhighlight %}

결과는 아래와 같이 해당 라우팅정보가 삭제된다.
{% highlight bash %}
root@local-vm-ubuntu:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         dlinkrouter     0.0.0.0         UG    0      0        0 enp0s3
192.168.0.0     *               255.255.255.0   U     0      0        0 enp0s3
{% endhighlight %}

이제 ping 을 날려도 해당 호스트로 ping 이 안된다.

#### 라우팅 정보추가
그럼 라우팅 정보를 추가해보겠다.

{% highlight bash %}
route add -net 192.168.99.0 netmask  255.255.255.0 dev enp0s8
{% endhighlight %}

아래와 같이 해당 라우팅 정보가 추가된다.

{% highlight bash %}
root@local-vm-ubuntu:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         dlinkrouter     0.0.0.0         UG    0      0        0 enp0s3
192.168.0.0     *               255.255.255.0   U     0      0        0 enp0s3
192.168.99.0    *               255.255.255.0   U     0      0        0 enp0s8
{% endhighlight %}

#### 단일 호스트에 대해서 라우팅을 추가/삭제 할 때

{% highlight bash %}
route add -host 192.168.99.100 dev enp0s8
route del -host 192.168.99.100 dev enp0s8
{% endhighlight %}

#### 게이트웨이 추가, 제거
{% highlight bash %}
route add default gw 192.168.0.1 dev enp0s3
route del default gw 192.168.0.1 dev enp0s3
{% endhighlight %}

192.168.99.100으로 나가는 트래픽을 192.168.0.1 게이트웨이를 통하도록 할 때

{% highlight bash %}
route add -host 192.168.99.100 netmask 0.0.0.0 gw 192.168.0.1 dev enp0s3

root@local-vm-ubuntu:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         dlinkrouter     0.0.0.0         UG    0      0        0 enp0s3
192.168.0.0     *               255.255.255.0   U     0      0        0 enp0s3
192.168.99.0    *               255.255.255.0   U     0      0        0 enp0s8
192.168.99.100  dlinkrouter     255.255.255.255 UGH   0      0        0 enp0s3
{% endhighlight %}

192.168.99.0 네트워크로 나가는 트래픽을 192.168.0.1 게이트웨이를 통하도록 할 때

{% highlight bash %}
route add -net 192.168.99.0 netmask 255.255.255.0 gw 192.168.0.1 dev enp0s3

root@local-vm-ubuntu:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         dlinkrouter     0.0.0.0         UG    0      0        0 enp0s3
192.168.0.0     *               255.255.255.0   U     0      0        0 enp0s3
192.168.99.0    dlinkrouter     255.255.255.0   UG    0      0        0 enp0s3
192.168.99.0    *               255.255.255.0   U     0      0        0 enp0s8
192.168.99.100  dlinkrouter     255.255.255.255 UGH   0      0        0 enp0s3
{% endhighlight %}

#### 부팅과 함께 적용시키기
/etc/rc.d/rc.local 파일에 라우트 설정 내용을 추가하여 네트워크 설정을 한다.
