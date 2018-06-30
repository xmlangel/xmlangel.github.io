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

결론부터 보여주면 Command 입력창에 Cmd 를 입력후 Value 항목에 파라미터 값들을 넣어주면 된다.

![jmeter]({{ site.url }}/assets/images/jmeter-26.png){: width="100%" height="100%"}

그럼 설정을 해보겠다.

시나리오는 아래와 같다. 

요즘 한물간건진 모르겠지만 암호화패 API 를 이용하려고 한다 사이트에서 제공하는 APIClient 를 이용해서 이용해보려고한다.
1. Java ApiClient Jar 파일 생성
2. CSV 파일로 Coin 종류를 입력받아 BTC 이면 실행한다.
3. Json 형태로 출력된 결과값을 확인한다.
4. 정상적으로 호출이되었는지 확인한다.

그럼 시작해보겠다.

jar 파일은 미리 생성해놓길바란다.(다른부분을 잘모르고 api.bithumb.com 에서 제공 하고 있는 Java Api Client 를 이용해보려고한다.)

# 필요한 플러그인
기본 CSV Data set 을 이용해도 되지만 Random 으로 데이터를 불러오는 Random CSV data set 을 이용한다.

- Random CSV Data Set

- Vendor: BlazeMeter

- cumentation: https://github.com/Blazemeter/jmeter-bzm-plugins/blob/master/random-csv-data-set/RandomCSVDataSetConfig.md

# Thread Group 생성
알다시피 Jmeter 의 기본인 Thread Group 부터 생성해야 한다.

![jmeter]({{ site.url }}/assets/images/jmeter-27.png){: width="100%" height="100%"}
![jmeter]({{ site.url }}/assets/images/jmeter-28.png){: width="100%" height="100%"}

# OS Sampler 추가

# JSON Extractor

# View Result Tree 결과확인
