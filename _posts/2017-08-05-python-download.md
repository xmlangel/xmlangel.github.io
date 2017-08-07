---
layout: post
title:  "python file download"
date:   2017-08-05 12:10:13 +0900
categories: jekyll update
comments: true
tags :
- python
- download
- urllib
---

내가 이글을 적는 이유는 웹사이트에 있는 특정 정보를 추출하기 위해 스크레이핑(Scraping)을 하기 위해서이다. 

가장먼저 python 을 이용해서 다운로드 하는 부분을 알아보고 있다. 

urllib.request 를 통해서 다운로드먼져..


* 목차
{:toc}

# 다운로드 하기

## urllib.request

### 파일로 저장:urlretrieve()
urlretrieve()  함수를 이용해서 파일을 직접 다운로드 할 수 있다.

웹상에 있는 jpg 파일을 download.jpg 로 저장하는 예

{% highlight python %}
import urllib.request

# URL 저장 경로 지정하기
url = "https://xmlangel.github.io/images/xmlangel.jpg"

# 저장할 파일이름
savename = "download.jpg"

# 다운로드
urllib.request.urlretrieve(url, savename)
print("저장완료")

{% endhighlight %}

### 메모리로 저장 : urlopen()
urlopen() 함수를 이용해서 메모리에 저장할 수 있다.

웹상에 있는 jpg 파일을 메모리에 로드후 download2.jpg 로 저장하는 예
{% highlight python %}
import urllib.request

# URL 저장 경로 지정하기
url = "https://xmlangel.github.io/images/xmlangel.jpg"

# 저장할 파일이름
savename = "download2.jpg"

##다운로드
memory = urllib.request.urlopen(url).read()
print("memory 에 저장")

#파일로 저장
with open(savename, mode ="wb") as f:
	f.write(memory)
	print("저장완료")
{% endhighlight %}

# 스크레이핑 하기(Scraping)  하기
## BeautifulSoup
BeautifulSoup 은 HTML 과 XML 을 분석해주는 라이브러리 이다.

자세한 설명은 아래에서
https://www.crummy.com/software/BeautifulSoup/ 

pip를 이용해서 간단히 설치가 가능하다.

{% highlight bash %}
pip install beautifulsoup4
{% endhighlight %}

### find()
요소추출

### find_all()
여러요소추출

{% highlight python %}
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')
#기본
title1 = soup.html.head.title
print(title1.string)

# 1개요소
title = soup.find("title")

print(title.string)

# 여러개
links = soup.find_all("a")

# 링크목록
for a in links:
	heaf =a.attrs['href']
	text = a.string
	print(heaf,":",text)

{% endhighlight %}

결과
<{% highlight python %}
root@python:/home# python beautifulsoup-find.py
The Dormouse's story
The Dormouse's story
http://example.com/elsie : Elsie
http://example.com/lacie : Lacie
http://example.com/tillie : Tillie
{% endhighlight %}


{% highlight python %}
{% endhighlight %}

# 사용예시
<span style="color:blue">
기상청에 있는 RSS 데이터를 이용해서 지역의 예보데이터를 가져오는 예제를 만들어 보겠다.
편의를 위해 지역명을 입력받는 형식으로 만든다.</span>


기상청의 RSS 사이트는 아래 경로에서 확인 가능하다.

홈 > 날씨 > 생활과 산업 > 서비스 > 인터넷 > 웹

URL 은 아래와 같다.
http://www.kma.go.kr/weather/lifenindustry/sevice_rss.jsp


[충청남도](http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=133)


[서울](http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109)


{% highlight bash %}
root@python:/home# pip install beautifulsoup4
Collecting beautifulsoup4
Installing collected packages: beautifulsoup4
Successfully installed beautifulsoup4-4.6.0
{% endhighlight %}

{% highlight python %}
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

# 지역명을 입력받는다.(지역명이 없을경우 Error 를 보여준다.)
if len(sys.argv)<=1 :
	print("Error: 지역이름을 입력하세요")
	sys.exit()
regionNumber = sys.argv[1]

#RSS Site 주소
siteURL = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp"

# 지역명이름을 위한 변수
values = {
	'stnId': regionNumber
}
print(values)

# 매개변수를 URL 인코딩을 해준다.
params = urllib.parse.urlencode(values)

# RSS URL을 파라미터와 조합
RSSurl = siteURL + "?" + params

print("url=",RSSurl)

#RSS 정보를 메모리에 저장
sitedata = urllib.request.urlopen(RSSurl).read()

# utf-8 형식으로 decode
RSStext = sitedata.decode("utf-8")

# BeautifulSoup 으로 분석
soup= BeautifulSoup(RSStext,"html.parser")

#정보추출
title_list = soup.find_all("title")
wf = soup.find("wf")

for title in title_list:
	sitetitle=title.string
	print(sitetitle)

print(wf)

{% endhighlight %}



