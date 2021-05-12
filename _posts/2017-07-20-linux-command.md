---
layout: post
title:  "Linux Command 명령어"
date:   2017-07-20 10:50:13 +0900
categories: linux update
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

## 디랙토리별 파일의 용량확인
어느 디렉토리에서 용량을 많이 사용하고 있는지 궁금할 때가 있다. 이 때 각 디렉토리별 용량을 확인하기 위해 필요한 명령어다.
{% highlight bash %}
du -h --max-depth=1
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

## Crontab 주기
크론tab의 주기를 볼수 있는 웹페이지 [crontab](https://crontab.guru/)

## Ubuntu repo 변경
느린 외국 repo 가 아닌 한국 repo로 변경
archive.ubuntu.com(또는 kr.archive.ubuntu.com) 로 되어있는것을 ftp.daumkakao.com 로 바꿔면된다.

{% highlight bash %}
sudo sed -i 's/archive.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list
sudo sed -i 's/security.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list
sudo sed -i 's/extras.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list
apt-get clean
apt-get update
{% endhighlight %}  
       
