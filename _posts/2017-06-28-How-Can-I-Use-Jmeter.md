---
layout: post
title:  "Jmeter 어떻게 쓰지?"
date:   2017-06-28 00:02:49 +0900
categories: jekyll update
---
* 목차
{:toc}

# Jmeter 사용해보기

웹테스트를 진행하다가 동시 사용자 몇명까지 처리가 가능한지 또는 부하를 주고 싶을경우 Jmeter 를 이용하면 손쉽게 테스트를 할수 있다.

## 간단한 테스트 해보기

#### 처음화면
Jmeter 를 실행하면 아래와 같은 화면이 나타난다.

![Jmeter-01]({{ site.url }}/assets/images/jmeter-01.png){: width="100%" height="100%"}

#### Threads 
Test 를 수행할때 제일 먼재 해줘야 하는 부분이 Threads(User)를 만들어주는 부분이다 모든 시작은 여기서 부터 해준다.

![Jmeter-02]({{ site.url }}/assets/images/jmeter-02.png){: width="50%" height="50%"}

Thread Group 이 만들어진다.

여기서 수행할 사람수 일반적으로 user 라고 한다. 그리고 반복할 획수를 지정할수 있다.

![Jmeter-03]({{ site.url }}/assets/images/jmeter-03.png){: width="100%" height="100%"}

여기서는 10 명의 User 가 3 회 반복으로 총 30회 반복을 수행하는것으로 설정한것이다.

# IP Spooping 하는법

Mac 을 이용해서 다른부분은 일단 Pass 하고 mac 에서 하는법

#### alias 하기
ifconfig 로 아이피확인후 비슷한 아이피대역으로 alias 를 걸어주면된다.

{% highlight ruby %}
sudo ifconfig en0 alias 192.168.0.12 255.255.255.0

{% endhighlight %}


![Jmeter-ipspooping]({{ site.url }}/assets/images/jmeter-ipspooping.png){: width="100%" height="100%"}

#### alias 삭제
alias 삭제하는 법은 아래와같다.
{% highlight ruby %}
sudo ifconfig en0 -alias 192.168.0.12

{% endhighlight %}

IP 를 추가했으므로, 이제 Jmeter 에서 IP 를 지정해서 테스트를 할 수 있다.

HTTP Request 의 Advanced 에서 아이피를 지정 하면 된다.
![Jmeter-ipspooping-01]({{ site.url }}/assets/images/jmeter-ipspooping-01.png){: width="100%" height="100%"}

#### CSV Data Set Config
CSV 를 이용해서 할 수도 있다.
![Jmeter-ipspooping-02]({{ site.url }}/assets/images/jmeter-ipspooping-02.png){: width="100%" height="100%"}

먼저 CSV 파일을 생성해놓는다.

![Jmeter-ipspooping-03]({{ site.url }}/assets/images/jmeter-ipspooping-03.png){: width="50%" height="50%"}

CSV Data Set Config 설정을 한다. 
File 경로와 변수설정을 해놓는다. 여기서는 변수가 IP 이다.

![Jmeter-ipspooping-04]({{ site.url }}/assets/images/jmeter-ipspooping-04.png){: width="100%" height="100%"}

설정한 변수를 HTTPS Request 의 IP 에 할당한다.

![Jmeter-ipspooping-05]({{ site.url }}/assets/images/jmeter-ipspooping-05.png){: width="100%" height="100%"}

테스트를 실행하면 Request 에 설정한 값들로 IP 가 적용된것을 확인 해볼 수 있다.
![Jmeter-ipspooping-06]({{ site.url }}/assets/images/jmeter-ipspooping-06.png){: width="100%" height="100%"}


{% highlight ruby %}

{% endhighlight %}