---
layout: post
title:  "Jmeter-Response Data 저장하기"
date:   2019-07-20 09:00:13 +0900
categories: jekyll update
tags:
- jmeter
- sava Data
---
API 테스트나 성능 테스트를 진행할때 서버 응답값을 가지고 테스트를 수행할수 있다.
이때 응답받은 데이터를 변수화(various)해서 저장 하는 방법에대해서 기술하려고 한다.

결론은 아래와 같이 하면 된다.

```

vars.put("response", prev.getResponseDataAsString());

```

![jmeter]({{ site.url }}/assets/images/jmeter-26.png){: width="100%" height="100%"}

그럼 설정을 해보겠다.
