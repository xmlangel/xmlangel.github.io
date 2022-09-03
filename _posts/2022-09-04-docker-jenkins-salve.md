---
layout: post
title: "[docker] docker 환경에서 젠킨스(jenkins) master-slave 컨테이너 설정해서 사용하기!!"
date:   2022-09-03 23:00:00 +0900
categories: docker update
profile: kmkim.png
tags :
- docker
- jenkins
- docker-compose
---

Docker 를이용해서 Jenkins를 설정하고 master - slave 컨테이너를 설정하는 방법을 알아보고자합니다.

* 목차
{:toc}
# master 컨테이너
먼져 master docker 컨테이너를 만들어준다. jenkins 에서 공식지원하는 컨테이너를 이용해서 생성 하면 된다.

공식 DockerHub에는 설명이 없고 이전 hub에 있으니 그점은 참고해서 받으면 된다.

- [jenkins 이전 공식](https://hub.docker.com/_/jenkins)
- [jenkins 공식 dockerHub참고](https://hub.docker.com/r/jenkins/jenkins)


```
docker run -p 8088:8080 -p 50000:50000 -v /your/home:/var/jenkins_home jenkins
```
생성된 컨테이너는 8088 포트를 통해서 접속해보면 아래와 같은 화며이 나온것을 확인 할 수 있다.
![docker-jenkins-slave-001.png](/assets/images/2022-09-04/docker-jenkins-slave-001.png)

secret Key 는 shell 커맨드 창에서 확인하거나 /your/home/secrets/initialAdminPassword 에서 확인 하면 된다.
![docker-jenkins-slave-002.png](/assets/images/2022-09-04/docker-jenkins-slave-002.png)

- Key 를 입력한후에는 플러그인을 설치 해준다. 
![docker-jenkins-slave-003.png](/assets/images/2022-09-04/docker-jenkins-slave-003.png)

- 플러그인설치
![docker-jenkins-slave-004.png](/assets/images/2022-09-04/docker-jenkins-slave-004.png)

설치가 끝나고나면 id/password 를 설정해주면 기본적인 설정은 마무리된다.


![docker-jenkins-slave-005.png](/assets/images/2022-09-04/docker-jenkins-slave-005.png)
![docker-jenkins-slave-006.png](/assets/images/2022-09-04/docker-jenkins-slave-006.png)
- 어드민 사용자 생성
![docker-jenkins-slave-007.png](/assets/images/2022-09-04/docker-jenkins-slave-007.png)
- 설치 완료
![docker-jenkins-slave-008.png](/assets/images/2022-09-04/docker-jenkins-slave-008.png)

기본적인 설치가 끝났다. 

## master ssh 키 생성
자 이제 설치가 끝났다 이제 무엇을할까? 우리가 하고자 하는것은 Master 와 Slave 노드를 만들어서 사용하고자 하는것이다.

그러기위해서 master jenkins 에서 ssh 키를 생성하면된다. 

생성된 컨테이너의 이름을 확인후 ssh-keygen 을 통해서 생성하면된다.

SSH 키는 /your/home/.ssh/id_rsa.pub 에서 확인하면된다.
```
docker ps 
docker exec -it gracious_lewin ssh-keygen -t rsa
```

## master docker-compose 설정

# slave 컨테이너
## slave docker-compose 설정
# 최종 docker-compose
```
version: '3'
services:
  master:
    container_name: master
    image: jenkins/jenkins:lts
    restart: unless-stopped
    volumes:
      - ./jenkins_home:/var/jenkins_home
    ports:
      - "8082:8080"
      - "50000:50000"
    links:
      - slave01
  node:
    container_name: slave01
    image: jenkins/ssh-agent
    restart: unless-stopped
    environment:
      - JENKINS_AGENT_SSH_PUBKEY=id_rsa.pub(master 에서 생성한 키를 넣어주면됩니다.)
    volumes:
      - ./slave_jenkins_home:/var/jenkins_home

```
# Jenkins 설정
## slave node 추가
## slave java 경로설정
