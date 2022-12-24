---
layout: post
title:  "[python][자동화] tesseract를 이용해서 이미지에서 문자추출해보기"
date:   2022-12-23 18:03:13 +0900
categories: python tesseract

tags:
- python
- tesseract
---


* 목차
{:toc}
_

## tesseract
테서렉트는 ([Tesseract](https://ko.wikipedia.org/wiki/%ED%85%8C%EC%84%9C%EB%9E%99%ED%8A%B8)) OCR(optical character recognition)을 쉽게 이용할수 있게 구현된 모듈이다. 
tesseract에서 제공하는 pytesseract를 이용하여 간단하게 문자인식과 숫자인식을 할 수 있다고 한다. 먼저 장점으로는 한두줄의 코딩만으로 문자를 추출할 수 있는 장점이 있고 단점으로는 요즘 OCR 에서 핫한 딥러닝 기반의 OCR 보다는 낮은 수준의 인식률입니다. 실제 사용하기는 무리가 있고 테스트 프로그램이나 토이 프로그램에 적용할 만한 수준이라 보시면 된다고 보면되겠다. 

Apache License, 버전 2.0 에 따라 배포되는 무료 소프트웨어이며 2006년부터 Google에서 개발을 후원 한다고 한다. 그렇다 구글에서 후원한거다.. 전문적으로 뭘 할게 아니니 시도해보자.

##  tesseract를 사용하려는 이유
[이전포스트](https://xmlangel.github.io/posts/2022-12-20-No-module-named-tkinter)에서 이것저것해야하는것중 하나를 하려고 하는것이다.

그렇다. OCR 사진을 찍은후 그것을 인식해보려고한다.

사용하는 이미지는 아래 이미지를 이용하려고한다.

게임이니 게임 데이터를 가지고 해보는것이 확실하다.

먼저 관련 모듈들을 설치한다.

tesseract 와 opencv를 이용해서 한글을 추출할 것이다.

```python
pip3 install numpy opencv-contrib-python pytesseract
```

그럼 게임에 접속해서 이미지를 하나 캡쳐해온다.

![tesseract-01]({{ site.url }}/assets/images/gamedata.png){: width="60%" height="60%"}

그럼 이미지에서 텍스트를 추출해보자.
## 시도1 이미지를 tesseract만이용해서 사용
```python
import pytesseract
from PIL import Image

filename = 'gamedata.png'
img =Image.open(filename)
text = pytesseract.image_to_string(img)
print(text)
```
결과 :
```
a ie oO oO N + oO oO oO
Ne} oO + So wo
i oS aq fo}
CS o SC ey
a
rr
Ho
wr
zl
ar ily
i Ul Rd
a Ub q RG
dio ar Rd Pl Pay TK

ral
7|
AY
Sci
THHH
AAt
a
```
뭔가 안되네... 한글은 안되나보다.. 

## 시도2 한글 데이터 추가 

설치된 언어를 보니 한글이 설치가 안되어있는듯하다. 

```python
tesseract --list-langs
List of available languages in "/opt/homebrew/share/tessdata/" (3):
eng
osd
snum
```
한글 언어를 설치해주자..
```
brew install tesseract-lang
```

한글을 설치후 다시 해보고 한글설정을 해줬다. 

```python
import pytesseract
from PIL import Image

filename = 'gamedata.png'
img =Image.open(filename)
text = pytesseract.image_to_string(img,lang='kor+eng') 
print(text)
```
결과 : 
```
더 대 = oO  N + = = =
Ne} oO + So  wo
i   oS aq  fo}
CS  o SC  ey
a
|
월
Ho
바
[기
ar  ily
i Ul  Rd
a   Ub 뒤  더      가
dio ar Rd [개  Pay     TK

건
기
사
역대
패배
전사
정
```
뭔가 나오긴하는데 아쉽다.. 다른방법으로 해봐야겠다. 

## 시도3 opencv 이용 

opencv를 이용해서 변경해서 해보자.

```python
import pytesseract
import cv2
from PIL import Image

config = ('-l kor+eng --oem 3 --psm 6')
img= cv2.imread(filename,1)
text = pytesseract.image_to_string(img, config=config)
cv2.imshow("orignal",img)
cv2.waitKey(0) 
cv2.destroyAllWindows()
```
결과 : 
```
 50000 00 ~
i  ——
전투력
건설 능력                                                                                                                 6,761
기술력                                                                                                                                     61
부대 전투력                                                                                                                          ar?
사령관 전투력                                                                                                            6,200
0 전투동 이
역대 최고 전력                           16,062
승리                                                                                                                                          4
패배                                          두                                               0
전사                                                                           ’                                                             0
정찰횟수                                                                                                                      :
이이 이
```
비슷하게 나오기 시작하는것같다.

뭔가 설정이 더 필요한거같다. 

## 시도4 opencv grayscale 처리
그레이 스케일처리를 해줘본다.

```python
import pytesseract
import cv2
from PIL import Image

config = ('-l kor+eng --oem 3 --psm 6')
img = cv2.imread(filename,cv2.COLOR_BGR2GRAY)
img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
cv2.imshow("grayscale",img)
text = pytesseract.image_to_string(img,config=config)
print(text)
```
결과:
```
 지도자146336348               전투력: 16,062                             처치 포인트: 0
전투력
건설 능력                                                                                                                 6,761
기술력                                                                                                                        61
부대 전투력                                                                                                              3,040
사령관 전투력                                                                                                            6,200
전투 통계
역대 최고 전력                                                                                                          16,062
승리                                                                                                                            4
패배                                                                                                                            0
전사                                                                                                                            0
정찰 횟수                                                                                                                      0
```
그레이 처리된이미지

![tesseract-02]({{ site.url }}/assets/images/gamedata-gray.png){: width="60%" height="60%"}


쓸만해진것같다.. 이제 후처리로 글자들을 가져와서 넣으면 될것같다. 그건 다음에..

오늘은 여기까지...

해보면서 느낀건 그렇게 어렵게 느껴지지 않는것같다. 손쉽게 이미지에서 글자를 가져올수 있다니.. 대단하다..

전문적으로 할것이 아니라면 이정도면 할만한것같다...


cf
- [pytesseract](https://github.com/madmaze/pytesseract)
- [이미지에서 문자 텍스트 추추하는 방법](https://ddolcat.tistory.com/954)
- [파이썬 문자인식 숫자인식 해보자(pytesseract-OCR,deep-text-recognition)](https://ekfkdlxm.tistory.com/18)