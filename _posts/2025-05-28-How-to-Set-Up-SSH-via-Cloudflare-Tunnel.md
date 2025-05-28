---
layout: post
title: "[Cloudflare] How to Set Up SSH via Cloudflare Tunnel"
date:  2025-05-28 21:42:00 +0900
categories: cloudflare
How to Set Up SSH via Cloudflare Tunne

tags:
- cloudflare
- ssh
- tunnel
---


* 목차
{:toc}
_

---

## 왜 이런 작업을 하게 됐을까?

안녕하세요!

저번에 설치한 Odroid 를 열씸히 쓰고있습니다. 

개인적으로 하고있는 작업이 있는데  가끔 회사에서 열어보고 싶은 마음이 들더라고요 

상용툴은 아니고 그냥 필요해서 만들어쓰는 툴입니다.

일명 I Can Create Testcase 대충 필요한 기능을 내가 만들어쓰는 테스트 케이스 관리툴

회사에서 만드는 건아니고 개인적으로 만들고 있는 툴입니다.

<table>
  <tr>
    <td><img src="/assets/images/ict02.png" alt="ICT 이미지 02" width="120"></td>
  </tr>
</table>

어쨋든 이런걸 만들고 있는데 주말 같은데 친구만나고 잠깐 시간날때 뭔가를 수정한다거 나 하는 일이 있으면 openvpn 접속하고 하는데 

이런 방법이 아닌 다른 좀더 멋드러진 보안이 좀더 뛰어나다고 하는게 있더라고요.. 

클라우드플에어에서 제공하는 터널 기능을 그런 것이 있더라고요..

인터넷 찾아보니 최근것은 없고 해서 2025.05.28일 기준 (내가 작업한날짜) 으로 함께 정리해보았어요..

나중에 또 찾아보기 쉽게..

그럼 .. 시작해볼게요.


## Cloudflare Tunnel(구 Argo Tunnel)로 포트 개방 없이 안전하게 SSH 접속하기

Cloudflare Tunnel(구 Argo Tunnel)을 사용하면 서버의 인바운드 포트를 열지 않고도 안전하게 SSH 접속이 가능합니다. 

서버를 외부에서 접속하려면 일반적으로 방화벽에서 포트를 열거나(포트포워딩) 복잡한 네트워크 설정이 필요합니다. 

하지만 이 방식은 보안상 취약점이 생기기 쉽고, 관리도 번거롭다고 합니다. 

Cloudflare Tunnel(이전 명칭: Argo Tunnel)은 이런 문제를 근본적으로 해결해주는 솔루션이라는군요 

Cloudflare Tunnel을 활용해 서버의 인바운드 포트를 전혀 열지 않고도 안전하게 SSH로 접속하는 원리와 실제 적용 방법을 설명 해보겠습니다. 

### Cloudflare Tunnel이란?

Cloudflare Tunnel은 Cloudflare가 제공하는 제로 트러스트 네트워크 서비스로, 서버가 직접 외부에서 접근당하지 않도록 Cloudflare 네트워크와 안전한 아웃바운드 터널을 생성합니다. 

즉, 서버에서는 외부로만 접속을 열고, 외부에서 서버로 직접 들어오는 연결(인바운드 포트 개방)이 전혀 필요 없습니다.

cloudflared라는 경량 데몬이 서버에서 실행되어, Cloudflare 네트워크와 안전하게 연결을 맺습니다.

이 연결을 통해 HTTP, SSH 등 다양한 서비스를 외부에 노출할 수 있습니다.

Cloudflare Access와 연동하면 SSO, MFA 등 고급 인증 정책도 적용할 수 있습니다.

#### 왜 포트를 열지 않아도 되는가?
기존의 SSH 원격 접속 방식은 22번 포트(기본 SSH 포트)를 외부에 개방해야 했습니다. 이 경우, 무차별 대입 공격, 포트 스캐닝 등 각종 보안 위협에 노출됩니다.

Cloudflare Tunnel은 서버에서 Cloudflare로 아웃바운드(나가는) 연결만 생성합니다. 

외부에서 서버로 직접 접근하는 경로는 존재하지 않으므로, 서버의 방화벽에서 SSH 포트를 열 필요가 없습니다. 오직 Cloudflare 네트워크를 경유한 트래픽만 서버에 도달할 수 있습니다

---

## 1. 사전 준비

- Cloudflare 계정 및 도메인 보유
  (반드시 도메인이 있어야 하는지는 잘모르겠습니다. 어쨋든 나는 도메인이있으니..)
- 서버에 SSH(예: openssh-server) 설치 및 활성화
- 서버와 클라이언트 모두에 cloudflared 바이너리 설치

저같은 경우에는 odroid 에 macbook pro m2 를 가지고 접속하려고합니다.

그러니 나의 준비물은 
- odroid : Ubuntu 24.04
- Mac Pro : 2023년모델.. (벌써 이년이 흘럿구나...)
---

## 2. 서버에서 Cloudflare Tunnel 생성 및 연결
그럼 시작해보겠습니다. 

1. Cloudflare 에 로그인
2. Zero Trust> 대시보드에 들어갑니다.
3. "Network > Tunnels"에서 "Create a tunnel"을 클릭합니다.
4. Cloudflared 를 누릅니다.(Recommended 라고하니..)
5. 터널 이름을 지정하고, 안내에 따라 서버에 cloudflared를 설치합니다.
   - 저같은 경우에는 Odroid 라고 이름을 지정했어요.
   - Ubuntu 이니.. Debian 을 선택하니 아래와 같은 명령어를 입력하라고나옴.

```shell
# Add cloudflare gpg key
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# Add this repo to your apt repositories
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list

# install cloudflared
sudo apt-get update && sudo apt-get install cloudflared

```

설치가 완료되고 난후에 서비스를 시작하는 토큰값을 넣어주면됨.

화면에 나오는데로 따라하면됨


``` shell
sudo cloudflared service install eyJhIjo..

```

정상적으로 끝나면 아래에 커낵트 아이디와 정보가 나옴.

```shell
Connectors

Connector ID xxxxxx-xxxxxxxx-xxxxx-xxxxxx-xxxxxx Connected  2025.5.0

```
6. Next 를 누르면 도메인 정보와 Service를 입력하는 화면이 나타납니다. 

도메인에는 본인의 도메인 정보의 하위 도메인 정보를 생성해서 만들면됩니다.

저같은 경우는 xmlangel.uk 도메인이 있으므로그걸 지정해서했습니다. 

Public hostname 정보

``` shell
Subdomain : 사용할서버이름
Domain : 도메인주소(example.com)
```

Service 에는

```shell
Type : ssh
Url : localhost:22
```
7. 정보를 다 입력하고 나서 저장을 합니다.
   
8. 이제 cloudflared로 터널을 생성하고, 터널에 public hostname을 추가 합니다.

   - 서버에서 아래 명령어로 입력하면됩니다. hostname 은 보인이 설정한 도메인정보
   - url 은 url 에 입력한 정보를 입력하면됩니다.

- 예시 명령:
```
cloudflared tunnel --hostname ssh.example.com --url ssh://localhost:22

```
- 여기서 ssh.example.com은 Cloudflare에 등록된 도메인 하위 도메인입니다.

대충 아래와 같은 화면으로 수행이 됩니다.

중간에 WRN Erro 등이 나올수 있는데 몇번해보니 상관없는듯..합니다. 


``` shell
|➜  ~ sudo cloudflared service install eyJhIj
2025-05-28T13:54:36Z INF Using Systemd
2025-05-28T13:54:37Z INF Linux service for cloudflared installed successfully
|➜  ~ cloudflared tunnel --hostname ssh.example.com --url ssh://localhost:22
2025-05-28T14:03:52Z INF Thank you for trying Cloudflare Tunnel. Doing so, without a Cloudflare account, is a quick way to experiment and try it out. However, be aware that these account-less Tunnels have no uptime guarantee, are subject to the Cloudflare Online Services Terms of Use (https://www.cloudflare.com/website-terms/), and Cloudflare reserves the right to investigate your use of Tunnels for violations of such terms. If you intend to use Tunnels in production you should use a pre-created named tunnel by following: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
2025-05-28T14:03:52Z INF Requesting new quick Tunnel on trycloudflare.com...
2025-05-28T14:03:56Z INF +--------------------------------------------------------------------------------------------+
2025-05-28T14:03:56Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2025-05-28T14:03:56Z INF |  https://xp-experiences-remix-procedures.trycloudflare.com                                 |
2025-05-28T14:03:56Z INF +--------------------------------------------------------------------------------------------+
2025-05-28T14:03:56Z INF Cannot determine default configuration path. No file [config.yml config.yaml] in [~/.cloudflared ~/.cloudflare-warp ~/cloudflare-warp /etc/cloudflared /usr/local/etc/cloudflared]
2025-05-28T14:03:56Z INF Version 2025.5.0 (Checksum a62266fd02041374f1fca0d85694aafdf7e26e171a314467356b471d4ebb2393)
2025-05-28T14:03:56Z INF GOOS: linux, GOVersion: go1.22.10, GoArch: amd64
2025-05-28T14:03:56Z INF Settings: map[ha-connections:1 hostname:nas.qaspecialist.shop protocol:quic url:ssh://localhost:22]
2025-05-28T14:03:56Z INF cloudflared will not automatically update if installed by a package manager.
2025-05-28T14:03:56Z INF Generated Connector ID: b6f5a555-1b3e-4297-8cdb-d53d2b07eb26
2025-05-28T14:03:56Z INF Initial protocol quic
2025-05-28T14:03:56Z INF ICMP proxy will use 192.168.29.131 as source for IPv4
2025-05-28T14:03:56Z INF ICMP proxy will use fe80::5020:8f:54ce:62b8 in zone enp3s0 as source for IPv6
2025-05-28T14:03:56Z WRN The user running cloudflared process has a GID (group ID) that is not within ping_group_range. You might need to add that user to a group within that range, or instead update the range to encompass a group the user is already in by modifying /proc/sys/net/ipv4/ping_group_range. Otherwise cloudflared will not be able to ping this network error="Group ID 1000 is not between ping group 1 to 0"
2025-05-28T14:03:56Z WRN ICMP proxy feature is disabled error="cannot create ICMPv4 proxy: Group ID 1000 is not between ping group 1 to 0 nor ICMPv6 proxy: socket: permission denied"
2025-05-28T14:03:56Z INF ICMP proxy will use 192.168.29.131 as source for IPv4
2025-05-28T14:03:56Z INF ICMP proxy will use fe80::5020:8f:54ce:62b8 in zone enp3s0 as source for IPv6
2025-05-28T14:03:56Z INF Starting metrics server on 127.0.0.1:20242/metrics
2025-05-28T14:03:56Z INF Tunnel connection curve preferences: [CurveID(4588) CurveID(25497) CurveP256] connIndex=0 event=0 ip=198.41.200.193
2025/05/28 23:03:56 failed to sufficiently increase receive buffer size (was: 208 kiB, wanted: 7168 kiB, got: 416 kiB). See https://github.com/quic-go/quic-go/wiki/UDP-Buffer-Sizes for details.
2025-05-28T14:03:57Z INF Registered tunnel connection connIndex=0 connection=9e3a4c86-ed8e-449e-9fdf-e44aeaa5c10a event=0 ip=198.41.200.193 location=icn05 protocol=quic
```

---

## 3. Cloudflare Zero Trust에서 SSH 접근 정책 설정

- Zero Trust 대시보드에서 "Access > Applications"로 이동하여 "Add an application"을 클릭합니다.
- "Self-hosted"를 선택하고, Application domain에 ssh.example.com을 입력합니다.
- 인증 방식(예: One-time Pin, SSO 등)과 접근 허용 사용자/그룹을 지정합니다.

---

## 4. 클라이언트에서 SSH 접속 설정

- 클라이언트에도 cloudflared를 설치합니다.
- SSH 클라이언트 설정 파일(~/.ssh/config)에 아래와 같이 프록시 명령을 추가합니다:

Ubuntu 나 다른 os 는 설정을 참고해서 해보길.
일단 아래는 ubuntu
``` shell
Host ssh.example.com
  ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h
  User <서버_유저명>
```

난 맥이니 아래와 같이 설정했음.

``` shell

Host odroid.qaspecialist.shop
        ProxyCommand /opt/homebrew/bin/cloudflared access ssh --hostname %h
	      User user
```

- SSH 접속 시 cloudflared가 자동으로 Cloudflare 인증을 진행하고, 터널을 통해 서버로 접속합니다.


---

## 5. 접속 테스트

- 아래 명령으로 SSH 접속을 시도합니다:

``` shell
ssh [서버_유저명]@ssh.example.com
```

- 최초 접속 시 브라우저가 열리며 Cloudflare Access 인증을 요구할 수 있습니다. 인증 후 터미널에서 SSH 세션이 열립니다.

---

이 방법을 사용하면 외부에 SSH 포트를 노출하지 않고도 안전하게 SSH로 서버를 관리할 수 있다고합니다. 

안전하게 접속해서 이용하면됩니다.

그럼 오늘은 여기까지.

끝..

