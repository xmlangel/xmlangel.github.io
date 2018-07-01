---
layout: post
title:  "Jmeter-OS Sampler 로 jar 파일 실행해보기"
date:   2018-06-30 23:00:13 +0900
categories: jekyll update
tags:
- jmeter
- os sampler
- json
---

간만에 야근을 하지 않아 시간이 남아서 기록을 다시 시작한다.

Jmeter 에서 jar 파일을 실행해보려고 한다.

결론은 간단하다 하지만 해맨시간을 생각하면 약간은 허무하다.

결론부터 보여주면 Command 입력창에 Cmd 를 입력후 Command Parameter Value 항목에 파라미터 값들을 넣어주면 된다.

![jmeter]({{ site.url }}/assets/images/jmeter-26.png){: width="100%" height="100%"}

그럼 설정을 해보겠다.

시나리오는 아래와 같다. 

1. 거래소 암호화폐 API 를 이용하려고 한다 
2. 해당 사이트에서 제공하는 APIClient 를 이용해서 한다.
3. Java ApiClient Jar 파일을 생성한다.
4. CSV 파일로 암호화폐 종류를 입력받아 원하는 암호화폐이면 jar 파일을 실행한다.
5. 출력된 값을 확인 한다.
6. 정상적으로 호출이되었는지 확인한다.

그럼 시작해보겠다.

jar 파일은 미리 생성해놓길바란다.(다른부분을 잘모르고 api.bithumb.com 에서 제공 하고 있는 Java Api Client 를 이용 한다.)
# Jar 파일준비
전체적인 설명은 못하고 간단하게 요약해서 설명한다.
왜 난 개발자가아니라서 개발관련사항들은 잘모른다. 그냥 가져다 쓸뿐

- private Api 를 이용하려면 미리 API 를 생성해야한다.
- API 를 생성후 ApiKey 와 ScretKey를 기록해두어야한다.
- 다운받은 Api Cliet 에 Apikey 와 secretKey를 저장후 Jar 파일을 만들어준다.
- jar 파일은 runable jar 파일로 만들어준다.
![jmeter]({{ site.url }}/assets/images/jmeter-29.png){: width="100%" height="100%"}


# 필요한 플러그인
기본 CSV Data set 을 이용해도 되지만 Random 으로 데이터를 불러오는 Random CSV data set 을 이용한다.

- Random CSV Data Set

- Vendor: BlazeMeter

- cumentation: https://github.com/Blazemeter/jmeter-bzm-plugins/blob/master/random-csv-data-set/RandomCSVDataSetConfig.md

# Thread Group 생성
알다시피 Jmeter 의 기본인 Thread Group 부터 생성해야 한다.

![jmeter]({{ site.url }}/assets/images/jmeter-27.png){: width="100%" height="100%"}
![jmeter]({{ site.url }}/assets/images/jmeter-28.png){: width="100%" height="100%"}

# OS Process Sampler 추가
OS Process Sampler 는 Local Machine의 Command 를 실행할수 있게 해주는 Sampler 이다. 

OS process Sampler 를 추가해준다.

![jmeter]({{ site.url }}/assets/images/jmeter-30.png){: width="100%" height="100%"}
Command 입력창에 cmd 를 입력후 Value 항목에 파라미터 값들을 넣어주면 된다.

준비한 Jar 파일의 경로를 Working 디렉토리로 설정해주면 실행가능하다.

![jmeter]({{ site.url }}/assets/images/jmeter-31.png){: width="100%" height="100%"}

실행이 되는지 수행을 해본다.

# View Result Tree 결과확인
실행결과를 보기위해 View Result Tree 를 추가해준다.

추가후 실행을 하면 Request 에 보면 어떻게 실행이 되었는지 확인할 수 있다.
![jmeter]({{ site.url }}/assets/images/jmeter-33.png){: width="100%" height="100%"}

Response Data 를 보면 정상적으로 호출이 들어가서 에러없니 수행된내용 확인이 가능하다.
![jmeter]({{ site.url }}/assets/images/jmeter-32.png){: width="100%" height="100%"}

# Random으로 CSV 파일 읽어오기
이제 입력값들을 무작위로 받아들이기 위해 CSV 파일에서 읽어들일 수 있는 Random CSV를 추가해준다.
![jmeter]({{ site.url }}/assets/images/jmeter-34.png){: width="100%" height="100%"}

CSV 파일은 coin.csv 로 설정하고, 파일은 3가지 Coin 을 추가해준다.
````
etc
btc
eth
````
Random CSV는 미리 파일이 정상적으로 읽어지는지 Test 가 확인이 가능하다.
- filename : 읽어들일 파일이름
- Delimeiter : 구분자
- variable names : 변수이름지정
- random order : random으로 읽이들이기 체크를 하지않으면, 순서대로 읽는다.
![jmeter]({{ site.url }}/assets/images/jmeter-35.png){: width="100%" height="100%"}

# 특정암호화폐인지 확인

# JSON Extractor 결과추출

