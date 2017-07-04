---
layout: post
title:  "Jmeter-IP Spooping"
date:   2017-07-01 06:02:49 +0900
categories: jekyll update
tags:
- Jmeter
---
스푸핑(Spoofing)의 사전적 의미는 '속이다'이다. 테스트 진행시 IP 를 변경해서 테스트를 진행하고 싶을경우 어떻게 진행해야 할까?

* 목차
{:toc}

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