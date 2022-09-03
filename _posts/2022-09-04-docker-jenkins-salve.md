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
## master ssh 키 생성
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
