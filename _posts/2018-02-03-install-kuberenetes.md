---
layout: post
title:  "Centos 에서 Kuberenetes 설치하기"
date:   2018-02-3 11:11:13 +0900
categories: jekyll update
tags:
- docker
- kuberenetes
- K8s
---

* 목차

{:toc}

centos 에 설치하기 위해서는 master node 와 minion 에 모두 cent OS 7 이상이 설치되어 있어야합니다.

본글은 아래 링크를 따라하면서 만든것입니다.

오류가 있을시 아래 링크 참고하시면 될거 같습니다.

https://kubernetes.io/docs/getting-started-guides/centos/centos_manual_config/

설치할 Hosts 정보와 아이피는 아래와같다.
virtualbox 등의 아이피를 설정해주면 된다.
{% highlight ruby %}

#centos-master = 10.128.29.105
#centos-minion-1 = 10.128.29.102
#centos-minion-2 = 110.128.29.104
{% endhighlight %}
# a

그럼 본격적으로 설치를 시작해보겠다.

## repo추가

echo /etc/yum.repos.d/virt7-docker-common-release.repo

{% highlight ruby %}

[virt7-docker-common-release]
name=virt7-docker-common-release
baseurl=http://cbs.centos.org/repos/virt7-docker-common-release/x86_64/os/
gpgcheck=0
{% endhighlight %}

## 설치

## hosts 파일내용추가
/etc/hosts
{% highlight ruby %}

10.128.29.105 centos-master
10.128.29.102 centos-minion-1
10.128.29.104 centos-minion-2
{% endhighlight %}

## kubernetes 환경설정
/etc/kubernetes/config 파일을 수정해준다.

모두 기본값이고 호스트에 추가한 부분만 수정해주면 된다.
KUBE_MASTER="--master=http://centos-master:8080"

{% highlight ruby %}

# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=false"

# How the replication controller and scheduler find the kube-apiserver
KUBE_MASTER="--master=http://centos-master:8080"
{% endhighlight %}

#방화벽 해제
모든 노드에 방화벽을 해제해준다.

{% highlight ruby %}
setenforce 0
systemctl disable iptables-services firewalld
systemctl stop iptables-services firewalld
{% endhighlight %}

# Master 설정변경

/etc/etcd/etcd.conf 파일을 수정해준다.

{% highlight ruby %}
# [member]
ETCD_NAME=default
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"

#[cluster]
ETCD_ADVERTISE_CLIENT_URLS="http://0.0.0.0:2379"
{% endhighlight %}

Edit /etc/kubernetes/apiserver to appear as such:

{% highlight ruby %}
# The address on the local server to listen to.
KUBE_API_ADDRESS="--address=0.0.0.0"

# The port on the local server to listen on.
KUBE_API_PORT="--port=8080"

# Port kubelets listen on
KUBELET_PORT="--kubelet-port=10250"

# Comma separated list of nodes in the etcd cluster
KUBE_ETCD_SERVERS="--etcd-servers=http://centos-master:2379"

# Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# Add your own!
KUBE_API_ARGS=""
{% endhighlight %}

## ETCD 시작

ETCD 를시작해준다. Network overy 설정을 해주는것이고, Network overy 는 172.30.0.0 네트워크를 사용한다.

{% highlight ruby %}
systemctl start etcd
etcdctl mkdir /kube-centos/network
etcdctl mk /kube-centos/network/config "{ \"Network\": \"172.30.0.0/16\", \"SubnetLen\": 24, \"Backend\": { \"Type\": \"vxlan\" } }"
{% endhighlight %}

flannel overlay Docker network 설정을 해준다.

/etc/sysconfig/flanneld

{% highlight ruby %}

# Flanneld configuration options

# etcd url location.  Point this to the server where etcd runs
FLANNEL_ETCD_ENDPOINTS="http://centos-master:2379"

# etcd config key.  This is the configuration key that flannel queries
# For address range assignment
FLANNEL_ETCD_PREFIX="/kube-centos/network"

# Any additional options that you want to pass
#FLANNEL_OPTIONS=""
{% endhighlight %}

Start the appropriate services on master:
{% highlight ruby %}
for SERVICES in etcd kube-apiserver kube-controller-manager kube-scheduler flanneld; do
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES
done
{% endhighlight %}

# Node 설정변경

/etc/kubernetes/kubelet 설정변경

먼져 centos-minion-1 node 에서 설정을 해준다.

KUBELET_HOSTNAME 만 변경하면 되는 사하으로 크게 어려움은 없을듯.

{% highlight ruby %}

# The address for the info server to serve on
KUBELET_ADDRESS="--address=0.0.0.0"

# The port for the info server to serve on
KUBELET_PORT="--port=10250"

# You may leave this blank to use the actual hostname
# Check the node number!
KUBELET_HOSTNAME="--hostname-override=centos-minion-1"

# Location of the api-server
KUBELET_API_SERVER="--api-servers=http://centos-master:8080"

# Add your own!
KUBELET_ARGS=""
{% endhighlight %}

다음은 centos-mast-minion-2 노드에서 설정을 해준다.

{% highlight ruby %}

# The address for the info server to serve on
KUBELET_ADDRESS="--address=0.0.0.0"

# The port for the info server to serve on
KUBELET_PORT="--port=10250"

# You may leave this blank to use the actual hostname
# Check the node number!
KUBELET_HOSTNAME="--hostname-override=centos-minion-2"

# Location of the api-server
KUBELET_API_SERVER="--api-servers=http://centos-master:8080"

# Add your own!
KUBELET_ARGS=""
{% endhighlight %}

두 노드에서 모두 설절을 변경해준다.

flannel to overlay Docker network  설정변경
 /etc/sysconfig/flanneld

{% highlight ruby %}
# Flanneld configuration options

# etcd url location.  Point this to the server where etcd runs
FLANNEL_ETCD_ENDPOINTS="http://centos-master:2379"


# etcd config key.  This is the configuration key that flannel queries
# For address range assignment
FLANNEL_ETCD_PREFIX="/kube-centos/network"

# Any additional options that you want to pass
#FLANNEL_OPTIONS=""

{% endhighlight %}

각노드에서 kube-proxy 설정을 해준다.

{% highlight ruby %}

for SERVICES in kube-proxy kubelet flanneld docker; do
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES
done
{% endhighlight %}

kubectl 설정

{% highlight ruby %}

kubectl config set-cluster default-cluster --server=http://centos-master:8080
kubectl config set-context default-context --cluster=default-cluster --user=default-admin
kubectl config use-context default-context

{% endhighlight %}

# Master에서 동작확인.

{% highlight ruby %}

$ kubectl get nodes
root@localhost ~]# kubectl get nodes
NAME              STATUS    AGE
centos-minion-1   Ready     57s
centos-minion-2   Ready     54s

{% endhighlight %}

참고한 URL

- http://www.popit.kr/kubernetes-introduction/

- https://kubernetes.io/docs/getting-started-guides/centos/centos_manual_config/