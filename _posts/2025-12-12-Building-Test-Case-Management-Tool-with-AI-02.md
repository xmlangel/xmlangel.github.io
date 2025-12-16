---
layout: post
title: "[AI 개발] 2부 제작과정 - QA 엔지니어로 일하며 AI 도구로 테스트 케이스 관리툴 만든 경험담"
date: 2025-12-12 20:42:00 +0900
categories: ai-development
tags:
- ai
- test-management
- testcasecraft
---

* 목차
{:toc}

---

2부를 시작합니다.

  

1부에서 LLM 사용기를 다뤘다면, 이번 2부에서는 실제 TestCaseCraft를 어떻게 설계하고 만들었는지 그 구체적인 과정을 기록하려 합니다. 지난 몇 개월간 퇴근 후와 주말을 반납하며 진행한 작업들을, 당시의 기억과 틈틈이 남겨둔 기록을 바탕으로 차근차근 풀어보겠습니다.

  

[1부: LLM 사용기]({% post_url 2025-08-10-Building-Test-Case-Management-Tool-with-AI-01 %})

  

2부: 제작과정 (현재글)

  

3부: (미정)


개발자가 아닌 QA 엔지니어의 시선으로, AI와 함께 맨땅에 헤딩하며 쌓아 올린 이야기를 시작합니다.

  

# 1. 프로젝트 이름 짓기

   

프로젝트를 시작할 때 가장 먼저 한 일은 이름을 정하는 것이었습니다. 이름이 있어야 애착이 생기니까요.

  

처음엔 직관적인 TestcaseManagement라고 불렀다가, 다음으로는 조금 더 문장형인 I can create testcase라는 이름도 시도해봤습니다. 하지만 부를 때마다 입에 착 붙지 않았고, 무엇보다 제가 이 도구를 만들며 느끼는 감정이 담겨있지 않았습니다.

  

자동차를 사랑하는 사람들이 '붕붕이' 같은 애칭을 붙이듯, 저도 저만의 도구에 의미 있는 이름을 주고 싶었습니다.

  

고심 끝에 탄생한 이름이 바로 TestCaseCraft입니다.

  
**TestCaseCraft의 탄생** 이 이름에는 단순한 '테스트 케이스 관리' 이상의 의미를 담고 싶었습니다. QA(Quality Assurance)는 단순히 오류를 찾아내는 반복 작업이 아니라, 품질이라는 결과물을 정성스럽게 다듬고 만들어가는 장인(Craftsman)의 과정이라고 생각하기 때문입니다.

  

마치 장인이 자신의 작품을 깎고 다듬어 완성하듯, 끝까지 품질을 책임지는 과정을 이 도구로 표현하고 싶었습니다. 조금 거창하게 들릴 수도 있지만, 그만큼 애착을 가지고 만든 툴이기에 이 이름이 가장 자연스럽게 느껴졌습니다.

  

<img src="/assets/images/testcasecraft_light.jpg" alt="테스트 케이스 크래프트 로고" width="60%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

  
  

# 2. 아키텍처 설계


TestCaseCraft는 단순한 기록용 도구가 아니라, QA가 실제로 테스트를 설계하고 실행하는 전 과정을 효율적으로 지원하는 플랫폼을 목표로 했습니다. 그래서 처음부터 **'통합'과 '확장성'**을 최우선으로 고려했습니다.

  
**전체 시스템 구조**
  

전체적인 폴더 구조와 기술 스택은 다음과 같이 잡았습니다. Spring + FastAPI + React + PostgreSQL 조합을 통해 안정성과 최신 AI 기술을 동시에 잡으려 노력했습니다.

```
┌─────────────────┐    ┌─────────────────────┐    ┌───────────────────────┐
│   Frontend      │    │   Backend           │    │   Database            │
│   (React)       │◄──►│(Spring Boot+FastAPI)│◄──►│  (PostgreSQL-pgvector)│
└─────────────────┘    └─────────────────────┘    └───────────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └─────────────►│  Authentication │◄─────────────┘
                        │  (JWT + Refresh)│
                        └─────────────────┘
```
  

### 1) Frontend (React SPA)

  

사용자 경험(UX)을 위해 **React 기반의 Single Page Application(SPA)**을 선택했습니다. 테스트 케이스를 작성하고 수정하는 과정이 끊김 없이 매끄러워야 했기 때문입니다.

  

React 18 + Material-UI 7

```

├── src/

│ ├── components/ # 재사용 가능한 UI 컴포넌트

│ ├── context/ # 전역 상태 관리 (Redux Toolkit 등)

│ ├── services/ # API 호출 서비스 모듈

│ ├── models/ # 데이터 모델 (TypeScript 인터페이스)

│ └── utils/ # 유틸리티 함수

```

개발 과정의 변화 (CRA에서 Vite로)

처음에는 익숙한 create-react-app으로 시작했습니다. 하지만 빌드 속도 문제와 React 공식 문서의 권장 사항 변경을 확인하고, 과감하게 Vite로 전환했습니다. 현재는 Vite 7 + MUI 7 조합을 사용 중인데, 초기 설정만 잘 넘기면 개발 경험(DX)이 훨씬 쾌적했습니다. "나중에 고생하느니 지금 최신화하자"는 판단은 옳았습니다.

  

### 2) Backend (Spring Boot API)

  

저는 20년 이상의 QA 엔지니어이지 전문 백엔드/프런트엔드 개발자는 아닙니다. 그래서 가장 익숙하고 안정적인 Java와 Spring Boot를 선택했습니다.

  

요즘 AI 프로젝트는 Python이 대세지만, 핵심 비즈니스 로직의 안정성과 유지보수를 생각하면 Java가 더 낫다고 판단했습니다. LLM은 별도 서비스로 분리하면 되니까요.

```

Spring Boot 3.4

├── controllers/ # REST API 엔드포인트

├── services/ # 비즈니스 로직

├── repositories/ # JPA 데이터 접근 계층

├── models/ # Entity 객체

├── security/ # JWT 인증 및 권한 관리

└── config/ # 설정 클래스

```

  

Spring Security를 도입해 JWT 기반 인증과 역할(Role) 기반 접근 제어를 구현하여 보안성도 놓치지 않으려 했습니다.

  

### 3) RAG Service (FastAPI)

  

여기서 고민이 많았습니다. LLM 기능을 넣어야 하는데, Java 생태계에는 Python의 LangChain만큼 강력하고 참고할 만한 라이브러리가 부족했습니다.

  

결국 백엔드를 두 개로 나누는 형태를 취하기로 결정했습니다.

Spring Boot: 비즈니스 로직, 회원 관리, CRUD
FastAPI: RAG(검색 증강 생성), 문서 파싱, 임베딩, LLM 통신


```

FastAPI - RAG Service

├── 문서 업로드 및 저장 (MinIO - S3 호환)

├── 문서 파싱 (PyMuPDF4LLM 등)

├── 텍스트 임베딩 (Sentence Transformers)

├── 벡터 검색 (PostgreSQL + pgvector)

└── 대화 관리 (LangChain)

```


이 구조 덕분에, Spring 서버에 부하를 주지 않고 무거운 AI 작업을 별도로 처리할 수 있게 되었습니다. 문서 파싱은 초기엔 유료 API를 썼지만, 현재는 PyMuPDF4LLM으로 95% 이상 처리하며 비용과 속도를 모두 잡았습니다.

  
<table>
  <tr>
    <td><img src="/assets/images/RAG_Structure.png" alt="RAG Structure" width="900" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>

### 4) Database (PostgreSQL + pgvector)

  

시스템의 뼈대인 DB는 PostgreSQL 18을 선택했습니다.

제가 다니는 회사가 PostgreSQL 관련 제품을 다루기도 하고, 무엇보다 pgvector 확장 기능을 통해 별도의 벡터 DB(Pinecone 등) 없이도 RAG 시스템을 구축할 수 있다는 점이 매력적이었습니다.

  

서비스용 DB와 RAG용 DB를 논리적으로 분리하여, AI 데이터 처리가 꼬여도 핵심 서비스에는 영향이 없도록 설계했습니다.

  

### 5) Testing & Integration

  

QA 툴을 만드는 QA 엔지니어로서 테스트를 소홀히 할 순 없었죠.

  

Testing: 처음엔 Cypress를 썼으나, 속도와 병렬 처리 이점이 있는 Playwright로 전환하여 E2E 테스트를 구축했습니다.

  

Integration: 현업에서 가장 많이 쓰는 JIRA 연동을 기본으로 넣었습니다. 테스트 실패 시 바로 티켓을 생성할 수 있습니다. 알림은 Gmail API를 연동해 우선 구현했습니다.

   

# 3. 기능 구현
 

**"최소한의 기능부터 완벽하게"**

거창한 기능보다는 QA 업무에 **'꼭 필요한 기능'**부터 정의했습니다. 개발 순서는 Backend → Frontend → RAG 순으로 진행했습니다.

## 프로젝트 관리 (Tree Structure)
여러 프로젝트를 생성하고 관리하는 구조로 쉽게 생성할수 있게 했어요 

조직(Organization) → 프로젝트(Project) → 그룹(Group)으로 이어지는 위계 구조를 잡았습니다.

이 기능을 통해 프로젝트마다 수백, 수천 개 단위의 테스트케이스를  

효율적으로 찾아보고 관리할 수 있도록 했습니다.

<table>
  <tr>
    <td><img src="/assets/images/2025-09-11-Project.gif" alt="Project" width="800" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>


## 테스트 케이스 관리 (Tree Structure) 

QA 업무의 핵심입니다. 폴더 트리 구조로 수천 개의 케이스를 직관적으로 관리할 수 있게 했습니다.

**트리 구조로 한눈에 관리할 수 있는 인터페이스** 를 가장 먼저 고려했습니다.  
물론 드레그 앤 드롭 기능을 넣으려고 했으나 마우스를이리 저리 끌고 다니기 힘들어 텍스트입력을 통해 순서변경이라던가 수동적인 면들을 넣게되었어요
테스트 케이스에 들어갈 항목들은 기본 항목들로 구성했어요 필요하면 하나씩 추가하며 되니까는요 범용툴은 내가 케이스 항목들이라던가 그런부분들을 커스텀할수 없지만 이건 내가만든거니 커스텀 가능하자나요 

- 테스트케이스 이름
- 설명
- 사전조건
- 사후조건 
- 예상결과
- 테스트 스텝
- 첨부파일
- 테그

그리고 요즘 대부분 Markdown 형식이라 에디터도 Markdown 형식의 에디터를 지원하게 만들었어요.

하지만 대량 입력을 하기위해서 스프레드시트 기능을 넣었습니다.
Import/Export 하는 기능 보다는 엑셀/구글 스프레드시트에서 작업한 내용을 바로 복사 붙여 넣기 할 수 있도록 만들었어요.
중간에 줄을 추가한다거나 삭제 한다거나 하는기능들도 만들어서 넣었죠.

<table>
  <tr>
    <td><img src="/assets/images/2025-12-12-Testcase.gif" alt="Testcase" width="400" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
    <td><img src="/assets/images/2025-12-12-Testcase-03.gif" alt="Testcase-01" width="400" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>
  

## 테스트 플랜 (Test Plan)
테스트케이스가 준비되면, 그다음은 실행 계획을 세워야 합니다.  
그래서 **테스트 플랜 관리 기능** 을 별도로 분리했습니다.

- 테스트 플랜 생성, 수정, 삭제  
- 개별 플랜에 테스트케이스를 연결  
- 실행 단위별 관리 및 통계 기능 연동  

플랜 단위로 테스트를 묶어 관리함으로써  
“프로젝트별 QA 수행 내역”을 직관적으로 파악할 수 있도록 설계했습니다.
<table>
   <tr>
    <td><img src="/assets/images/2025-12-12-TestPlan.gif" alt="TestPlan" width="700" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>
  
## 테스트 실행 (Execution)

이 단계에서는 테스트케이스의 실행 상태와 결과를 관리할 수 있도록 했습니다.

- 테스트 실행 생성, 수정, 삭제  
- 개별 케이스의 **Pass/Fail 결과 기록**  
- 결과 입력 후 자동으로 다음 케이스로 이동  

일일이 페이지를 전환하지 않아도 쓸수있게 클릭 한 번으로 Pass/Fail을 기록하고, 자동으로 다음 케이스로 넘어가는 UX에 집중했습니다.
(제가 직접 쓸 거라, 클릭 횟수를 줄이는 데 집착했습니다.)
<table>
   <tr>
    <td><img src="/assets/images/2025-12-12-TestExecution.gif" alt="TestExecution" width="700" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>

## 테스트 결과 (Result)
테스트 결과는 간단하게 결과에 대한 통계를 보고 통계에 대한 상세 내용들을 볼수 있도록했어요

수동 테스트와 자동화 테스트에 대한 결과를 한눈에 같이 보는데 집중을 했습니다.

현재는 가장 간단한 것만 집중했고 향후 써보며 바꿔나가려고 합니다.

<table>
   <tr>
    <td><img src="/assets/images/2025-12-12-TestResult.gif" alt="TESTRESULT" width="700" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>


## 자동화 테스트 (Test Automation)**

**"자동화 기능 결과 한곳에서 같이 볼수 있게 "**

자동화 테스트 부분도 빠트릴수 없었죠 요즘은 대부분 자동화 테스트를 만들고 하자나요 

그래서 범용적으로 사용하는 **Junit xml** 데이터를 불러와 테스트 계획에 연결하고 결과를 보고 수정할수 있는 기능들을 넣는것 위주로 만들었어요 

자동화 테스트는 테스트 플랜과 연결되고 자동화 테스트 개별 적으로 볼수있게 
독립적인 것이 아닌 연계해서 볼수 있는 기능을 넣어야지 하고 만들었어요 

그래서 테스트 플랜에 자동화 테스트 연결을 시켜줘서 테스트 실행들을 한곳에서 볼수 있게 구현했어요
<table>
   <tr>
    <td><img src="/assets/images/2025-12-12-Automation.gif" alt="AUTOMATION" width="700" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>


## RAG 문서(RAG Documents)
RAG 부분은 프로젝트 후반부에 추가된 기능이지만,  
LLM을 실질적으로 활용하기 위해 빼놓을 수 없는 영역이었습니다.  

첨부된 문서를 LLM 질의를 통해서 정확한 내용과 그 기반으로 다시 테스트 케이스를 생성할수 있도록하는 기능을 넣으려고 노력했어요 

<table>
   <tr>
    <td><img src="/assets/images/2025-12-12-RAG_01.gif" alt="RAG_01" width="700" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>

RAG 문서 내용을 기준으로 기능리스트를 만든다던가 테스트 케이스를 작성해서 테스트 케이스를 새로생성해서 넣는 기능을 함께 넣었어요

LLM 을 통해서 문서기반의 기능리스트와 테스트케이스가 자동으로 생성됩니다.

<table>
   <tr>
    <td><img src="/assets/images/2025-12-12-RAG_02.gif" alt="RAG_02" width="700" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>

----  

이렇게 TestCaseCraft의 기본 골격을 완성했습니다.
  
처음엔 단순하지만 분명한 목표에서 출발했고,

추후 RAG 기능이 붙고 자동화 범위가 확장되면서 점점 복잡해졌습니다.

완벽하진 않지만 하나 하나 만들어가는 재미가 있었습니다. 앞으로도 계속 작업을 해나가야하고요.
(현재 RAG 처리 입배딩시 lock 걸리는 부분이라던가, 캐시 처리하는 부분이라던가... 기타 필요한부분들) 

하지만 **초기의 명확한 정의**가 전체 시스템의 방향성을 잡아주는 기준이 되어주었습니다.

LLM 은 비용이 나가는 부분들을 제거하기위해 현재 대부분 Ollama 에 gpt-oss:120b 모델을 가지고 임베징진행해서 작업해나가고 있습니다.

그렇게 상태가 나쁘지는 않아요..

정리하고나니 상당히 복잡한 구조로 가 나왔네요
  
좀 긴 이야기 이지만 오늘은 여기까지 하고 다음에 뭘할지 생각해볼게요.

끝.