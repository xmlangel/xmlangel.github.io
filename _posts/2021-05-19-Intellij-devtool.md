---
layout: post
title:  "Intellij devtool 설정"
date:   2021-05-19 00:15:13 +0900
categories: etc
tags:
- intelij
- devtools
---
로컬환경에서 수정된 코드가 자동으로 반영되도록 도와주는 devtool 설정하는 방법입니다.

* 목차
{:toc}
이클립스에서는 Springboot 를 이용해서 저장하면 자동으로 저장한사항이 반영되는 것을 경험하고 Intelij도 되겠거니 하고 해봤는데 안된다.
왜안되지 하고 찾아보니.. 역시나.. 나만 불편한게 아녔다.

까먹기전에 적어놓고 기록해놓는다. 해보시길.

## registry 설정
control + shitf + a (cmd + shift + a) 를 누른후 registry 를 검색해서 선택한다.
![registry]({{ site.url }}/assets/images/intelij-registry.jpg){: width="100%" height="100%"}

compiler.automake.allow.wen.app.running 을 체크해준다.

설명을 보면 Allow auto-make to start even if developed application is currently running. Note that automatically started make may eventually delete some classes that are required by the application. 이렇다고한다.
![registry]({{ site.url }}/assets/images/intellij-compiler.jpg){: width="100%" height="100%"}

## Compiler 설정
Setting>Build, Execution, Deployment>Compiler(Preferences>Build,Execution,Deployment>Compiler)에 들어가 
Build project automatically 를 적용시켜준다.
![registry]({{ site.url }}/assets/images/intellij-build-compiler.jpg){: width="100%" height="100%"}

## application.yml 설정
~~~java
spring:
  devtools:
    restart:
      enabled: true
~~~

이제 저장해보고 적용되는지 해보면된다.
