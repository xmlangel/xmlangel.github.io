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

안녕하세요!
저번에 Odroid 를 항시 열어놓고 있는데 가끔 회사에서 열어보고 싶을마음이 들더라고요 ..

그래서 찾아보니 방법이 있어라고요.. 

그래도 오늘은 찾아보고 실행한 내용을 정리해서 적어놓아요.

---

## 왜 이런 작업을 하게 됐을까?

요즘 테스트 케이스 관리툴을 만들고 있습니다. 

상용툴은 아니고 그냥 필요해서 만들어쓰는 툴입니다.

일명 I Can Create Testcase 

## Cloudflare Tunnel을 통한 SSH 접속 설정 방법

Cloudflare Tunnel(구 Argo Tunnel)을 사용하면 서버의 인바운드 포트를 열지 않고도 안전하게 SSH 접속이 가능합니다. 아래는 대표적인 설정 방법입니다.

---

**1. 사전 준비**

- Cloudflare 계정 및 도메인 보유
- 서버에 SSH(예: openssh-server) 설치 및 활성화
- 서버와 클라이언트 모두에 cloudflared 바이너리 설치

---

**2. 서버에서 Cloudflare Tunnel 생성 및 연결**

1. Cloudflare Zero Trust 대시보드에 로그인합니다.
2. "Network > Tunnels"에서 "Add a tunnel"을 클릭합니다.
3. 터널 이름을 지정하고, 안내에 따라 서버에 cloudflared를 설치합니다.
4. cloudflared로 터널을 생성하고, 터널에 public hostname을 추가합니다.
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
