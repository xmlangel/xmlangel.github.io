---
layout: post
title:  "Ubnutu Network 설정"
date:   2017-07-20 10:50:13 +0900
categories: linux update
comments: true
tags :
- Ubuntu
- Network
- IP
---

Ubuntu 16.04 에서 네트워크 설정하는 법을 잘 생각이 나지 않아 적어놓는다...
* 목차
{:toc}

모든 검증은 ubuntu 16.04 에서 했다. 그리고 권한은 root 권한을 가지고 작업을 해야 한다.

먼저 어느 네트워크 카드가 붙어있는지 확인 해보자
{% highlight bash %}
ip link show
{% endhighlight %}

{% highlight ruby %}
root@local-vm-ubuntu:~# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:fd:dc:d4 brd ff:ff:ff:ff:ff:ff
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:8f:3c:58 brd ff:ff:ff:ff:ff:ff
{% endhighlight %}

# Ip Setting

우분투를 처음 설치하면 다른 리눅스 배포판과 마찬가지로 유동아이피로 설정되어 있다.

아이피를 변경하기 위해서는 아래 파일을 변경해야 한다.

## interface 변경

{% highlight bash %}
/etc/network/ interfaces
{% endhighlight %}

### DHCP 설정
{% highlight bash %}
auto eth0
iface eth0 inet dhcp
{% endhighlight %}
만약 2개의 NIC 를 이용하면 하나의 NIC 에는 Default gateway 설정을 해준다.

{% highlight bash %}
auto eth0
iface eth0 inet dhcp
post-up route add default gw 192.168.0.1

auto eth1
iface eth1 inet dhcp

{% endhighlight %}


### 고정아이피 설정

{% highlight bash %}
auto eth0
iface eth0 inet static
address xxx.xxx.xxx.xxx
netmask xxx.xxx.xxx.xxx
broadcast xxx.xxx.xxx.xxx
gateway xxx.xxx.xxx.xxx
dns-nameservers xxx.xxx.xxx.xxx

{% endhighlight %}


## 네트워크 설정 재시작
설정파일을 편집했으면 네트워크를 재시작해야 한다.


{% highlight bash %}
sudo /etc/init.d/networking restart

{% endhighlight %}

ifconfig 명령어를 통해 정상적으로 변경되었는지 확인한다. (변경이 안되었으면 reboot 후 다시 확인)
