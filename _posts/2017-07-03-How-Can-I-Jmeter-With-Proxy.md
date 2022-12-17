---
layout: post
title:  "Jmeter-어떻게 쓰지-02"
date:   2017-07-03 19:02:49 +0900
categories: jmeter update
tags:
- Jmeter
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

인증서가 나오면 확인을 하면된다.

![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-23.png){: width="100%" height="100%"}

IE 에서는 proxy 설정이 쉬으므로 패스 그리고 지금은 Mac 이라서 IE 를 쓸수 없다. 

크롬에서 녹화를 해보겠다.

크롬에서 녹화를 하기위해서 proxy 설정을 해보겠다.

확장프로그램은 Quick & Dirty Proxy Flipper 를 이용해보겠다.
쓰고싶은 다른 프로그램이 있으면 이용해도 된다.

확장프로그램은 알아서 받아서 설치한다.

![Chrome-Proxy]({{ site.url }}/assets/images/Chrome_proxy.png){: width="50%" height="50%"}

Jmeter 에서 8888 을 설정해놔서 http://localhost:8888 으로 설정해준다.

![Chrome-Proxy]({{ site.url }}/assets/images/Chrome_proxy-01.png){: width="50%" height="50%"}

이제 여기저기 돌아다녀본다. 돌아다닌후 Proxy 설정을 원래대로 바꿔주고 Jmeter 에서 녹화된것을 확인 해본다. 뭔가가 많다.

![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-24.png){: width="50%" height="50%"}

png, css 등 불필요한 파일들은 삭제해준다. 그러면 수동으로 설정한것과 같이 녹화된 것을 확인 할 수 있다.

![Jmeter-Test-Script-Recoder]({{ site.url }}/assets/images/jmeter-25.png){: width="100%" height="100%"}

Threads Group를 추가하고, 녹화된 파일을 붙여준후 실행해주면 된다.

오늘은 여기까지 다음엔 뭘더볼까..ㅎㅎ

{% highlight ruby %}

{% endhighlight %}