---
layout: post
title: "[VPN] Mac 에서 CommandLine 으로 VPN 활성화 하는 방법"
date:  2023-03-22 23:00:13 +0900
categories: VPN
img : "/assets/images/vpn.jpg"
tags:
- vpn
- mac
---


* 목차
{:toc}
_

![mac-vpn]({{ site.url }}/assets/images/vpn.jpg){: width="50%" height="50%"}

회사에서 업무를 진행하다 보면 VPN 환경에서 진행해야 하는 경우가 종종있다. 

- 개발 환경들이 외부에 노출이 되지 않아야 한다 거나, 
- 내부에 구축한 MacMini 에서 AWS 환경하의 서버들에 접근하는 경우라던가?
- 기타 이유로 특정한 VPN을 이용해서 붙어 야한다.

## VPN 구성 설정
macOS 에는 미리 구성된 VPN에 대한 연결을 설정할수 있다. 

1. 시스템 환경 설정을 엽니다.
2. 네트워크 아이콘을 클릭합니다.
3. 왼쪽 하단의 "+" 버튼을 클릭하여 새로운 VPN 구성을 추가합니다.
4. 인터페이스에서 "VPN"을 선택합니다.
5. VPN 유형에서 사용할 VPN 유형을 선택합니다.
6. 서비스 이름에 사용자가 원하는 이름을 입력합니다.
7. 구성에 필요한 서버 주소와 계정 정보를 입력합니다.
8. 인증 설정에서 사용자 인증서 또는 비밀번호를 설정합니다.
9. VPN 구성을 저장하고 완료합니다.
10. 이제 VPN에 연결하려면 시스템 환경 설정에서 VPN 구성을 선택하고 "연결" 버튼을 클릭합니다. VPN 연결을 끊으려면 동일한 구성을 선택하고 "끊기" 버튼을 클릭합니다.

|------|
|VPN설정|
|![mac-vpn]({{ site.url }}/assets/images/mac-vpn-01.png){: width="100%" height="100%"}|

이렇게 하면 화면에서 연결을 해야 한다.

시작할 수 있는 scutil 및 networksetup 과 같은 여러 명령줄 유틸리티가 포함되어 있다고 한다. 

터미널에서 아래의 명령어를 입력을 통해서 할수 있다고 한다. 

- 연결

```
sudo /usr/bin/env /usr/sbin/scutil --nc start "Connection Name" --secret "Password"
```

- 연결해제

```
sudo /usr/bin/env /usr/sbin/scutil --nc stop "Connection Name"
```

하지만 IKEv2/IPSEC VPN 구성에서 작동하지 않않는다. 이 로 인해 VPN 상태 표시줄 아이콘 활성화 해야한다.

## VPN 연결 Commandline으로

외부에서 툴을 다운받아서 설치한후에 사용하면된다. 

[vpnutil](https://github.com/Timac/VPNStatus/releases){:target="_blank"} 이라는 툴을 사용 하면 된다. 

작성 할 당시의 버전은 1.3이였다.

|------|
|vpnutil|
|![mac-vpn]({{ site.url }}/assets/images/mac-vpn-02.png){: width="100%" height="100%"}|


압축된 파일을 해제한 후 명령어를 실행하면 사용법이 나온다. 

간단한것같다. 

```shell
./vpnutil

Usage: vpnutil [start|stop] [VPN name]
Examples:
	 To start the VPN called 'MyVPN':
	 vpnutil start MyVPN

	 To stop the VPN called 'MyVPN':
	 vpnutil stop MyVPN

	 To list all available VPNs and their state:
	 vpnutil list

	 To get the status of the VPN called 'MyVPN':
	 vpnutil status MyVPN

Copyright © 2018-2021 Alexandre Colucci
blog.timac.org
```

1. 먼저 리스트를 확인하고
```
./vpnutil list
```

2. VPN을 시작해준다.
```
./vpnutil start VPN(본인이 설정한 VPN의 이름)
```

|------|
|vpnutil start|
|![mac-vpn]({{ site.url }}/assets/images/mac-vpn-03.png){: width="100%" height="100%"}|

간단히 툴하나깔아서 된다 역시 편하다...(과연? ) 

어쨋든 간단하게 하나 완료.. 

자동화를 한다거나 CI같은것들을 연결해서 사용해서 사용한다면 해당 명령어를 실행해서 사용 하면 된다.


오늘은 여기까지..

끝.
