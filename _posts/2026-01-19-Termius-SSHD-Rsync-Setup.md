---
layout: post
title: "[Termius] 안드로이드 폰에 SSH 서버 구축하고 Rsync로 파일 전송하기 (ft. ssh-copy-id)"
date: 2026-01-19 09:05:00 +0900
categories: android
tags:
- termius
- ssh
- rsync
- android
- ssh-copy-id
---

* 목차
{:toc}

---

평소 PC와 안드로이드 폰 간에 파일을 주고받을 때 케이블을 연결하거나 클라우드를 거치는 것이 번거로울 때가 있습니다.  
특히 개발자라면 터미널 환경에서 `rsync`를 이용해 빠르고 효율적으로 파일을 동기화하고 싶은 욕구가 생기죠.

이번 글에서는 안드로이드 폰에 **Termius** 앱을 설치하여 SSH 서버(SSHD)를 구동하고, PC에서 **ssh-copy-id**로 키 기반 인증을 설정한 뒤 **rsync**로 파일을 전송하는 과정을 정리해보았습니다.

비 개발자는 약간 어려울수 있어요.

## 1. Termius 앱 설치 및 준비

가장 먼저 할 일은 안드로이드 폰에 Termius 앱을 설치하는 것입니다.
구글 플레이 스토어에서 `Termius`를 검색하여 다운로드합니다. 이 앱은 훌륭한 SSH 클라이언트이기도 하지만, **Local Terminal** 환경과 **SSH Server** 기능도 제공합니다.

1. 플레이 스토어에서 **Termius** 설치
2. 앱 실행 및 로그인 (계정이 없다면 생성)

<img src="/assets/images/2026-01-19-termius-googleplay.png" alt="Termius Google Play" width="60%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

## 2. 폰에서 SSHD 서버 설정하기

Termius 앱 내에서 SSH 서버를 활성화하고 접속 비밀번호를 설정해야 합니다.
Termius 앱의 **Local Terminal** (로컬 터미널) 기능을 이용하여 SSH 서버 패키지를 설치하고 실행해야 합니다.

1. **패키지 업데이트 및 OpenSSH 설치**
   Termius의 Local Terminal을 열고 다음 명령어를 입력합니다.
   ```bash
   pkg update && pkg upgrade
   pkg install openssh
   ```

2. **비밀번호(Password) 설정**
   외부에서 접속할 때 사용할 비밀번호를 설정합니다.
   ```bash
   passwd
   # 입력 프롬프트가 뜨면 비밀번호를 입력합니다.
   ```
비밀번호를 기억해놓으세요 

3. **SSHD 서버 실행 및 사용자 정보 확인**
   서버를 구동하고, 내 ID와 IP를 확인합니다.
   ```bash
   sshd
   whoami
   ```
<img src="/assets/images/2026-01-19-termius-whoami.png" alt="whoami" width="60%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
보이는것과 같이 보통 u0_a폰모델 형식으로 아이디를 확인할수 있어요. 제폰은 s24이므로 a24와 같은 형식으로 나옵니다.



4. **포트 확인**: 안드로이드는 1024번 이하 포트를 루팅 없이 사용할 수 없으므로, 보통 `8022` 포트를 사용합니다.

## 3. PC에서 SSH 접속 테스트

이제 PC(Mac 또는 Linux, Windows WSL)의 터미널을 열고 접속을 시도해봅니다.  
폰과 PC는 **동일한 와이파이 네트워크**에 있어야 합니다.

```bash
# 폰의 IP 주소가 192.168.0.10 이라고 가정
# 포트는 8022 (앱 기본 설정에 따름)
ssh -p 8022 u0_a123@192.168.0.10
```
  
* `u0_a123`: 안드로이드 사용자 ID (보통 `whoami` 명령어로 폰 터미널에서 확인 가능)
* 비밀번호 입력 프롬프트가 뜨면, 아까 설정한 비밀번호를 입력합니다.

접속이 성공했다면 절반은 성공입니다!

## 4. ssh-copy-id로 비밀번호 없이 접속하기

매번 비밀번호를 치는 것은 번거롭습니다. `ssh-copy-id`를 이용해 PC의 공개키(Public Key)를 폰에 등록해줍시다.

### 4.1 PC에 SSH 키가 없다면?
먼저 키가 있는지 확인하고 없다면 생성합니다.
```bash
ls ~/.ssh/id_rsa.pub
# 파일이 없다면 생성
ssh-keygen -t rsa -b 4096
# 엔터만 누르면 기본 경로에 생성됨
```

### 4.2 공개키 전송
이제 `ssh-copy-id` 명령어를 사용합니다.

```bash
ssh-copy-id -p 8022 u0_a123@192.168.0.10
```

명령어를 실행하면 처음 한번은 폰의 비밀번호를 물어봅니다. 입력해주면 PC의 공개키가 폰의 `~/.ssh/authorized_keys`에 자동으로 추가됩니다.

이제 다시 SSH 접속을 시도해보세요. 비밀번호 없이 바로 접속될 것입니다.

```bash
ssh -p 8022 u0_a123@192.168.0.10
# 비밀번호 없이 로그인 성공!
```

## 5. Rsync 설정 및 파일 전송

이제 파일을 동기화할 차례입니다. 폰(Termius/Termux 환경)에 `rsync`가 설치되어 있어야 합니다. 없다면 패키지 매니저(`pkg` 또는 `apt`)를 통해 설치합니다.

```bash
# 폰 터미널에서 실행
pkg install rsync
```

### 5.1 PC에서 폰으로 파일 보내기
이제 PC에서 작업한 파일이나 폴더를 폰으로 전송해봅시다.

```bash
# 로컬의 files 폴더를 폰의 storage/shared/Download 폴더로 동기화
rsync -avz -e 'ssh -p 8022' ./files/ u0_a123@192.168.0.10:~/storage/shared/Download/
```

* `-a`: 아카이브 모드 (권한, 시간 등 보존)
* `-v`: 상세 출력
* `-z`: 전송 시 압축
* `-e 'ssh -p 8022'`: SSH 포트가 기본 22번이 아니므로 포트 지정

### 5.2 폰의 파일을 PC로 가져오기
반대로 폰의 사진이나 문서를 PC로 가져올 수도 있습니다.

```bash
rsync -avz -e 'ssh -p 8022' u0_a123@192.168.0.10:~/storage/shared/DCIM/Camera/ ./my_photos/
```

---

이렇게 Termius(또는 Termux) 환경과 Rsync를 활용하면, 케이블 연결 없이도 매우 빠르고 안정적으로 파일을 관리할 수 있습니다. 특히 `ssh-copy-id`를 통해 인증 과정을 자동화해두면, 스크립트를 짜서 매일 밤 자동으로 백업하는 등의 활용도 가능해집니다.

저같은 경우는 구글 픽셀폰이 있어서 Rsync 기능을 이용해서 백업을 해서 업로드 하고있습니다.

이렇게 하는 방법도 있구나 하는 정도만 참고해보시길..

끝.