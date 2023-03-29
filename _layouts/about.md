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
       
      2004년 부터 쭈~욱 같은 업무를 하고 있네요..
      
      업무를 하면서 아래와 같은 제품 들을 다뤄 들을 다뤄 봤습니다. 
    <hr>
<p>    
       ● 카쉐어링서비스(2019~onGoing) <br>
       ● 암호화페거래소(2018) <br>
       ● APM(Application monitoring management) (2015~2018) <br>
       ● 딜리버리서비스(2015) <br>
       ● SAP(2012~2015)<br>
        ✓ BPC 7.5,BPC 10.0 <br>
        ✓ SAP HANA<br>
       ● CCTV 카메라 감시(2010~2012)<br>
        ✓ NVR<br>
        ✓ VIDEO INTELLIGENCE <br>
       ● 디지털 컨텐츠 보안(2006~2010)<br>
       ✓ DRM(Digital rights management) Software<br>
       ✓ 보안USB<br>
       ✓ CC인증 <br>
       ● 임베디드 소프트웨어(2004~2006)<br>
       ✓ MP3 player<br>
       ✓ 에어컨 공조 컨트롤러<br>
       ✓ 냉장고 패드 컨트롤러 <br>
       ✓ TV 셋탑박스<br>

<hr>
       ● Skill set<br>
        ✓ JAVA<br>
        ✓ Python<br>
        ✓ AWS 적용 전반에 관한 경험 보유<br>
        ✓ QA 팀 셋업 및 QA 프로세스 정립<br>
        ✓ 클라우드 기반 인프라 관리 운영<br>
        ✓ Chef, Ansible 스크립트 작성 및 운영<br>
        ✓ Docker 및 가상화 환경 테스트 환경 구축<br>
        ✓ CC 인증 및 GS 인증 경험<br>
        ✓ 다양한 Testing tool 사용 경험(JIRA,Load Runner, Jmeter, Appium, Selenium, STAF, Fitness)<br>
        ✓ CI(Jenkins, CruiseControl) 와 연동한 Daily Build 및 자동화
        ✓ Open Source 및 상용소스와 연동 자동화 테스트 구축 및 운용<br>
<hr>
        ● Licence<br>
         ✓ CISA(Certified Information System Auditor)<br>
         ✓ PMP(Project Management Professional)<br>
         ✓ ISTQB(International Software Testing Qualifications Board)<br>
<hr>
      </div>
    </div>
  </div>
</div>
