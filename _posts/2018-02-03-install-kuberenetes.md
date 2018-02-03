---
layout: post
title:  "sublim 에서 vs code 로 "
date:   2017-09-17 11:20:13 +0900
categories: jekyll update
comments: true
tags:
- vscode
---

Sublime  에서 vs code 로 넘어왔다.
* 목차
{:toc}

# vscode 터미널에서 바로실행

centos 에 설치하기 위해서는 centOs 7 이상이 설치되어 있어야한다.
To configure Kubernetes with CentOS, you’ll need a machine to act as a master, and one or more CentOS 7 hosts to act as cluster nodes.

Hosts 정보

Please replace host IP with your environment.
#centos-master = 10.128.29.105
#centos-minion-1 = 10.128.29.102
#centos-minion-2 = 110.128.29.104


## repo추가

echo /etc/yum.repos.d/virt7-docker-common-release.repo

{% highlight ruby %}

[virt7-docker-common-release]
name=virt7-docker-common-release
baseurl=http://cbs.centos.org/repos/virt7-docker-common-release/x86_64/os/
gpgcheck=0
{% endhighlight %}

## 설치

Install Kubernetes, etcd and flannel on all hosts - centos-{master,minion-n}. This will also pull in docker and cadvisor.

## hosts 파일내용추가
/etc/hosts
{% highlight ruby %}

10.128.29.105 centos-master
10.128.29.102 centos-minion-1
10.128.29.104 centos-minion-2
{% endhighlight %}

4. kubernetes 환경설정
Edit /etc/kubernetes/config which will be the same on all hosts to contain:
