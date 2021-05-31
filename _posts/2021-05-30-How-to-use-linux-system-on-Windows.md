---
layout: post
title:  "윈도우에서 Linux 시스템 이용 하기 (WSL)"
date:   2021-05-31 10:36:15
author: 김광명
categories: windows update
profile: kmkim.png
tags:
- wsl
- ubuntu
---

윈도우에서도 WSL 이라는 기능을 이용해서 리눅스를 이용할수 있다. 
![wsl-ubuntu-00.jpg](/assets/images/2021-05-31/wsl-ubuntu-00.jpg)

* 목차
{:toc}

# 설치는 어떻게 하느냐 ?

Windows 10 Pro 이상 부터 WSL(Windows Susystem for Linux)를 사용할 수 있다고한다.

내가 자주 이용하는 Ubuntu 를 설치해보겠다.


## WSL 설치 방법

1. PowerShell을 관리자 권한으로 실행하고 아래 명령어를 실행한다.
~~~
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
~~~
2. WSL이 설치가 완료되면 재부팅 하면됨.

3. 마이크로소프트 스토어에 들어가 Ubuntu를 찾아 설치한다.

![wsl-ubuntu-01.jpg](/assets/images/2021-05-31/wsl-ubuntu-01.jpg)

이제 집에서 간단하게 리눅스를 간단하게 이용할 수 있다.

회사 맥북을 가져오지 않고 집에서 간단하게 리눅스를 이용할 수 있게 되었다.
 (사실 이용하고 있었지만. 요즘 심심해서 다시 Jekyll 을 보고 있어서 다시설치함.)

만약 윈도우에 루비설치하고 파이썬설치하고 하고싶다면 예전에 작성한 내용을 참고해보시길(2015 년도에 작성했던거라 동작안할수도있음.)

[Jekyll 윈두우에 설치해서 사용하기](https://xmlangel.github.io/Install-Jekyll-on-Windows/)

자 그럼 설치가 되었을것이다. 

## 저장소(repository) 변경하기

ubuntu 커맨드에서 apt-get update 를 하면 상당히 느릴것이다.

왜냐? archive.ubuntu.com 기본 레파지토리 경로가 ubuntu.com으로 되어있어서 느리다.

한국미러 사이트를 이용하시길..

예전에 ftp.daum.net 이였던게 mirror.kakao.com 으로 바겼더군..

암튼. 우선 아래와 같이 파일을 연다.

~~~
sudo vi /etc/apt/sources.list
~~~

vi의 치환기능을 이용해 한번에 변경한다.

~~~
:%s/kr.archive.ubuntu.com/ftp.daum.net/g

:%s/security.ubuntu.com/ftp.daum.net/g
~~~

다완료 되면 업데이트와 업그레이드를 실행한다.

~~~
sudo apt-get update
~~~

필요하다면 upgrade 도 해준다.(작업이 상당히 오래걸린다 아래 작업은 해도되고 안해도된다.)

~~~
sudo apt-get upgrade
~~~

다 완료되면 linux 버전을 확인할수 있을 것이다.

~~~
cat /etc/lsb-release

또는

cat /etc/issue

~~~

![wsl-ubuntu-02.jpg](/assets/images/2021-05-31/wsl-ubuntu-02.jpg)


# 쓸만한팁

## 자 윈도우에 설치했으니 윈도우에서 찾아가기도 해야겠지?

윈도우에서 찾아가는 경로는 아래에 에있다.
안에 들어가면 리눅스파일경로들을 볼수있을것이다.

~~~
C:\Users\유저이름\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState\rootfs
~~~

## 권한에러 날경우(permission denied)

윈도우 시스템에서 파일을 만들어서 리눅스 시스템에 넣고 리눅스에서 그 경로를 찾아가며 권한관련 에러가 난다.

이문제를 해결하기위해서는 리눅스에서 권한을 추가해주면된다.

(윈도우랑 리눅스 같이쓰려면 권한관련 내용이 좀 복잡한듯)

![wsl-ubuntu-03.jpg](/assets/images/2021-05-31/wsl-ubuntu-03.jpg)

~~~
sudo chmod -R a+rwx /path/to/folder 
~~~

자세한 내용은 아래 링크를참고.

[How to Give All Permissions in Ubuntu](https://smallbusiness.chron.com/give-permissions-ubuntu-33174.html)

이제 그냥 이용하면된다...

근데 오늘도 이용하긴 글른듯.. 

왜 내가 다 설치하고나면 윈도우는항상 업데이트가 뜨는지 모르겠다...

그래서 윈도우를 안쓰는건가? 

아니면 맥을 너무오래써서 윈도우랑 안친해서 그런건진.. 

기본팁은 여기까지.


## MS 공식설명서
정말로 정말로 내가 쓴글에 신뢰가 가지 않는다면 MS의 공식사이트를 참고하는게 빠를수도..

[MS WSL 공식설명서 ](https://docs.microsoft.com/ko-kr/windows/wsl/install-win10)

그럼 오늘은 여기까지..