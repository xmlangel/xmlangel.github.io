---
layout: post
title:  "virtualenv로 Pydev 와 Django 설정 하기"
date:   2017-08-12 00:20:13 +0900
categories: etc update
comments: true
tags:
- PyDev
- virtualenv
- Python
---

Eclipes 플러그인인 PyDev 를 이용한 Django 설정을 하는 법입니다.

* 목차
{:toc}


자주 설정하지 않아 한번 설정할때마다 여기저기 검색하는 시간이 오래걸리는 이상한 현상....설정1시간 작업10분...

다음의 설정 시간을 줄이기위해 기록해놓는다.

# virtualenv 설정
virtualenv 는 가상의 python 환경을 만들어줌으로써, 독림된 python 환경을 이용할때 이용하는거 같다. 

테스트 환경과 운영환경의 버전이 다르거나 할때 오류가 발생하니 버전이 달라 동일한 환경을 만들거나 할때 유용할듯..

자세한건 [Virtualenv](https://virtualenv.pypa.io/en/stable/) 여기로

## virtualenv 설치
설치는 pip 로 설치하면 간단히 설치된다.

{% highlight ruby %}
pip install virtualenv
{% endhighlight %}

virtualenv라는 폴더를 생성해 여기에 자체 파이썬 및 pip 를 저장하고, 파이선 패키지를 설치하기 위한 위치도 저장한다.

디렉토리를 만들고 virtualenv 명령을 이용해서 가상의 환경을 만들어준다.
여기서는 python3.5 버전을 python3.5 디랙토리에 생성한다.

{% highlight ruby %}
virtualenv --python=python3.5 python3.5
{% endhighlight %}

### activate
디랙토리를 만들고 설정을 완료하면 이제 이용이 가능하다. 이용을 하려면 activate 를 해줘야 한다.

{% highlight ruby %}
. python3.5/bin/activate

{% endhighlight %}
설정을 완료하면 아래와 같이 ()로 표시되서 변경된것을확인 가능하다
{% highlight ruby %}
 (python3.5) $ 
{% endhighlight %}
## 다른방법(virtualEnv Wrapper의 설치
virtual Env 의 다른방법으로는 Virtualenvwrapper 를 이용하는 방법도 있다.

아래와 같이 설치해주면 virtualenv 도 함께 설치된다.

{% highlight ruby %}
pip install virtualenvwrapper
{% endhighlight %}

가상 환경을 저장할 디렉토리를 생성하고, 환경변수에 등록하면된다.

{% highlight ruby %}

mkdir ~/.python_virtual_envs
 
# 아래 내용을 ~/.bashrc 에 마지막에 저장한다.
export WORKON_HOME=~/.python_virtual_envs
source /usr/local/bin/virtualenvwrapper.sh # 각종 PATH 등을 설정해줌.
{% endhighlight %}

### 가상 환경 생성
{% highlight ruby %}
mkvirtualenv 가상환경이름 # 기본 생성
mkvirtualenv --python=python2.6 가상환경이름 # 특정 파이썬 버전 지정해서 생성
{% endhighlight %}

-  가상환경을 생성/확성화하면 $VIRTUAL_ENV 환경 변수에 디렉토리명이 들어간다.

### 특정 가상환경 선택
{% highlight ruby %}
workon 가상환경이름 # <tab>키 누르면 자동 완성됨
{% endhighlight %}

### 가상환경 종료
{% highlight ruby %}

deactivate
{% endhighlight %}

### 가상환경 디렉토리로 이동
{% highlight ruby %}

cdvirtualenv
{% endhighlight %}

### 현재 가상환경의 써드 파티 패키지 전체 삭제
{% highlight ruby %}

wipeenv
{% endhighlight %}

### 가상환경 목록
{% highlight ruby %}

lsvirtualenv
{% endhighlight %}

### 가상환경 삭제
{% highlight ruby %}

rmvirtualenv
{% endhighlight %}

### 모든 가상환경에 대한 명령 실행
{% highlight ruby %}

# allvirtualenv command with arguments
allvirtualenv pip install -U pip
{% endhighlight %}

# Django 설치
Django 는 python 에서 유명한 framework 이다.
설치역시 pip 로 가능하다.

{% highlight ruby %}
pip install django
{% endhighlight %}

# PyDev 설치
## PyDev plugin 설치
Eclipes 마켓이나 url경로를 넣어서 설치 가능하다.

Help -> Install New Software PyDev 사이트를 추가 한후 설치하면 된다. ( Location은 http://pydev.org/updates )

![pydev-01]({{ site.url }}/assets/images/pydev-01.png){: width="100%" height="100%"}

설정한후 pydev 체크후 다운로드 받아 설치 하면된다.

![pydev-02]({{ site.url }}/assets/images/pydev-02.png){: width="100%" height="100%"}

설치완료후 재시작하면 PyDev 사용이 가능하다.
## Interpreter 설정
환경설정>PyDev>Interpreters>Python Interpreter 설정에서 인터프리터 설정을 해준다.

![pydev-03]({{ site.url }}/assets/images/pydev-03.png){: width="100%" height="100%"}

virtualenv 폴더의 bin 경로를 지정해준다.
![pydev-04]({{ site.url }}/assets/images/pydev-04.png){: width="100%" height="100%"}
virtualenv 폴더의 bin 경로를 지정해준다.
![pydev-05]({{ site.url }}/assets/images/pydev-05.png){: width="100%" height="100%"}

자동으로 python들을 잡아준다.
![pydev-06]({{ site.url }}/assets/images/pydev-06.png){: width="100%" height="100%"}

# Django Project 생성
Project 를 생성하고 interpreter 설정을해주면 vittualenv 환경으로 된 Django 프로잭트이용이 가능하다.
![pydev-07]({{ site.url }}/assets/images/pydev-07.png){: width="100%" height="100%"}



