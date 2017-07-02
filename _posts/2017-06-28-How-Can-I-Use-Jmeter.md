---
layout: post
title:  "Jmeter 어떻게 쓰지?-01"
date:   2017-06-28 00:02:49 +0900
categories: jekyll update
---

웹테스트를 진행하다가 동시 사용자 몇명까지 처리가 가능한지 또는 부하를 주고 싶을경우 Jmeter 를 이용하면 손쉽게 테스트를 할수 있다.

* 목차
{:toc}

# Jmeter 사용해보기

## 테스트 환경

부하 발생을 목적으로 하는 프로그램으로(물론 일반 웹시나리오 테스트들도 이용이 가능하다.) 외부로 테스트를 수행하면 네트워크에 무리가 갈수 있으므로 내가 사용하고 있는 PC 에서 환경을 만들어 테스트를 해보고자 한다.

간단히 테스트 해보기 위해 Spring PetShop 을 이용해보겠다. 

해당 프로젝트는 아래에서 확인 가능하다.

<https://github.com/spring-projects/spring-petclinic>

{% highlight git %}
git clone https://github.com/spring-projects/spring-petclinic.git
cd spring-petclinic
./mvnw spring-boot:run
{% endhighlight %}
build 후 java 로 실행도 가능하다.

{% highlight shell %}
java -jar spring-petclinic-1.5.1.jar --server.port=8080 &
{% endhighlight %}



http://localhost:8080 으로 접속하면  개새끼 한마리랑 냥이 한마리가 보일것이다.

![petshop]({{ site.url }}/assets/images/petshopforspring.png){: width="100%" height="100%"}

## 간단한 테스트 해보기
Jmeter 에서는 테스트 스크립트를 Test Plan 이라고 표현한다. 

처음 만들어볼 Test Plan 은 3 Step 으로 진행해보려고 한다. 

1. Pet Shop 페이지 진입
2. Find Owner 페이지에 접속
3. Error 발생 페이지 접속

* Pet Shop 페이지 진입
![petshop]({{ site.url }}/assets/images/petshopforspring.png){: width="100%" height="100%"}

* Find Owner 페이지에 접속
![petshop-01]({{ site.url }}/assets/images/petshop-01.png){: width="100%" height="100%"}

* Error 발생 페이지 접속 
![petshop-02]({{ site.url }}/assets/images/petshop-02.png){: width="100%" height="100%"}

#### 처음화면
Jmeter 를 처음 실행하면 Test Plan 이라는 아래와 같은 화면이 나타난다.

![Jmeter-01]({{ site.url }}/assets/images/jmeter-01.png){: width="100%" height="100%"}

#### Threads>Thread Group 
Test 를 수행할때 제일 먼재 해줘야 하는 부분이 Threads(User)를 만들어주는 부분이다 모든 시작은 여기서 부터 해준다.
Add>Threads>Thread Group
![Jmeter-02]({{ site.url }}/assets/images/jmeter-02.png){: width="50%" height="50%"}

Thread Group 이 만들어진다.

여기서 수행할 사람수 일반적으로 user 라고 한다. 그리고 반복할 횟수를 지정할수 있다.

![Jmeter-03]({{ site.url }}/assets/images/jmeter-03.png){: width="100%" height="100%"}

여기서는 10 명의 User 가 3 회 반복으로 총 30회 반복을 수행하는것으로 설정한것이다.

#### Sampler>Http Request Sampler
테스트 리스트를 생성하기위해 Http Request Sampler 를 추가해준다.

![HttpREquest]({{ site.url }}/assets/images/Httprequest.png){: width="100%" height="100%"}

추가후 Server Name 에 localhost Port number 에 8080 을 입력해준다.
![Httprequest-02]({{ site.url }}/assets/images/jmeter-04.png){: width="100%" height="100%"}
#### Listner>View Result Tree
정상 동작하는지 보고싶지 않은가? 그냥 하면 동작하는지 알수 없다.  
Listner 를 추가해줘야 한다.

View Result Tree Listner 를 추가해준후 실행을 하면 결과를 볼 수 있다.
![viewResultTree-01]({{ site.url }}/assets/images/jmeter-05.png){: width="100%" height="100%"}

Result 를 보면 정상으로 처리된걸 볼수 있다.
![viewResultTree-02]({{ site.url }}/assets/images/jmeter-06.png){: width="100%" height="100%"}

### Config Element>Http Request Defaults
여러개의 스텝을 넣어야 하는데 URL만 같고 뒤의 path 만 다르다. 이럴경우 Config Element 를 이용해서 쉽게 설정이 가능하다.

Http Request Defaults 를 이용하면 URL 만 넣고, Sampler 에서는 Path 만 지정해서 사용가능하다.
![HttpRequestDefault-01]({{ site.url }}/assets/images/jmeter-07.png){: width="100%" height="100%"}
Server Name 과 Port 정보에 공통으로 사용할 정보들을 넣어준다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-08.png){: width="100%" height="100%"}
그리고 기존에 Http Request 에서는 해당부분을 삭제해준다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-09.png){: width="100%" height="100%"}
실행후 결과를 보면 공통으로 적용된 부분을 볼 수 있다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-10.png){: width="100%" height="100%"}

나머지 부분도 Http Request 를 만들고 이름을 변경해서 정리해준후 결과를 보면 아래와 같이 모두 정상적으로 수행된 결과를 볼 수 있다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-11.png){: width="100%" height="100%"}

Thread Group 에서 테스트 시간에 따른 Thread 숫자를 그래프로 볼수도 있다.

![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-12.png){: width="100%" height="100%"}.
10개의 Thread 를 60초동안 생성했으므로 계단처럼 단계적으로 생성된것처럼 보인다.

![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-13.png){: width="100%" height="100%"}

하지만 기본으로 제공되는 Thread Group 의 Ramp-Up Period 는 정교하지 못하다. Thread 를 100으로 설정해보겠다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-14.png){: width="100%" height="100%"}
선형으로 나타난것을 볼수 있다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-15.png){: width="100%" height="100%"}

점진적으로 증가하는 것은 테스트 할수 없다.

### Threads>Stepping Thread Group

만약 10개의 Thread 로 1분 동안 테스트 하고, 다시 10개의 Thread 를 추가해서 20개의 Thread 로 1분동안 테스트하도록 설정한다면 Thread Group의 Ramp-Up Period 로는 테스트 할 수 없다.(뭐 Thread Group 을 추가로 생성해서 StartUp Delay 를 각각 1분씩 추가하는 꼼수를 부릴수는 있겠다.)

이럴경우 추가로 플러그인은 추가해서 사용하는방법들이 있을 수 있다.
아래는 jp@gc - Stepping Thread Group 을 추가해서 테스트를 기본 Thread Group 을 삭제하고 옮겨봤다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-16.png){: width="100%" height="100%"}

Threads Scheduling Parameters 에서 설정한데로 100명의 유저를 10 명씩 추가되는화면을 볼수 있다.
![HttpRequestDefault-02]({{ site.url }}/assets/images/jmeter-17.png){: width="100%" height="100%"}

간단하게 적으려고 했는데 적다보니 길어졌다. 

좀더 정리해가면서 적고 오늘은 여기시 그만.........

간만에 쓰려니 역시 이것저것 써보면서 해봐야겠다.


{% highlight ruby %}

{% endhighlight %}