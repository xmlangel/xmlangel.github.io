---
layout: post
title: "[odroid] Odroid XU4/HC1에서 microSD로 부팅하고 SSD/HDD를 루트로 쓰는 꿀팁!"
date:  2025-05-09 20:40:00 +0900
categories: odriod

tags:
- odroid
- ubuntu
- nas
---


* 목차
{:toc}
_

안녕하세요!
오늘은 Odroid XU4, HC1 같은 구형 보드에서
**microSD는 부트용, SSD/HDD는 루트 파일시스템**으로 쓰는 방법을 정리해볼게요.

microSD는 느리고 수명도 짧아서, SSD나 HDD로 옮기면 속도도 빨라지고 안정성도 훨~씬 좋아집니다!
저도 직접 해보고 완전 만족했던 꿀팁이라, 여러분도 꼭 한번 해보시길 추천드려요 😊

참고로, 신형 보드는 이 작업이 필요 없다고 하니 신형 쓰시는 분들은 패스하셔도 됩니다!

---

## 왜 이런 작업을 하게 됐을까?

집에 굴러다니는 Odroid, SSD, 하드 같은 장비를 그냥 놀리기 아까워서
"이걸로 뭘 해볼까?" 고민하다가 NAS도 만들고, 서버도 돌려보고 싶었거든요.

근데 하드를 연결해보니
중간중간 전원이 나가서 그런지 하드가 갑자기 "딱딱" 돌아가는 소리가 들리더라고요.
그래서 평소엔 꺼두고, 필요할 때만 켜는 번거로움이 생겼어요. (전기세는 아끼지만…)

또 집에 공유기(OpenVPN 지원되는 AC1900)가 있는데,
언제부턴가 OpenVPN 접속이 안 되더라고요.
HTTPS가 아니라서 그런가 싶기도 하고, 원인 찾기가 귀찮아서
"그냥 내가 직접 오드로이드에 OpenVPN 서버를 올려볼까?" 생각이 들었습니다.

그리고 NAS 용도로 aoostar wtr pro도 사봤는데,
팬 소음이 커서 평소엔 꺼두고 필요할 때만 켜게 되더라고요.
그래서 "차라리 조용한 Odroid로 NAS를 굴려보자!" 싶어서
남는 장비들을 활용해보게 됐습니다.

---

## 1. microSD에 OS 설치 \& 부팅 확인

1. Odroid 공식 이미지(우분투)를 microSD에 플래싱!

[ODROID-XU3/XU4 Ubuntu 이미지](https://dn.odroid.com/5422/ODROID-XU3/Ubuntu/){:target="_blank"}{:rel="noopener noreferrer"}
여기에서 X4 용으로 받아서..하면됨.
   
2. Odroid에 microSD를 꽂고 정상적으로 부팅되는지 확인하세요.

부팅이 안되도 여러번 해보다보면 됨.. 안되면 될때까지.. 이미지 선택만 잘하면 실패할일 없음.
   

---

## 2. SSD/HDD 연결 \& 포맷하기

1. **SSD/HDD 연결**
USB-SATA 어댑터(또는 HC1은 SATA)에 SSD/HDD를 연결합니다.
2. **디스크 인식 확인**

```bash
lsblk
```

`/dev/sda` 또는 `/dev/sdb`로 보이면 OK!
3. **파티션 만들기(필요하면)**

```bash
sudo fdisk /dev/sda
```

    - `d`로 기존 파티션 삭제
    - `n`으로 새로 만들기
    - `w`로 저장
4. **포맷(ext4 추천!)**

```bash
sudo mkfs.ext4 /dev/sda1
```

5. **마운트**

```bash
sudo mkdir /mnt/ssd
sudo mount /dev/sda1 /mnt/ssd
```


---

## 3. 루트 파일 복사하기

- **rsync로 한 번에 싹 복사! (2번 반복 추천)**

```bash
sudo rsync -aAXv --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} / /mnt/ssd
```

복사 중 파일이 바뀔 수 있으니, 두 번 돌려주면 더 안전해요!

---

## 4. SSD/HDD UUID 확인

```bash
sudo blkid /dev/sda1
```

예시 결과:
`/dev/sda1: UUID="abcd-1234-ef56-7890" TYPE="ext4"`

---

## 5. 부트로더 설정(boot.ini 수정)

- microSD의 `/media/boot/boot.ini` 파일 열어서
`root=UUID=abcd-1234-ef56-7890`로 바꿔주세요!

```
setenv bootrootfs "console=tty1 console=ttySAC2,115200n8 root=UUID=abcd-1234-ef56-7890 rootwait ro fsck.repair=yes net.ifnames=0"
```

- UUID 대신 `/dev/sda1`로 해도 되지만, UUID가 더 안전합니다!

---

## 6. fstab도 수정!

- `/mnt/ssd/etc/fstab` 파일에서
루트(/) 파티션을 SSD/HDD로 변경해줍니다.

```
UUID=abcd-1234-ef56-7890 / ext4 defaults,noatime 0 1
```

- 기존 `/dev/mmcblk0p2` 등은 주석 처리하거나 삭제!

---

## 7. 재부팅 \& 확인

1. SSD에 파일이 잘 복사됐는지 확인!

```bash
ls /mnt/ssd
```

2. 재부팅!

```bash
sudo reboot
```

3. 부팅 후 루트가 SSD인지 확인!

```bash
mount | grep ' / '
```

`/dev/sda1 on / type ext4` 이렇게 나오면 성공!

---

## 8. microSD의 /boot 자동 마운트

- 시스템 업데이트 시 부트 파티션이 잘 마운트되게 `/etc/fstab`에 추가:

```
UUID=abcd-1234-ef56-7890 / ext4 errors=remount-ro,noatime 0 1
LABEL=boot /media/boot vfat defaults 0 1

```

- 적용:

```bash
sudo mount /media/boot
```

---

- 이제 microSD는 부트로더/커널만 담당하고,
실질적인 시스템 구동은 SSD/HDD에서 이뤄집니다!
- 속도도 빨라지고, SD카드 수명 걱정도 끝!
SSD 수명이 다할때까지 쭈~욱 사용해주도록하마... 

- SSD로 옮기면 정말 쾌적해져요. 강추👍

끝.

#Odroid #XU4 \#HC1 \#SSD부팅 \#microSD \#리눅스팁 \#갓성비NAS \#취미서버

