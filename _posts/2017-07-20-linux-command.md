---
layout: post
title:  "Linux Command 명령어"
date:   2017-07-20 10:50:13 +0900
categories: jekyll update
comments: true
tags :
- linux
- command
---

find, grep, egrep, du-sk, ps-ef 간단사용법
* 목차
{:toc}

## 파일찾기
{% highlight bash %}
find . -name core -exec rm -i {} \;
find / -xdev -size +100000000c -exec ll {} \;    <-- 100M이상 파일찾기
{% endhighlight %}
 
## 특정파일유형에서 단어찾기
{% highlight bash %}
find . -name '*.sh' -print |xargs grep 'se jong'
find . -name '*.sh' -print |xargs grep 'CSBS Hit Now(' /home/svc/regist.sh
find . -type f | xargs grep "less than 5"
{% endhighlight %}

## cron 실행정상유무확인
{% highlight bash %}
tail -100 /var/adm/cron/log  <-- HP  
tail -100 /var/log/cron​          <-- Linux
﻿{% endhighlight %}

## 같은내용에서 또다시 추릴때
{% highlight bash %}
 grep -i "Apr 24" alert*log | grep -c "ORA-00060"
 {% endhighlight %}

-i 는 대문자 소문자 상관없이 찾는 옵션.
-c 는 "ORA-00060" 을 포함하는 줄 합계를 구하는 옵션
 
##  egrep 으로 2개이상의 같은 단어를 찾을때
{% highlight bash %}
cat /var/adm/syslog/syslog.log|grep "May" |egrep -i "error|failed|fault|EMS"
egrep -i 'echo|discard' /etc/services
vgdisplay -v vg_ora1 | egrep 'Name|Size'
{% endhighlight %}

## 폴더내 파일의 용량별 정렬할때
{% highlight bash %}
du -sk ./* | sort -nr
{% endhighlight %}

## ps -ef 확인
pid 값 확인

{% highlight bash %}
ps -ef | grep 검색어 | awk '{print $2}'
{% endhighlight %}

## 확인된 pid kill 함
{% highlight bash %}
ps -ef | grep 검색어 | awk '{print $2}'| xargs kill -9     
{% endhighlight %}

##  로그 점검시
{% highlight bash %}
grep make_ /var/opt/ignite/recovery/latest/recovery.log  <-- HP ignite백업
grep -i -e error -e fail /var/adm/syslog/syslog.log   <-- HP syslog
tail -f /var/adm/rc.log    <-- HP 부팅 후 프로세스가 정상수행됐는지..
{% endhighlight %}