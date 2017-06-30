---
layout: post
title:  "Docker registry 로 개인 Docker 구축해보기"
date:   2017-03-11 08:49:43 +0900
categories: jekyll update
---
* 목차
{:toc}

도커를 이용하면서 도커허브에 올리면 좋겠지만 내부에서 이용 하려고 할때 Open할수 없는 정보들이 있을수 있다.

하지만 private registry 를 이용하면 어느정도는 극복할수 있다.

사용할 환경은 
- Vagrant
- docker
- docker-compoose
- Ubuntu 14.04

vagrant 를 이용하면 쉽게 구성이 가능하다.

# [vagrant 설정](#vagrant)

{% highlight ruby %}
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "opscode-ubuntu-14.04"
  config.vm.network "private_network", ip: "11.168.20.1"
  config.vm.network "public_network", bridge: [
    "en0: Wi-Fi (AirPort)"
    ]
  #vagrant 에서 data 폴더를 공유해서사용 
  config.vm.synced_folder "./data", "/vagrant_data"

  config.vm.provision "shell", inline: <<-SHELL
   #한글 및 사용편위를 위한 패키지설치
   sudo sed -i 's/us.archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list
   sudo sed -i 's/security.archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list
   sudo apt-get update
   sudo apt-get install -y vim screen curl
   
   #Docker 설치
   sudo apt-get install apt-transport-https ca-certificates
   sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
   echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main">/etc/apt/sources.list.d/docker.list
   sudo apt-get update
   sudo apt-get install docker-engine -y
   sudo service docker start

   #Docker Compose 설치
   sudo apt-get -y install python-pip
   sudo pip install docker-compose

   #apache2-utils에 있는 htpasswd 를 사용하기위한 패키지 다운로드
   apt-get -y install apache2-utils

   SHELL
end
{% endhighlight %}

ubuntu의 다른 버전이라면 docker.list파일에 아래의 내용으로 변경해서 설치하면된다.

{% highlight shell %}
### ubuntu 12.04
deb https://apt.dockerproject.org/repo ubuntu-precise main

### ubuntu 14.04
deb https://apt.dockerproject.org/repo ubuntu-trusty main

### ubuntu 15.10
deb https://apt.dockerproject.org/repo ubuntu-wily main

### ubuntu 16.04
deb https://apt.dockerproject.org/repo ubuntu-xenial main
{% endhighlight %}

# docker-compose.yml 에 nginx 와 registry 설정을한다.

vagrant 에서 vagrant_data 로 연결하였으므로, vagrant_data 에서 작업을 한다.

작업할 디랙토리 구조느 아래와 같다.

{% highlight shell %}
root@vagrant:/vagrant# cd /vagrant_data
root@vagrant:/vagrant_data# tree
.
|-- data
|-- docker-compose.yml
|-- nginx
    |-- registry.conf

{% endhighlight %}

data 디랙토리와 nginx 디랙토리를 만들어준다.

{% highlight shell %}
root@vagrant:/vagrant_data# mkdir data
root@vagrant:/vagrant_data# mkdir nginx
{% endhighlight %}

data 디랙토리는 registry의 data 경로로 이용하고, nginx 는 nginx 설정파일이 저장될 위치이다.

- docker-compose.yml
{% highlight ruby %}
nginx:
  image: "nginx:1.9"
  ports:
    - 5043:443
  links:
    - registry:registry
  volumes:
     - ./nginx/:/etc/nginx/conf.d

registry:
    image: "registry:2"
    ports:
        - 127.0.0.1:5000:5000
    environment:
        REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /data
    volumes:
        - ./data:/data

{% endhighlight %}

- registry.conf

{% highlight ruby %}
upstream docker-registry {
  server registry:5000;
}

server {
  listen 443;
  server_name myregistrydomain.com;

  # SSL
  # ssl on;
  # ssl_certificate /etc/nginx/conf.d/domain.crt;
  # ssl_certificate_key /etc/nginx/conf.d/domain.key;

  # disable any limits to avoid HTTP 413 for large image uploads
  client_max_body_size 0;

  # required to avoid HTTP 411: see Issue #1486 (https://github.com/docker/docker/issues/1486)
  chunked_transfer_encoding on;

  location /v2/ {
    # Do not allow connections from docker 1.5 and earlier
    # docker pre-1.6.0 did not properly set the user agent on ping, catch "Go *" user agents
    if ($http_user_agent ~ "^(docker\/1\.(3|4|5(?!\.[0-9]-dev))|Go ).*$" ) {
      return 404;
    }

    # To add basic authentication to v2 use auth_basic setting plus add_header
    # auth_basic "registry.localhost";
    # auth_basic_user_file /etc/nginx/conf.d/registry.password;
    # add_header 'Docker-Distribution-Api-Version' 'registry/2.0' always;

    proxy_pass                          http://docker-registry;
    proxy_set_header  Host              $http_host;   # required for docker client's sake
    proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
    proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header  X-Forwarded-Proto $scheme;
    proxy_read_timeout                  900;
  }
}
{% endhighlight %}
docker-compose 를 이용해서 docker 를 띄운후 결과를 확인해본다.

- registry 에서 확인결과
{% highlight shell %}
root@vagrant:/vagrant_data# docker-compose up
root@vagrant:/vagrant_data# curl http://localhost:5000/v2/

{% endhighlight %}

{% highlight shell %}
Output
{}
{% endhighlight %}

- nginx에서 확인결과

{% highlight shell %}
root@vagrant:/vagrant_data# docker-compose up
root@vagrant:/vagrant_data# curl http://127.0.0.1:5043/v2/

{% endhighlight %}

{% highlight shell %}
Output
{}
{% endhighlight %}

이제 정상적으로 동작하는것을 확인해보았다.

그럼 한번 Push 를 해보겠다.

내부에서 테스트를 해보려면.

{% highlight shell %}
$ sudo docker run hello-world
$ sudo docker tag hello-world 127.0.0.1:5043/hello-world
$ sudo docker push 127.0.0.1:5043/hello-world
{% endhighlight %}

다른 클라이언트에서 접속해서하려면.(vagrant 이므로 11.168.20.1 로 아이피가 지정되어있으므로 해당 아이피로 host 머신에서 접속테스트해보면된다.)

{% highlight shell %}
$ sudo docker run hello-world
$ sudo docker tag hello-world 11.168.20.1:5043/hello-world
$ sudo docker push 127.0.0.1:5043/hello-world
$ sudo pull 11.168.20.1:5043/hello-world
{% endhighlight %}

## Setting Up Authentication
누구나 접근이 가능하게 하면 이또한 문제 그래서 htpasswd utlity 를 이용해서 접속하게 하는 방법을 해보겠다.


{% highlight shell %}
cd ~/docker-registry/nginx
htpasswd -c registry.password USERNAME
{% endhighlight %}

Username을 입력후 비빌번호를 입력해준다.
그런후 

registry.conf를 변경해준다. 이미 위에서 입력한내용을 주석으로 풀어준다.
아래 내용의 주석을 풀어주면된다.

{% highlight shell %}
# To add basic authentication to v2 use auth_basic setting plus add_header
auth_basic "registry.localhost";
auth_basic_user_file /etc/nginx/conf.d/registry.password;
add_header 'Docker-Distribution-Api-Version' 'registry/2.0' always;
{% endhighlight %}

그런후 다시 실행해주면 인증이 필요하다고 한다.

{% highlight shell %}
root@vagrant:/vagrant_data/#docker-compose down
root@vagrant:/vagrant_data/#docker-compose up -d 
root@vagrant:/vagrant_data# curl http://localhost:5043/v2/
<html>
<head><title>401 Authorization Required</title></head>
<body bgcolor="white">
<center><h1>401 Authorization Required</h1></center>
<hr><center>nginx/1.9.15</center>
</body>
</html>
{% endhighlight %}

생성한 아이디와 패스워드를 입력하면 정상적으로 되는것을 확인할수 있다.

{% highlight shell %}
root@vagrant:/vagrant_data# curl http://USERNAME:PASSWORD@localhost:5043/v2/
{}%
{% endhighlight %}

https  설정까지는 현재까지는 필요없어 

일단 http 를 통해 사용자인증이 되는 환경까지는 구성됐다.

이제 이용하면 될것 같다.. 

https 는 다음을 위해 남겨놓고 오늘은 여기까지... 


#### 참고자료

[How To Set Up a Private Docker Registry on Ubuntu 14.04
](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-14-04)

<!-- http://gyus.me/?p=546 -->

<!-- {% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}
 -->