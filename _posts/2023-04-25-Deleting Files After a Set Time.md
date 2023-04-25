---
layout: post
title: "[shell] 일정시간이 지난 파일삭제"
date:  2023-04-25 09:25:00 +0900
categories: shell

tags:
- shell
---


* 목차
{:toc}
_

ec2 나 서버를 관리할때 파일이 일정시간 지나면 삭제하는 스크립트이다.

특정 디랙토리 내의 수정 시간이 1달 이전인 디렉토리를 삭제하는 스크립트입니다.

오래된 파일을 보관하지 않아도될때 아래 스크립트를 사용하면 유용할것 같다.

아래 내용을 간단히 설명하면 
DIRECTORY 의 경로에 있는 파일을검색해서 30일 이 지난 파일을 삭제하고, 삭제된 파일을 보여준다.

만약 디랙토리에 30일이 경과된 파일이 없다면 삭제할 파일이 없다는 메세지를 화면상에 표출해준다.

```
#!/bin/bash

# 삭제할 파일이 저장된 디렉토리 경로를 지정합니다.
DIRECTORY="/path/"

# 현재 시간을 초로 계산합니다.
CURRENT_TIME=$(date +%s)

# 1달(30일) 전 시간을 초로 계산합니다.
ONE_MONTH_AGO=$(date -d "30 days ago" +%s)
deleted=false
# 디렉토리 내 모든 디렉토리를 확인하면서 수정 시간이 1달 이전인 디렉토리를 삭제합니다.
for DIR in ${DIRECTORY}*/; do
    if [ -d ${DIR} ]; then
        MODIFIED_TIME=$(stat -c %Y ${DIR})
        if [ ${MODIFIED_TIME} -lt ${ONE_MONTH_AGO} ]; then
            rm -rf ${DIR}
            echo "${DIR} 디렉토리 삭제 완료"
            deleted=true
       fi
    fi
done

if ! $deleted; then
    echo "삭제할 파일이 없습니다."
fi
```

수동으로 실행하면 의미가 없을듯하니 cron ,crontab 등에 등록해서 사용하면 유용할듯 합니다. 


그럼 오늘은 여기까지..

끝.
