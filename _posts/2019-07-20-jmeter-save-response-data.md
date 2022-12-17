---
layout: post
title:  "Jmeter-Response Data 저장하기"
date:   2019-07-20 09:00:13 +0900
categories: jmeter update
tags:
- jmeter
- sava Data
---
API 테스트나 성능 테스트를 진행할때 서버 응답값을 가지고 테스트를 수행할수 있다.
이때 응답받은 데이터를 변수화(variable)해서 저장 하는 방법은 아래와 같이 하면 된다.

```
vars.put("response", prev.getResponseDataAsString());
```
이미지로 보면 아래와 같다.
![jmeter]({{ site.url }}/assets/images/Jmeter-Response Data-01.png){: width="80%" height="80%"}

그럼 설정을 해보겠다.
쓰래드를 생성하고, 더미 Sampler 를 이용해서 더미 데이터 결과를 만들수 있게 해준다.
![jmeter]({{ site.url }}/assets/images/Jmeter-Response Data-02.png){: width="80%" height="80%"}

이 더미를 실행하면 응답으로 토큰값을 보내준다.
![jmeter]({{ site.url }}/assets/images/Jmeter-Response Data-03.png){: width="80%" height="80%"}

Post Processor인 JSR223으로 생성 해준다. 아래 언어 형식은 JAVA 이다. 다른 언어를 선택해줘도 된다.  
![jmeter]({{ site.url }}/assets/images/Jmeter-Response Data-04.png){: width="80%" height="80%"}

Debug Sampler 를 이용해서 결과값을 보면 아래와 같이 TOKEN 값이 저장된것을 확인 할 수있다.

![jmeter]({{ site.url }}/assets/images/Jmeter-Response Data-05.png){: width="80%" height="80%"}
