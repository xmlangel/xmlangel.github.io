---
layout: post
title: "[QA] Katalon 2022년 보고서"
date:  2023-04-10 13:00:00 +0900
categories: QA

tags:
- QA
- Report
---


* 목차
{:toc}
_
Katalon 에서 2022년도 품질현황 보고서를 출간했다.

묻혀둔 문서를 오늘에서야 읽어보고 정리해본다. 

해당 리포트의 출처는 [The State of Quality Report 2022](https://katalon.com/state-quality-2022-thank-you){:target="_blank"} 이다. 

그럼 간단하게 요약을 해보려고 한다. 

## 보고서의 응답자들 과 수행방법
- 3,000 명 이상의 응답
- 팀경험에 초점을 맞춰서 진행
- 6~10명정 도된 팀들에 대한 응답

해당 보고서는 두단계로 수행.
- 첫번째 단계에서 응답자들에게 소프트웨어 품질 기술, 테스트 자동화, AI 채택에 관한 28개의 질문으로 구성 해서 온라인을 통한 설문을 진행,
- 두번째 단계에서 전문가 및 경험이 풍부한 분들에게 인터뷰 방식을 통해서 의견수렴과 통잘력을 수집했다고함.

|------|---|
|역할|팀규모|
|![katalon-01]({{ site.url }}/assets/images/katalon-2022-report-01.jpg){: width="50%" height="100%"}|![katalon-02]({{ site.url }}/assets/images/katalon-2022-report-02.jpg){: width="50%" height="100%"}|

## Coty Rosenblath의 보고서 요약
해당 보고서는 Katalon의 CTO인 Coty Rosenblath의 보고서 요약으로 리포트의 전반적인 사항을 요약서술해서 말하고 있었다. 
- 테스트 자동화는 매우 효과적인 기술임에도 불구하고, 전문가들 중 절반 이하만이 이를 프로젝트에 적용한 것으로 나타났고 이는 이 기술을 구현하는 데 어려움이 있었다는 것을 의미
- 요구사항의 빈번한 변경과 시간 부족은, 테스트 자동화를 사용하여 품질을 보장하는 데 주요한 과제였으며, 아직도 자동화를 통해 해결할 수 있는 여러 테스트 활동들이 존재
- 보고서에 따르면, 회귀 테스트 이외에도, 자동화 도구를 사용하여 테스트 결과를 분석하고, 테스트 데이터를 생성하며, 성능 테스트를 수행하는 등 여러 시간이 많이 걸리는 작업들을 자동화하는 경향이 있음
- 인공지능의 잠재력이 크다고 하지만, 보고서는 아직 테스트 자동화를 위한 인공지능 기술이 초기 단계에 있다는 것을 강조하며, QA 관행과 도구를 효과적으로 사용하는 것에 대한 더 많은 관심이 있었다는 결과를 보여줌.

## 나의 요약

- 가장 널리 사용되는 QA 기술은 자동화된 테시스템 테스트 이지만 사람들이 기대 만큼 많이 사용하고 있지는 않다.
    - 51% 만이 사용하고 있다고함.
  
![katalon-03]({{ site.url }}/assets/images/katalon-2022-report-03.jpg){: width="100%" height="100%"}

  - 품질과 속도 사이의 균형을 맞추기 위해 프로덕션에서의 모니터링 테스트 등장
  - 자동화된 테스트 및 코드리뷰가 가장 효과적인 QA 기술이다.
    - 자동화된 테스트(65%)
    - 코드리뷰(54%)

![katalon-04]({{ site.url }}/assets/images/katalon-2022-report-04.jpg){: width="100%" height="100%"}

  - 잦은 요구 사항 변경과 품질을 보장할 시간 부족은 고품질 소프트웨어를 제공하는데 가장 많이 언급되는 문제이다.
    - 잦은 요구사항 변경(46%)
    - 품질보증 시간 부족(39%)

![katalon-05]({{ site.url }}/assets/images/katalon-2022-report-05.jpg){: width="100%" height="100%"}

  - 전문가들은 소프트웨어 품질에 만종하지만 QA 관행 및 도구에 대해서는 만족하지 않고 있다.
  - 무료 오픈소스 자동화 도구보다는 상용 도구를 많이 사용하는 추세
    - Selenium 은 가장 많이 사용하는 도구이지만 2018 86%--> 20221 37% 로 감소.

![katalon-06]({{ site.url }}/assets/images/katalon-2022-report-06.jpg){: width="100%" height="100%"}

```
그냥 개인적인 생각은 오픈소스 자동화 툴 사용율이 줄었다고 하는데 기본 베이스는 Selenium 이니 전체적인 사용율을 

selenium 37
katalon 21
appium 16

74% 라고 생각한다. 

요즘 보고 있는 Cypress 도 12%에 육박하는 것같다 다른 리포트에서도 증가하는 추세를 보여주는듯하다. 

좀더 봐야할라나? 

뭐 Cypress 도 CSS 및 Xpath 로 엘리먼트를 찾으니 Selenium과 별반 차이점을 느끼지 못하겠다. 
(Cypress 에서는 다른 접근법이라고 하지만.. 물론 Cypress 가 직관적이고 좀더 쉽긴 한것같다.)
```
  - 테스트 자동화는 점점더 많은 테스트 활동에 적용
    - 회귀 테스트(53%)
    - 테스트 결과분석(38%)
    - 테스트 데이터 생성(36%)
    - 테스트 수행(34%)
  - 자동화도구를 적용하는데 가장일반적인 문제는 계속해서 지속되고 있다고함.
    - 도구에 대한 기술 및 경험부족(37%)
    - 자주 변경되는 요구사항(36%)
  
  ![katalon-07]({{ site.url }}/assets/images/katalon-2022-report-07.jpg){: width="80%" height="100%"}

  - 대부분의 팀은 테스트 자동화로 높은 ROI를 달성
    - 자동화 투자에서 20% 이상의 비용과 시간을절약
    - 6%는 손실을 봤고
    - 9%는 전혀 절약못함.
  
  ![katalon-08]({{ site.url }}/assets/images/katalon-2022-report-08.jpg){: width="60%" height="100%"}

  - 테스트 자동활르 위한 AI 는 아직초기 단계
    - 자동화를 위해 일부 AI의 기능을 사용함.
  
![katalon-09]({{ site.url }}/assets/images/katalon-2022-report-09.jpg){: width="60%" height="100%"}

끝으로 이 내용은 모두 내가 작성한것이 아닌 Katalon 에서 작성한것으로 모든 저작권 및 권한은 Katalon 에 있음을 밝혀둔다. 

그럼 오늘은 여기까지..

끝.