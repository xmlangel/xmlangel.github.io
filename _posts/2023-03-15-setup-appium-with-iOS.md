---
layout: post
title: "[Appium][iOS] Appium iOS 환경구성"
date:  2023-03-15 23:00:13 +0900
categories: Appium 

tags:
- appium
- iOS
---


* 목차
{:toc}
_
   
현재 appium.io 에 있는 것을 참고 해서 설치를 진행해보았다.

[appium.io](https://appium.io/){:target="_blank"}에서 가이드 하는것은 appium 1.0 버전을 설명하고 있다. 

앞으로는 [appium 2.0](https://github.com/appium/appium){:target="_blank"} 을 해야하겠지만 

아직 회사에 적용해 보지 않아 1.0 기준으로 설명해 보려고 한다.

Appium을 이용해서 iOS 자동화를 진행하 려면 반드시 Mac 장비가 있어야한다. 사과 회사는 사과만 좋아한다.


## Homebrew 설치

맥용 패키지 관리자인 homebrew를 설치해준다. 

mac을 사용한다면 거의 필수적으로 설치 해서 사용한다고 보면된다. (내가 알기는 그렇다 .. 아니라면 
언제든지 고칠 마음이 있다.)

[Homebrew](https://brew.sh/index_ko){:target="_blank"} 에서 자세한 설치 방법 참고

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Node, Appium 설치

가이드에 나와있는데로 그대로 따라하면된다. 별것없다. 

1. 노드를 설치
2. npm으로 appium 을 설치
3. wd 를 설치
4. appium 을 실행

```
> brew install node      # get node.js
> npm install -g appium  # get appium
> npm install wd         # get appium client
> appium &               # start appium
```

## 최신 WebdeiverAgent 다운로드

최신 [WebdeiverAgent](https://github.com/appium/WebDriverAgent/releases/tag/v4.13.0) 에서 관련 팡리을 다운받아서 압축을 해제하준다. 

버전은 항상올라가니 새로운안될경우 새로운 버전으로 빌드 하면될듯함.

설치할 당시의 버전은 4.13.0 버전이였다.

|------|
|webdriverAgent|
|![appium-ios]({{ site.url }}/assets/images/appium-ios-webdriverAgent-download.png){: width="100%" height="100%"}|

Homebrew 로 설치된 경로에 해당파일을 바꿔준다. 
(기존파일은 삭제하고, apppim-webdriveragent 파일로 이름을 바꿔서 넣어주면된다.)

M1 기준 아래 경로이다.
```
/opt/homebrew/lib/node_modules/appium/node_modules/appium-webdriveragent
```

## Xcode 설치
사과 공장이니 사과 공식 툴을 깔아줘야 한다 이것이 있어야 WebdriverAgent를 빌드하고 설치해 줄 수 있다.
사전에 인증서 같은 것들은 받아서 설정해놓으면 된다.
이 부분들이 조금은 오래 걸리 수도 있다 이 부분은 사전해 준비해놓길 바란다.

회사에서 한다면 개발팀의 도움을 받는 것이 빠르다..

그렇지 않다면 Apple 공식 개발자 문서를 찾아보면서 해보면 된다.

로그인을 해놓거나 Profiles이 있어야 진행이 가능하니 이 부분은 미리 설정을 해놓자.

|------|
|xcode Account 로그인|
|![appium-ios]({{ site.url }}/assets/images/appium-ios-xcode-account.png){: width="100%" height="100%"}|


----
2023.3.22일 새로 알게된 사실이있어서 추가로 적어 놓는다.

- 회사에서 제공받는 인증서가 없다면 개인 팀(Personam Team) 인증서를 이용해서 이용할 수도 있다.
- 기간이 얼마나 이용 가능한지는 모르겠지만 1년 사용 가능할 것 같다.
- 앱스토어에 등록할 것이 아니니 개인적으로 사용할 용도라면 사용이 가능한 것 같다.
  
검색을 해보니 아래와 같이 이용이 가능하다고 한다.


```
Apple의 Personam Team 인증서는 개인적인 목적으로 앱을 배포할 때 사용됩니다. 따라서 해당 인증서로 앱을 App Store에 배포할 수는 없습니다. 앱을 App Store에 배포하려면 Apple의 Enterprise 또는 Developer 프로그램에 가입하여 해당 프로그램에서 제공하는 인증서를 사용해야 합니다.
```
----

## XcodecommandlineTool 설치

간단하게 커맨드라인에서 아래 명령어 입력으로 설치 가능하다.

```
xcode-select --install 
```


## WebdriverAgent build 및 설치
공식 가이드 라인에 있는 가이드 라인데로 설치해주면된다.

먼져 Node 가 설치되어있어야한다. (위에서 설치했으니 Pass)

그리고 다운로드한 파일 압축을 풀여주고 `WebDriverAgent.xcodeproj` 파일을 xcode에서 실행해서 열어준후 `WebDriverAgentRunner`를 테스트 할 디바이스에 빌드해서 넣어주면된다. 

Xcode 에서 빌드를 해보고 정상적인지 확인 한다. 

|------|
|WebdrivarAgent 빌드 테스트|
|![appium-ios]({{ site.url }}/assets/images/appium-ios-webdriverAgentRunner-run.png){: width="100%" height="100%"}|


## Inspector 설치 
앱의 구성요소들을 확인하려면 Inspector 가 설치되어있어야 한다.

과거에는 Appium Server를 설치하면 같이 설치가 되었으나 appium 2.0 준비를 하면서 Inspector 도 따로 분리가 된듯하다. 

기본적으로 2.0 설정이 되어있지만 URL 등을 변경해서 사용하면 1.0 에서도 사용이 가능하다.

설치는 [Inspector](https://github.com/appium/appium-inspector/releases){:target="_blank"} 에서 설치 파일을 받아서 실행 해주면 된다.


|------|
|inspector|
|![appium-ios]({{ site.url }}/assets/images/appium-ios-inspector.png){: width="100%" height="100%"}|

설치들은 완료되었으니 다음에는 인스팩터에서 Appium 엘리먼트를 읽어오는 방법을 해보겠다.

졸리니 다음에.. 

끝.
