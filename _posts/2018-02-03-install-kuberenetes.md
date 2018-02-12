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

centos 에 설치하기 위해서는 master node 와 minion 에 모두 cent OS 7 이상이 설치되어 있어야합니다.

본글은 아래 링크를 따라하면서 만든것입니다.

오류가 있을시 아래 링크 참고하시면 될거 같습니다.

https://kubernetes.io/docs/getting-started-guides/centos/centos_manual_config/

설치할 Hosts 정보와 아이피는 아래와 같습니다.

# Kuberenetes 구성
Kubernetes 구성은 아래와 같다.
- Kubernetes master
- Kubernetes nodes
- etcd
- Overlay network(flannel)

Kubernetes master 는 Http 또는 Https 를 통해서 etcd 로 접속해서 데이터를 저장하고, Flannel 을 통해서 접근하고,
Kubernetes nodes 는 Kubernetes maste 로 부터 명령을 받고, 상테를 전송하는 구조 인듯.

![Kuberneties]({{ site.url }}/assets/images/Kubernetes-01.png){: width="100%" height="100%"}

 - etcd

```
etcd는 간단하게 키체인을 저장하는 저장소와 같은 것으로

여러대의 OS가 클러스터로 구성되어 있는 상황에서 

하나의 OS 인스턴스를 리더로 하여, 

한곳에서 키 값이 변경될 경우 약 1초에 1000개의 키를 동기화 할 수 있도록 빠른 서비스를 제공합니다.

일반적으로 etcd 는 기본 컨트롤러로 제공되는 etcdctl을 이용해서 기능 사용이 가능하다고 한다.

etcd 웹 페이지 : https://github.com/coreos/etcd

```
 - Flannel

```
Flannel is a simple and easy way to configure a layer 3 network fabric designed for Kubernetes
https://github.com/coreos/flannel

```

구성은 VirtualBox 를 이용해서 할예정이고, 아래와 같은 아이피는 아래와 같은 설정으로 구성했다.

{% highlight ruby %}

#centos-master = 10.128.29.105
#centos-minion-1 = 10.128.29.102
#centos-minion-2 = 110.128.29.104
{% endhighlight %}

# 설치

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

# 동작확인.

## Component 상태
{% highlight ruby %}
# kubectl get cs
NAME                 STATUS    MESSAGE              ERROR
controller-manager   Healthy   ok
scheduler            Healthy   ok
etcd-0               Healthy   {"health": "true"}
{% endhighlight %}


## Node 상태
{% highlight ruby %}

# kubectl get nodes
NAME              STATUS    AGE
centos-minion-1   Ready     57s
centos-minion-2   Ready     54s
{% endhighlight %}

Node 의 Capacity 확인

{% highlight ruby %}
# kubectl get nodes -o json | jq '.items[] | {name: .metadata.name, capacity: .status.capacity}'
{
  "name": "centos-minion-1",
  "capacity": {
    "alpha.kubernetes.io/nvidia-gpu": "0",
    "cpu": "4",
    "memory": "8167736Ki",
    "pods": "110"
  }
}
{
  "name": "centos-minion-2",
  "capacity": {
    "alpha.kubernetes.io/nvidia-gpu": "0",
    "cpu": "4",
    "memory": "8167736Ki",
    "pods": "110"
  }
}
{% endhighlight %}

- jq 가 없을 경우 아래 명령어로 설치가능

{% highlight ruby %}
wget -O jq https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64
chmod +x ./jq
cp jq /usr/bin
{% endhighlight %}

## Master iptables

{% highlight ruby %}

# iptables -t nat -S
-P PREROUTING ACCEPT
-P INPUT ACCEPT
-P OUTPUT ACCEPT
-P POSTROUTING ACCEPT

{% endhighlight %}

## Node iptables

{% highlight ruby %}
# iptables -t nat -S
-P PREROUTING ACCEPT
-P INPUT ACCEPT
-P OUTPUT ACCEPT
-P POSTROUTING ACCEPT
-N DOCKER
-N KUBE-MARK-DROP
-N KUBE-MARK-MASQ
-N KUBE-NODEPORTS
-N KUBE-POSTROUTING
-N KUBE-SEP-3X2QJUW2ZWG6VVDC
-N KUBE-SERVICES
-N KUBE-SVC-NPX46M4PTMTKRN6Y
-A PREROUTING -m comment --comment "kubernetes service portals" -j KUBE-SERVICES
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A OUTPUT -m comment --comment "kubernetes service portals" -j KUBE-SERVICES
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 172.30.94.0/24 ! -o docker0 -j MASQUERADE
-A POSTROUTING -m comment --comment "kubernetes postrouting rules" -j KUBE-POSTROUTING
-A DOCKER -i docker0 -j RETURN
-A KUBE-MARK-DROP -j MARK --set-xmark 0x8000/0x8000
-A KUBE-MARK-MASQ -j MARK --set-xmark 0x4000/0x4000
-A KUBE-POSTROUTING -m comment --comment "kubernetes service traffic requiring SNAT" -m mark --mark 0x4000/0x4000 -j MASQUERADE
-A KUBE-SEP-3X2QJUW2ZWG6VVDC -s 10.128.29.105/32 -m comment --comment "default/kubernetes:https" -j KUBE-MARK-MASQ
-A KUBE-SEP-3X2QJUW2ZWG6VVDC -p tcp -m comment --comment "default/kubernetes:https" -m recent --set --name KUBE-SEP-3X2QJUW2ZWG6VVDC --mask 255.255.255.255 --rsource -m tcp -j DNAT --to-destination 10.128.29.105:6443
-A KUBE-SERVICES -d 10.254.0.1/32 -p tcp -m comment --comment "default/kubernetes:https cluster IP" -m tcp --dport 443 -j KUBE-SVC-NPX46M4PTMTKRN6Y
-A KUBE-SERVICES -m comment --comment "kubernetes service nodeports; NOTE: this must be the last rule in this chain" -m addrtype --dst-type LOCAL -j KUBE-NODEPORTS
-A KUBE-SVC-NPX46M4PTMTKRN6Y -m comment --comment "default/kubernetes:https" -m recent --rcheck --seconds 10800 --reap --name KUBE-SEP-3X2QJUW2ZWG6VVDC --mask 255.255.255.255 --rsource -j KUBE-SEP-3X2QJUW2ZWG6VVDC
-A KUBE-SVC-NPX46M4PTMTKRN6Y -m comment --comment "default/kubernetes:https" -j KUBE-SEP-3X2QJUW2ZWG6VVDC

{% endhighlight %}

# 첫 삽뜨기
Master 에서 먼저 정상적으로 동작하는지 확인해본다.
```
# kubectl cluster-info

Kubernetes master is running at http://localhost:8080
```

만약 정상실행이 되고 있지 않으면 실행해준다.

```
/etc/init.d/kubernetes-master start.

```
node 가 정상적으로 실행되고 있는지 확인.
```
# kubectl get nodes
NAME              STATUS    AGE
centos-minion-1   Ready     3d
centos-minion-2   Ready     3d
```
실행되고 있지 않으면 node 에서 아래 명령어들을 실행해준다.

```
service docker start 
service kubernetes-node start
```

모두 정상적으로 실행되고 있다. 

이제 도커 레지트리에서 정상적으로 hub.docker.io 에서 받아보는지 Node 에서 테스트 해보겠다.

```
# docker pull nginx
Using default tag: latest
Trying to pull repository docker.io/library/nginx ...
latest: Pulling from docker.io/library/nginx
e7bb522d92ff: Pull complete
6edc05228666: Pull complete
cd866a17e81f: Pull complete
Digest: sha256:285b49d42c703fdf257d1e2422765c4ba9d3e37768d6ea83d7fe2043dad6e63d
```
잘받아진다.
private registry 를 이용하려면 아래 경로에 로그인 정보를 설정해준다.

```
# put the credential of docker registry
$ cat /var/lib/kubelet/.dockercfg
{
"<docker registry endpoint>": {
"auth": "SAMPLEAUTH=",
"email": "noreply@sample.com"
}
}
```

## Nginx 실행

실행은 아래 와 같은 형식으로 해준다.
```
kubectl run <replication controller name> --image=<image name> --replicas=
<number of replicas> [--port=<exposing port>]
```
자 이제 실행한다.

my-first-nginx 라는 이름으로 deploryment 를 생성하고 80 port 를 열어준다.

```
# Pull the nginx image and run with 2 replicas, and expose the container port 80
# kubectl run my-first-nginx --image=nginx --replicas=2 --port=80 
deployment "my-first-nginx" created
```

정상적인 경우 아래와 같이 deployments 와 pods 를 확인 가능하다.

```
# kubectl get deployments
NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
my-first-nginx   2         2         2            2           7m
```

```
# kubectl get pods
NAME                              READY     STATUS    RESTARTS   AGE
my-first-nginx-3504586902-ht4dx   1/1       Running   0          13m
my-first-nginx-3504586902-nc9wk   1/1       Running   0          13m
```



# 오류해결

- No resources found.

kubectl get pods 실행시 


ServiceAccount Account 를 삭제해준다.

```
$ cat /etc/kubernetes/apiserver
find the “KUBE_ADMISSION_CONTROL="--admission_control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"

second: delete "ServiceAccount"
finnaly: restart kube-apiserver service

you try "kubectl get pods"
```

- redhat-ca.crt error

kubectl run 이 올라오지 않고, image pull failed 발생시

https://github.com/candlepin/subscription-manager/tree/master/etc-conf/ca

```
Error syncing pod, skipping: failed to "StartContainer" for "POD" with ErrImagePull: "image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)"


```

참고한 URL

- http://www.popit.kr/kubernetes-introduction/

- https://kubernetes.io/docs/getting-started-guides/centos/centos_manual_config/