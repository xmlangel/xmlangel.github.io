---
layout: post
title: "[Cloudflare] Cloudflare Tunnel로 SSH 안전하게 연결하기"
date: 2025-05-28 21:42:00 +0900
categories: cloudflare
tags:

- cloudflare
- ssh
- tunnel
---

* 목차
{:toc}

---

## 왜 이 작업을 하게 됐을까요?

안녕하세요!

최근에 Odroid를 설치해서 잘 쓰고 있는데, 개인적으로 만든 툴을 회사에서도 잠깐씩 확인하고 싶을 때가 있더라고요.
이 툴은 상용툴은 아니고, 제가 필요해서 직접 만든 테스트 케이스 관리툴입니다.

<table>
  <tr>
    <td><img src="/assets/images/ict02.png" alt="ICT 이미지 02" width="120"></td>
  </tr>
</table>
주말이나 친구 만날 때, 짬날 때마다 뭔가 수정하려면 기존에는 openvpn으로 접속했는데,
조금 더 편하고 보안도 좋은 방법이 없을까 찾다가 Cloudflare에서 제공하는 터널 기능을 알게 됐어요.

인터넷에 최신 정보가 별로 없어서, 2025.05.28 기준으로 정리해봅니다.
나중에 저도 다시 찾아보기 쉽게요.

그럼, 시작해볼게요!

---

## Cloudflare Tunnel(구 Argo Tunnel)로 포트 개방 없이 안전하게 SSH 접속하기

Cloudflare Tunnel(예전 이름은 Argo Tunnel)을 이용하면 서버의 인바운드 포트를 열지 않고도 안전하게 SSH 접속을 할 수 있습니다.

보통 외부에서 서버에 접속하려면 방화벽에서 포트를 열거나(포트포워딩) 네트워크 설정이 꽤 번거롭죠.
이런 방식은 보안상 위험할 수도 있고 관리도 귀찮아요.

Cloudflare Tunnel은 이런 문제를 깔끔하게 해결해주는 솔루션입니다.
이 글에서는 인바운드 포트 개방 없이 SSH로 접속하는 원리와 실제 적용 방법을 쉽게 설명해볼게요.

### Cloudflare Tunnel이란?

Cloudflare Tunnel은 Cloudflare가 제공하는 제로 트러스트 네트워크 서비스입니다.
서버가 직접 외부에 노출되지 않고, Cloudflare 네트워크와 안전하게 아웃바운드 터널을 만듭니다.

즉, 서버에서는 외부로만 연결을 만들고, 외부에서 서버로 바로 들어오는 연결(인바운드 포트 개방)은 필요 없습니다.

서버에서 cloudflared라는 작은 데몬을 실행하면, Cloudflare 네트워크와 안전하게 연결됩니다.
이 연결을 통해 HTTP, SSH 등 다양한 서비스를 외부에 노출할 수 있고,
Cloudflare Access와 연동하면 SSO, MFA 등 고급 인증도 쓸 수 있습니다.

#### 왜 포트를 안 열어도 될까요?

예전 방식은 22번 SSH 포트를 외부에 열어야 했죠.
이러면 무차별 대입 공격이나 포트 스캐닝 같은 보안 위협에 노출됩니다.

Cloudflare Tunnel은 서버에서 Cloudflare로 나가는 연결만 만듭니다.
외부에서 서버로 바로 접근하는 경로가 없으니, 방화벽에서 SSH 포트를 열 필요가 없어요.
오직 Cloudflare 네트워크를 거친 트래픽만 서버에 들어올 수 있습니다.

---

## 1. 준비물

- Cloudflare 계정과 도메인
- 서버에 SSH(예: openssh-server) 설치 및 활성화
- 서버와 클라이언트 모두에 cloudflared 설치

저는 odroid(Ubuntu 24.04)와 MacBook Pro(M2, 2023년형) 조합으로 진행했습니다.

---

## 2. 서버에서 Cloudflare Tunnel 만들기

1. Cloudflare에 로그인
2. Zero Trust 대시보드로 이동
3. "Network > Tunnels"에서 "Create a tunnel" 클릭
4. Cloudflared 선택(Recommended)
5. 터널 이름 지정하고 안내에 따라 서버에 cloudflared 설치

예시(Ubuntu/Debian):

```shell
# Cloudflare GPG 키 추가
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# apt 저장소 추가
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list

# cloudflared 설치
sudo apt-get update && sudo apt-get install cloudflared
```

설치 후, 서비스 시작할 때 토큰값을 입력하라는 안내가 나옵니다.

```shell
sudo cloudflared service install <토큰값>
```

정상적으로 연결되면 Connector ID 등 정보가 나옵니다.

6. Next를 누르면 도메인과 Service 정보를 입력하는 화면이 나옵니다.
도메인은 본인 도메인의 하위 도메인을 지정하면 됩니다.

예시:

- Subdomain: 사용할 서버 이름
- Domain: 본인 도메인(example.com)
- Service Type: ssh
- Url: localhost:22

7. 정보 입력 후 저장
8. cloudflared로 터널과 public hostname 추가
```shell
cloudflared tunnel --hostname ssh.example.com --url ssh://localhost:22
```

여기서 ssh.example.com은 Cloudflare에 등록한 하위 도메인입니다.

---

## 3. Cloudflare Zero Trust에서 SSH 접근 정책 설정

- Zero Trust 대시보드 > "Access > Applications" > "Add an application"
- "Self-hosted" 선택, Application domain에 ssh.example.com 입력
- 인증 방식(One-time Pin, SSO 등)과 접근 허용 사용자/그룹 지정

---

## 4. 클라이언트에서 SSH 접속 설정

- 클라이언트에도 cloudflared 설치
- SSH 설정(~/.ssh/config)에 프록시 명령 추가

예시(Ubuntu):

```shell
Host ssh.example.com
  ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h
  User <서버_유저명>
```

예시(Mac):

```shell
Host odroid.qaspecialist.shop
  ProxyCommand /opt/homebrew/bin/cloudflared access ssh --hostname %h
  User <서버_유저명>
```

이렇게 하면 SSH 접속 시 cloudflared가 자동으로 Cloudflare 인증을 진행하고, 터널을 통해 서버에 접속합니다.

---

## 5. 접속 테스트

아래 명령으로 SSH 접속을 시도해보세요.

```shell
ssh [서버_유저명]@ssh.example.com
```

최초 접속 시 브라우저가 열리며 Cloudflare Access 인증을 요구할 수 있습니다.
인증 후 터미널에서 SSH 세션이 열립니다.

---

이 방법을 쓰면 SSH 포트를 외부에 노출하지 않고도 안전하게 서버를 관리할 수 있습니다.
편하게, 그리고 안전하게 서버를 이용하세요!

오늘은 여기까지입니다.
끝!

