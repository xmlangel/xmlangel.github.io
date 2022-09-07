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
![docker-jenkins-slave-000.png](/assets/images/2022-09-04/docker-jenkins-slave-000.png)

* 목차
{:toc}
# master 컨테이너

먼져 master docker 컨테이너를 만들어준다. jenkins 에서 공식지원하는 컨테이너를 이용해서 생성 하면 된다.

공식 DockerHub에는 설명이 없고 이전 hub에 있으니 그점은 참고해서 받으면 된다.

- [jenkins 이전 공식](https://hub.docker.com/_/jenkins)
- [jenkins 공식 dockerHub참고](https://hub.docker.com/r/jenkins/jenkins)


```
docker run -p 8088:8080 -p 50000:50000 -v /your/home:/var/jenkins_home jenkins/jenkins
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
커맨드 라인으로 실행하면 되겠지만 docker-compose 를 이용하면 여러개의 작업을 할수 있으므로 docker-compose.yaml 파일을 생성해서 master jenkins 파일을 생성해놓는다.
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
```
# slave 컨테이너
이제 슬레이브 컨테이너를 생성 할 차례다.

슬레이브 컨테이너 또한 jenkins 에서 ssh-agent 라는 이름의 이미지를 받아서 실행하면된다. 
- [jenkins/ssh-agent](https://hub.docker.com/r/jenkins/ssh-agent)

커맨드 라인 명령어로 실행하는 법은 아래와 같다. 

master 에서 id_rsa.pub 의 파일의 값을 public_key 란에 입력해주면된다.

```
docker run jenkins/ssh-agent "<public key>"
```
# 최종 docker-compose
docker-compose 를 이용해서 아래와 같이 생성해서 사용하면 기본적인 설정은 된것이다.

커맨드라인에서 publc key 로 입력한값은 docker-compose 에서 environment 에서 

JENKINS_AGENT_SSH_PUBKEY 값을 지정해 주면 동일한 결과를 얻을 수 있다.

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
      - JENKINS_AGENT_SSH_PUBKEY=public key
    volumes:
      - ./slave_jenkins_home:/var/jenkins_home
```
간단한 설정에 대한 설명은 참고해보길 바란다.

- container_name: 컨테이너의 이름
- image: 실행할 도커 이미지
- restart: unless-stopped  중지되면 재실행
- volumes : local pc 와 docker container 의 디스크 연결
- ports: open할 포트
- link:slave01 master 에서 연결할 컨테이너의 이름(master 에서 ip 가 아닌 여기에 설정된 이름으로 접속가능하게 해줌)
- environment : 환경 설정값

# Jenkins 설정
설치가 완료되었으니 이 master / slave 연결을 해주면 됩니다.

Jenkins Slave 연결을위해서는 Slave 컨테이너에 Java위치를 알아야 합니다. 

Jenkins 에서 제공한 이미지에는 이미 Java 가 설치 되어 있습니다. 

컨테이너에서 Java 위치를 미리 알아놓습니다. 

위에서 생성한 docker-compose 를 이용한다면 slave01에 접속해서 확인이 가능할것입니다.

```
docker exec -it slave01 which java

```

설정된 위치는 아래와 같음을 확인 할 수 있습니다.

```
/opt/java/openjdk/bin/java 
```
![docker-jenkins-slave-009.png](/assets/images/2022-09-04/docker-jenkins-slave-009.png)

연결에 필요한 java 경로를 확인하였으니 이제 Jenkins 메뉴를 통해서 Slave 추가를 해 보도록 하겠습니다.

## Slave Agent node 추가
Master 젠킨스가 slave 젠킨스를 인식하 하도록 Slave Agent node 를 추가해줍니다.

Manage Jenkins 페이지를 진입해 '신규 노드' 생성 항목에서 노드'(Manage nodes and Clouds New node) 를 선택해 관련 정보들을 입력해줍니다. 

![docker-jenkins-slave-010.png](/assets/images/2022-09-04/docker-jenkins-slave-010.png)
- Node name : node로 사용할 이름을 입력해준다. (ex: slave)
- permanent Agent : permant Agent 타입을 선택해준다.

입력 완료후 다음 정보들을 입력해줍니다.
![docker-jenkins-slave-011.png](/assets/images/2022-09-04/docker-jenkins-slave-011.png)
- name : 이름
- Description : 설명
- Number of executors : 한번에 실행할수 있는 수
- Remote root directory : Agent 가 실행될 디랙토리 경로
- Labels : 라벨
- Usage : Use this node as much as possible 
- Launch method : Launch agents via SSH - ssh 를 이용할것이기에 이것을 선택해준다.
- Host : docker-compose 에서 지정해준 이름값 
- Credentials : 아래에서 설정한 것을 선택해준다. ssh-key 생성한 값을 넣어주면된다.
- Host key Verification Stratery : Non verifying Verification Strategy
![docker-jenkins-slave-012.png](/assets/images/2022-09-04/docker-jenkins-slave-012.png)

## slave java 경로설정
Agent 를 구동하려면 Java 경로를 입력해주어야 한다. 
위에서 가져온 경로를 입력해준다.
![docker-jenkins-slave-013.png](/assets/images/2022-09-04/docker-jenkins-slave-013.png)
 
 ## master - slave 연결
 설정이 완료되고나면 연결이 됩니다.만약연결이 안될경우 Launch agent 를 눌러서 열결을 해줄수 있습니다.
![docker-jenkins-slave-014.png](/assets/images/2022-09-04/docker-jenkins-slave-014.png)

Log 를 보면 정상연결된것을 확인 할 수 있습니다.
![docker-jenkins-slave-015.png](/assets/images/2022-09-04/docker-jenkins-slave-015.png)

Dashboar와 Queue 영역에서 두개의 노드가 이용 가능한 상태임을 확인할수 있습니다.
![docker-jenkins-slave-016.png](/assets/images/2022-09-04/docker-jenkins-slave-016.png)

# 맺음말
간단하게 Jenkins 를 설치후 Master 와 node 를 연결해보았습니다. 

감사합니다.

끝..
