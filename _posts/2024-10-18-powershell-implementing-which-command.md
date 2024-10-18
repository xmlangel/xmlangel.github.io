---
layout: post
title: "[Powershell] which 를 윈도우에서 사용하기"
date:  2024-10-18 09:00:00 +0900
categories: powershell

tags:
- powershell
- which
---


* 목차
{:toc}
_

Mac 만 쓰다가 회사가 에서는 mac 을 쓰지 않는 환경에서 일을 하게 되었다.
과거에는 Windows 가 편했는데 이제는 Mac 이 더 편한것같다.(하지만 Apple 이 마냥좋은것만은아니다.)
그래서 어떻게 하면 Mac/linux 에서 검색하는 which 를 같이 쓸수 있을지 고민을 하였다.

which 와 같은 것을 그대로 사용하는 방법을 생각해보니 스크립트를 만들면 될것같았다.

Get-Command 같은 명령어를 이용하면 되겠지만 그것도 학습하는데 시간이 걸리는 것같아 which 명령어를 만들어서 사용하기로 하였다.

Powershell 에서는 $PROFILE 에 커스텀 스크립트를 만들어서 쓸수 있는 방법을 알아내었다. 

Powershell command-line 에서 $PROFILE 를 하면 해당위치가 나온다.
```
 PS C:\Users\USER> $profile
C:\Users\USER\Documents\WindowsPowerShell\Microsoft.PowerShellISE_profile.ps1
```

위 경로의 파일을 에디터 에서 수정해서 which 함수를 만들어서 사용하면 된다.

```
function which {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Command
    )
    
    $commandInfo = Get-Command $Command -ErrorAction SilentlyContinue
    
    if ($commandInfo) {
        return $commandInfo.Source
    } else {
        Write-Host "Command '$Command' not found."
    }
}
```

파일 저장 후 PowerShell 다시 시작 하면 프로필 파일이 자동으로 로드되면서 which 함수가 활성화되어 사용이 가능하다.

그럼 오늘은 여기까지..

끝.
