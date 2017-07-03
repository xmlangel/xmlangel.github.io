---
layout: post
title:  "Jmeter-어떻게 쓰지-02"
date:   2017-07-03 19:02:49 +0900
categories: jekyll update
---
여러 URL 을 테스트할 경우 각각의 Http Request를 생성 하려면 시간이 많이 걸립니다. Http Request를 자동으로 생성 작성할 수는 없을까요?
* 목차
{:toc}

# Test Script Recoder
Test Script Recoder 기능을 이용하면, 테스트하려는 사이트를 클릭하며 돌아다니기만 해도, 필요한 요청을 자동으로 생성해줍니다.
(이전 버전에서는 Proxy Server 였는데 이름이 바뀐거 같다.)

* 현재 Jmeter 3.0 에서 테스트 하였다.

#### Non - Test Elements>Http(s) Test Script Recorder

WorkBench 에 Test Script Recorder를 추가합니다.
![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-18.png){: width="100%" height="100%"}

Port를 임의로 지정한다. 여기서는 8888을 설정했다.
![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-19.png){: width="100%" height="100%"}

#### Logic Controller>Recoding Controller

Http Test Script Recoders 가 추가됐으면 Recoding Controller 가 반드시 추가되어야 하는거 같다..없을경우 아래와 같은 메세지가 나타난다.
![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-TestScriptRecorder-Error.png){: width="100%" height="100%"}
Test Plan Content 에서 Use Recoding Controller 를 설정해서 그런듯...기본으로 WorkBench > HTTP(S)Test Script Recoder 를 해도 되지만 Recoding Controller 를 해보겠다.
![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-20.png){: width="100%" height="100%"}

Recoding Controller 를 추가해준다.
![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-20.png){: width="100%" height="100%"}

Start 를 누르면 레코딩이 시작된다.
![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-21.png){: width="100%" height="100%"}

작성중.....
작성중.....
작성중.....
{% highlight ruby %}

{% endhighlight %}