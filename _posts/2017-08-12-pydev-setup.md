---
layout: post
title:  "virtualenv로 Pydev 와 Django 설정 하기"
date:   2017-08-12 00:20:13 +0900
categories: jekyll update
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



