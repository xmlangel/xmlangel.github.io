---
layout: post
title:  "Jekyll 에 Category 어떻게 추가하는거야?"
date:   2021-05-13 00:52:13 +0900
categories: etc update

tags:
- jekyll
- category
---
Jekyll 에 Category 항목을 추가하는 법
![PICT]({{ site.url }}/assets/images/jekyll-category.jpg){: width="100%" height="100%"}

* 목차
{:toc}

에잇 테그로만 관리하려고 했는데 카테고리로 관리하는게 편할것 같아서 Catetory 기능을 추가했다.

포스트 수가 얼마안되는데 카테고리가 꼭필요할까?
암튼 해보자.

## Github Page Jekyll 에 카테고리 추가하기

1. category 폴더만들기
2. _config.yml파일에 category list추가.
3. category/index.html 만들기
4. category 폴더에 category list에 추가한 리스트의 .md 파일생성
5. 생성한 카테고리에 맞게 category 지정.
