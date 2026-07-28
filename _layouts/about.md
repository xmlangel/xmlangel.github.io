---
# Mr. Green Jekyll Theme - v1.1.0 (https://github.com/MrGreensWorkshop/MrGreen-JekyllTheme)
# Copyright (c) 2022 Mr. Green's Workshop https://www.MrGreensWorkshop.com
# Licensed under MIT

layout: default
# About page
---
{%- include multi_lng/get-lng-by-url.liquid -%}
{%- assign lng = get_lng -%}
<div class="multipurpose-container about-container">
  <div class="row about-main">
    <div class="col-md-3 about-img">
      <img src="{{ page.img }}" alt="">
    </div>
    <div class="col-md-9 about-header">
      <h1 translate="no">{{ site.data.owner[lng].brand }}</h1>
      <div class="meta-container">
        hi!~
        {%- assign tmp_obj =  site.data.owner[lng].contacts | where_exp: "item", "item.email != nil" | first -%}
        {%- assign email = tmp_obj['email'] -%}
        {%- if site.data.conf.others.about.show_email and email %}
          {%- assign _email = email | split: '@' %}
          <p class="email">
            <a href="javascript:void(0);" onclick="setAddress('{{ _email[0] }}', '{{ _email[1] }}');">
              {%- if site.data.conf.others.about.email_icon %}<i class="{{ 'fa-fw ' }}{{ site.data.conf.others.about.email_icon }}"></i>{% endif -%}
              &nbsp;{{ site.data.lang[lng].about.email_title }}
            </a>
          </p>
        {% endif -%}
        {%- if site.data.conf.others.about.show_contacts and site.data.owner[lng].contacts.size > 0 %}
          {% include default/nav/contact-links.html -%}
        {% endif -%}
      </div>
    </div>
  </div>
  <div class="row about-divider">
    <hr>
  </div>
  <div class="row">
    <div class="col-md-12">
      <div class="about-msg markdown-style">
       
       이곳은 머리의 메모리가 휘발성이라 여기에 끄적여나가는 장소입니다.
       
       그냥 혼자만의 기록이라고 보시면될것같습니다.
<p>
       저의 직업은 QA 입니다. 지속적으로 품질보증업무를 수행하고 있죠..
       
       쭈~욱 같은 업무를 하고 있네요..
</p>
<p>
       지금은 PostgreSQL 쪽 DB 와 온톨로지·AI 관련 일을 하고 있습니다.
       
       DB 내부 동작 분석이랑 지식그래프, LLM 답변 검증을 한꺼번에 병행하고 있네요..
       
       그러다 막힌 것들을 여기에 하나씩 적어둡니다.
</p>
<p>
      업무를 하면서 아래와 같은 제품들을 다뤄 봤습니다. 
</p>

<div class="resume">

  <section class="resume-section">
    <h2 class="resume-heading">거쳐온 도메인</h2>
    <ol class="resume-timeline">
      <li class="is-current">
        <span class="resume-period">현재</span>
        <div class="resume-detail">
          <h3 class="resume-role">DB · 온톨로지 · AI</h3>
          <ul class="resume-tags">
            <li>PostgreSQL</li>
            <li>온톨로지 / 지식그래프</li>
            <li>LLM 답변 평가 자동화</li>
          </ul>
        </div>
      </li>
      <li>
        <span class="resume-period">2023–2024</span>
        <div class="resume-detail">
          <h3 class="resume-role">안면인식</h3>
          <p class="resume-note">Facial Recognition</p>
        </div>
      </li>
      <li>
        <span class="resume-period">2019–2023</span>
        <div class="resume-detail">
          <h3 class="resume-role">카셰어링 서비스</h3>
        </div>
      </li>
      <li>
        <span class="resume-period">2018</span>
        <div class="resume-detail">
          <h3 class="resume-role">암호화폐 거래소</h3>
        </div>
      </li>
      <li>
        <span class="resume-period">2015–2018</span>
        <div class="resume-detail">
          <h3 class="resume-role">APM</h3>
          <p class="resume-note">Application Performance Monitoring</p>
        </div>
      </li>
      <li>
        <span class="resume-period">2015</span>
        <div class="resume-detail">
          <h3 class="resume-role">딜리버리 서비스</h3>
        </div>
      </li>
      <li>
        <span class="resume-period">2012–2015</span>
        <div class="resume-detail">
          <h3 class="resume-role">SAP</h3>
          <ul class="resume-tags">
            <li>BPC 7.5 / 10.0</li>
            <li>SAP HANA</li>
          </ul>
        </div>
      </li>
      <li>
        <span class="resume-period">2010–2012</span>
        <div class="resume-detail">
          <h3 class="resume-role">CCTV 영상 감시</h3>
          <ul class="resume-tags">
            <li>NVR</li>
            <li>Video Intelligence</li>
          </ul>
        </div>
      </li>
      <li>
        <span class="resume-period">2006–2010</span>
        <div class="resume-detail">
          <h3 class="resume-role">디지털 콘텐츠 보안</h3>
          <ul class="resume-tags">
            <li>DRM</li>
            <li>보안 USB</li>
            <li>CC 인증</li>
          </ul>
        </div>
      </li>
    </ol>
  </section>

  <section class="resume-section">
    <h2 class="resume-heading">기술 스택</h2>
    <ul class="resume-tags is-loose">
      <li>Java</li>
      <li>Python</li>
      <li>PostgreSQL</li>
      <li>온톨로지 / 지식그래프</li>
      <li>GraphRAG</li>
      <li>LLM-as-a-Judge</li>
      <li>AWS</li>
      <li>Docker</li>
      <li>Kubernetes</li>
      <li>Chef</li>
      <li>Ansible</li>
      <li>Jenkins</li>
      <li>JIRA</li>
      <li>JMeter</li>
      <li>LoadRunner</li>
      <li>Appium</li>
      <li>Selenium</li>
      <li>Cypress</li>
      <li>STAF</li>
      <li>FitNesse</li>
      <li>ISO/IEC 29119</li>
      <li>ISO 9126</li>
    </ul>
  </section>

  <section class="resume-section">
    <h2 class="resume-heading">해온 일</h2>
    <div class="resume-groups">

      <div class="resume-group">
        <h3 class="resume-group-title">품질 프로세스</h3>
        <ul class="resume-list">
          <li>ISO/IEC 29119 기반 테스트 체계와 배포 게이트를 릴리즈에 정착</li>
          <li>ISO 9126 품질 특성 모델로 품질 기준 정의</li>
          <li>테스트 케이스 설계</li>
          <li>테스트 케이스 관리툴 TestCaseCraft 개발 후 오픈소스 공개</li>
          <li>CC 인증 및 GS 인증 대응</li>
        </ul>
      </div>

      <div class="resume-group">
        <h3 class="resume-group-title">테스트 자동화</h3>
        <ul class="resume-list">
          <li>Appium · Cypress · Selenium · JMeter 를 Jenkins 에 연결해 매 빌드 회귀 검증 체계 구축</li>
          <li>수작업 회귀 검증을 자동화로 전환</li>
          <li>ML 모델 검증 자동화</li>
          <li>TestNG 데이터 주도(Data-driven) 테스트 구성</li>
        </ul>
      </div>

      <div class="resume-group">
        <h3 class="resume-group-title">AI · LLM 품질</h3>
        <ul class="resume-list">
          <li>정확성 · 완전성 · 충실성 · 적절성 4축 평가 기준 설계</li>
          <li>GraphRAG · 지식그래프 기반 응답 근거 검증</li>
          <li>규정 문서에서 평가용 정답지(GT) 자동 추출</li>
        </ul>
      </div>

      <div class="resume-group">
        <h3 class="resume-group-title">DB 품질</h3>
        <ul class="resume-list">
          <li>PostgreSQL DB 제품 응답 품질 검증</li>
          <li>PostgreSQL regression 테스트 구조 분석</li>
          <li>DB 회귀 테스트 파이프라인 운영</li>
        </ul>
      </div>

      <div class="resume-group">
        <h3 class="resume-group-title">CI · 빌드 자동화</h3>
        <ul class="resume-list">
          <li>CI(Jenkins, CruiseControl) 연동 Daily Build 자동화</li>
          <li>가상화 기반 테스트 환경 구축(Docker)</li>
          <li>디바이스팜 구성(오픈소스 기반)</li>
        </ul>
      </div>

      <div class="resume-group">
        <h3 class="resume-group-title">서버 · 클라우드</h3>
        <ul class="resume-list">
          <li>AWS 기반 서버 구축 및 운영</li>
          <li>클라우드 인프라 관리·운영</li>
          <li>Kubernetes 설치·구성 및 컨테이너 환경 운영</li>
          <li>Chef · Ansible 로 서버 구성 관리 자동화</li>
        </ul>
      </div>

    </div>
  </section>

  <section class="resume-section">
    <h2 class="resume-heading">자격 · 인증</h2>
    <ul class="resume-certs">
      <li>
        <strong>CISA</strong>
        <span>Certified Information Systems Auditor</span>
      </li>
      <li>
        <strong>ISTQB</strong>
        <span>International Software Testing Qualifications Board</span>
      </li>
      <li>
        <strong>GS 인증</strong>
        <span>Good Software 인증</span>
      </li>
    </ul>
  </section>

</div>
      </div>
    </div>
  </div>
</div>
