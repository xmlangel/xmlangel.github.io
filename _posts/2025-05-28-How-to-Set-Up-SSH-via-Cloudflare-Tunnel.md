---
layout: post
title: "[Cloudflare] How to Set Up SSH via Cloudflare Tunnel
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
    <td><img src="/assets/images/ict01.png" alt="ICT 이미지 01" width="120"></td>
    <td><img src="/assets/images/ict02.png" alt="ICT 이미지 02" width="120"></td>
    <td><img src="/assets/images/ict03.png" alt="ICT 이미지 03" width="120"></td>
    <td><img src="/assets/images/ict04.png" alt="ICT 이미지 04" width="120"></td>
    <td><img src="/assets/images/ict05.png" alt="ICT 이미지 05" width="120"></td>
  </tr>
</table>

어쨋든 이런걸 만들고 있는데 주말 같은데 친구만나고 잠깐 시간날때 뭔가를 수정한다거 나 하는 일이 있으면 openvpn 접속하고 하는데 

이런 방법이 아닌 다른 좀더 멋드러진 보안이 좀더 뛰어나다고 하는게 있더라고요.. 

클라우드플에어에서 제공하는 터널 기능을 그런 것이 있더라고요..

인터넷 찾아보니 최근것은 없고 해서 2025.05.28일 기준 (내가 작업한날짜) 으로 이미지와 함께 정리해보았어요..

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

**1. 사전 준비**

- Cloudflare 계정 및 도메인 보유
  (반드시 도메인이 있어야 하는지는 잘모르겠습니다. 어쨋든 나는 도메인이있으니..)
- 서버에 SSH(예: openssh-server) 설치 및 활성화
- 서버와 클라이언트 모두에 cloudflared 바이너리 설치

저같은 경우에는 odroid 에 macbook pro m2 를 가지고 접속하려고합니다.

그러니 나의 준비물은 
- odroid : Ubuntu 24.04
- Mac Pro : 2023년모델.. (벌써 이년이 흘럿구나...)
---

**2. 서버에서 Cloudflare Tunnel 생성 및 연결**
그럼 시작해보겠습니다. 

1. Cloudflare 에 로그인

2. Zero Trust> 대시보드에 들어갑니다.

<table>
  <tr>
    <td><img src="/assets/images/cloudflare01.png" alt="cloudflare 이미지 01" width="200"></td>
  </tr>
</table>   

3. "Network > Tunnels"에서 "Add a tunnel"을 클릭합니다.
5. 터널 이름을 지정하고, 안내에 따라 서버에 cloudflared를 설치합니다.
6. cloudflared로 터널을 생성하고, 터널에 public hostname을 추가합니다.
    - 예시 명령:

```
cloudflared tunnel --hostname ssh.example.com --url ssh://localhost:22
```

    - 여기서 ssh.example.com은 Cloudflare에 등록된 도메인 하위 도메인입니다.

---

**3. Cloudflare Zero Trust에서 SSH 접근 정책 설정**

- Zero Trust 대시보드에서 "Access > Applications"로 이동하여 "Add an application"을 클릭합니다.
- "Self-hosted"를 선택하고, Application domain에 ssh.example.com을 입력합니다.
- 인증 방식(예: One-time Pin, SSO 등)과 접근 허용 사용자/그룹을 지정합니다.

---

**4. 클라이언트에서 SSH 접속 설정**

- 클라이언트에도 cloudflared를 설치합니다.
- SSH 클라이언트 설정 파일(~/.ssh/config)에 아래와 같이 프록시 명령을 추가합니다:

```
Host ssh.example.com
  ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h
  User <서버_유저명>
```

- SSH 접속 시 cloudflared가 자동으로 Cloudflare 인증을 진행하고, 터널을 통해 서버로 접속합니다.

---

**5. 접속 테스트**

- 아래 명령으로 SSH 접속을 시도합니다:

```
ssh [서버_유저명]@ssh.example.com
```

- 최초 접속 시 브라우저가 열리며 Cloudflare Access 인증을 요구할 수 있습니다. 인증 후 터미널에서 SSH 세션이 열립니다[^6].

---

이 방법을 사용하면 외부에 SSH 포트를 노출하지 않고도 안전하게 SSH로 서버를 관리할 수 있습니다.
