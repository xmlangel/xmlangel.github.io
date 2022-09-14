---
layout: post
title: "[jenkins] Free style job"
date:   2022-09-14 23:00:00 +0900
categories: jenkins update
profile: kmkim.png
tags :
- jenkins
---

Jenkins 의 JOB 중에 Free style Job 에 대해서 알아보고자 합니다. 

Free Style Job 의 경우 손쉽게 Jenkins Job 을 화면에서 제공하는 가이드에 따라서 작성을 해볼수 있습니다.

본 문서를 작성 할당시의 Jenkins 버전은 2.346.3 버전입니다. 버전마다화면들은 다를 수 있지만 기본 컨셉은 동일합니다. 참고하시기바랍니다.


* 목차
{:toc}

# Job 

Job 이란 Jenkins 에서 실행되는 각각의 작업들을 의미합니다.

사용자는 job을 생성하고 해당 job 에서 수행할 작업을 정의 할수 있습니다.

간단한게 job Type 들을 설명하자면

1. Freestyle project  : 과거부터 현재까지 사용되는 Jenkins job의 근간이 되는 프로젝트입니다. JENKINS 에서 설정들을 하고 설정된값들로 실행되게 해주는 프로젝트입니다. 

2. Pipeline : 이름에서 볼수 있는것처럼 파이프라인 타입은 파이프라인 생성을 담당합니다. Jenkins DSL을 사용해 코드를 작성함으로써 파이프라인을 생성할수 있게 해줍니다. 파이프라인 방식은 스크립트 방식과 DSL 인 서술적인 방식으로 파이프라인스크립트를 작성할 수 있습니다. Jenkinsfile을 빌드 스크립트로 활용하게 됩니다.

3. Multibranch Pipeline : Pipeline 형식이지만 Jenkinsfile을 포함하고 있는 새로운 브랜치가 프로젝트에 생성되면 Jenkins는 자동으로 해당 브랜치를 위핸 새로운 Jenkins프로젝트를 생성해주어 여러 브랜치들을 하나의 프로젝트로 관리 할수 있습니다.

Freestyle Project 는 웹 기반의 인터페이스에 종속되어 있어서 화면에서 제공하는 버튼들과 기능들을  정해진 흐름에 따라 이용했으나 

Pipeline Project 는 스텝의 순서나 Job의 순서가 변경되는 등 워크플로우가 변경되면 텍스트 기반에서 쉽게 변경할수있게 하여 파이프라인을 코드로 관리해서 하는 방식으로 변경해나가는 추세입니다.


## Job 만들기
job 을 만들려면 좌측 상단의 New Item 메뉴를 누르면됩니다.

![jenkins-job-00.jpg](/assets/images/2022-09-14/jenkins-job-00.jpg)

이름을 입력하고 JOB 의 타입을선택해줍니다.

간단하게 설명하기 위해 가장 기본이 되는 Freestyle project를 만들어보겠습니다.

![jenkins-job-00.jpg](/assets/images/2022-09-14/jenkins-job-01.jpg)





끝..
