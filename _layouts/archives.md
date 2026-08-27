---
# Mr. Green Jekyll Theme - v1.1.0 (https://github.com/MrGreensWorkshop/MrGreen-JekyllTheme)
# Copyright (c) 2022 Mr. Green's Workshop https://www.MrGreensWorkshop.com
# Licensed under MIT

layout: default
# The Archives of posts.
---
{%- comment -%} collected before the list include, which reassigns lng_pages {%- endcomment -%}
{%- include multi_lng/get-pages-by-lng.liquid pages = site.posts -%}
{%- assign sideYears = lng_pages | sort: 'date' | reverse | group_by_exp:"post", "post.date | date: '%Y'" -%}

<div class="two-col-layout">
  <div class="two-col-main">
    <div class="multipurpose-container">
      <h1>{{ site.data.lang[lng].archives.page_header }}</h1>
      {%- include util/archives-list.html -%}
    </div>
  </div>

  <aside class="two-col-side">
    <section class="side-filter-group">
      <h5><i class="fa-fw {{ site.data.conf.posts.post_query_tabs_year_tab_icon }}" aria-hidden="true"></i>{{ site.data.lang[lng].post-list.upside_down_tabs.tab.years }}</h5>
      <ul class="side-filter-list">
        {%- for year in sideYears %}
        <li><a href="#year-{{ year.name }}">{{ year.name }}<span class="side-filter-count">{{ year.items.size }}</span></a></li>
        {%- endfor %}
      </ul>
    </section>
  </aside>
</div>
