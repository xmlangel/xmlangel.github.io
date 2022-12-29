---
layout: post
title: "[mac][iterm2] Finder 현재 폴더 에서 iTerm2 열기"
date:  2022-12-29 21:54:13 +0900
categories: mac iterm2 finedr 

tags:
- mac
- iterm2
- finder
---


* 목차
{:toc}
_

## finder 에서 item 열기 

가끔 Finder 에서 터미널을 열어야 할경우가 있다. 여러 커스텀툴들을 써야 하나 하고 찾아보니.. 그런것은 아니였다.

시스템설정에서 설정하나만 바꿔주면 되었다.

[appium sample](https://github.com/appium/appium/blob/1.x/sample-code/java/java.iml){:target="_blank"}내용을 참고해서 필요한 정보들을 추가해준다.

sample 에서는 gradle 이므로 적절히 mnv 형태로 바꿔주면된다.

쭉보니 별다른것은 없다. appium client 만 추가해주면되는듯하다.

Mac OS 13(Ventura 기준) 하위 버전도 될듯싶다.

시스템설정>키보드>키보드 단축키>서비스>파일 및 폴더 체크

![open-iterm]({{ site.url }}/assets/images/open-iterm.png){: width="100%" height="100%"}
