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
### 주요 특징
Samsung Exynos ARMv7 Processor rev 3 (v7l)는 삼성의 Exynos 시리즈 SoC(System on Chip)에서 사용된 ARMv7 아키텍처 기반의 프로세서가 탑제 되어있던놈이다.

사실 가진정확안 모델은 아래와 같다. 베이스가 ODROID-XU4 라고 하니 일단 넘어가자..

- ODROID-HC1 : Home Cloud One
```
The HC1 is based on the very powerful ODROID-XU4 platform and it can run Samba, FTP, NFS, SSH, NGINX, Apache, SQL, Docker, WordPress and other server software smoothly with full Linux distributions like Ubuntu, Debian, Arch and OMV. Available and ready-to-go OS distributions are on our WiKi. Any OS for XU4 is fully compatible with the HC1. https://wiki.odroid.com/odroid-xu4/os_images/os_images
```

이 프로세서는 주로 2010년대 초중반의 스마트폰, 태블릿 등에서 널리 사용되었다고한다.

| 항목                        | 사양 및 설명 |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CPU                         | Samsung Exynos5422 ARM® Cortex™-A15 Quad 2.0GHz / Cortex™-A7 Quad 1.4GHz |
| DRAM Memory                  | 2Gbyte LPDDR3 RAM PoP (750MHz, 12GB/s memory bandwidth, 2x32bit bus) |
| GPU                         | Mali™-T628 MP6, OpenGL ES 3.1 / 3.0 / 2.0 / 1.1, OpenCL 1.2 Full profile |
| HDD / SSD SATA interface     | JMicron JMS578 USB 3.0 to SATA Bridge (UAS 지원, 최대 ~300MB/s 전송 속도), 7mm, 9mm, 12.5mm, 15mm 두께 HDD/SSD 설치 가능 |
| Micro-SD Slot               | UHS-1 호환, 최대 128GB/SDXC 지원 |
| USB2.0 Host                 | HighSpeed USB 표준 A타입 커넥터 x 1포트 |
| LEDs                        | Power, System-status, SATA-status |
| Gbit Ethernet LAN           | 10/100/1000Mbps 이더넷 (RJ-45, Auto-MDIX 지원) |
| Power Input                 | DC Barrel Jack Socket 5.5/2.1mm, 4.8V~5.2V 입력 (5V/4A 권장) |
| System Software             | Ubuntu 16.04 + OpenCL (Linux Kernel 4.9 LTS), Debian, DietPi, Arch-ARM, OMV 등 다양한 리눅스 배포판 지원, 전체 소스코드 Github 제공 |
| Size                        | 147 x 85 x 29 mm (무게: 226g) |

[ODROID-HC1](https://www.hardkernel.com/shop/odroid-hc1-home-cloud-one/){:target="_blank"}{:rel="noopener noreferrer"}
표로 보면


* /proc/cpuinfo 정보를 보면 아래와 같다. 

```
processor	: 7
model name	: ARMv7 Processor rev 3 (v7l)
BogoMIPS	: 120.00
Features	: half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm
CPU implementer	: 0x41
CPU architecture: 7
CPU variant	: 0x2
CPU part	: 0xc0f
CPU revision	: 3

Hardware	: Samsung Exynos (Flattened Device Tree)
Revision	: 0000
Serial		: 0000000000000000
```

다른 제품과의 벤치마크 정보는 아래와 같다.

| Benchmarks (Index Score)                         | Raspberry Pi 3 | ODROID-C1+ | ODROID-C2 | ODROID-XU4 |
|--------------------------------------------------|:--------------:|:----------:|:---------:|:----------:|
| Unixbench: Dhrystone-2 865.4                     | 1571.6         | 2768.2     | 5941.4    |            |
| Unixbench: Double-Precision Whetstone (x3)       | 1113           | 1887.3     | 3076.8    | 6186.3     |
| Nbench 2.2.3: Integer (x40)                      | 619.92         | 1173.6     | 1808.92   | 2430.52    |
| Nbench 2.2.3: Floating-Point (x100)              | 781.8          | 1245.3     | 2300.3    | 3787.3     |
| mbw100: Memory Bandwidth (MiB/s)                 | 542.912        | 616.339    | 1472.856  | 2591.461   |

|                | SD-class10 | SD-UHS1 | eMMC 5.0 |
|----------------|:----------:|:-------:|:--------:|
| Write speed (MB/s) | 8.5      | 10.8    | 39.3     |
| Read speed (MB/s)  | 18.9     | 35.9    | 140      |

스팩이 위와 같으니 읽기쓰기조금은 빨라지지 않을까? 아무래도.. SSD 이니 SD 보다는 빨리지겠지...
[ODROID-XU4 주요스팩정보](https://www.hardkernel.com/ko/shop/odroid-xu4-special-price/
){:target="_blank"}{:rel="noopener noreferrer"}


* 전원 정보 
- 5V 4A 어댑터를 사용(내경은 2.1mm, 외경은 5.5mm 중앙은 양극, 외경은 음극)
- 1~2A를 소모. USB 장치를 여러 개 연결하여 컴퓨팅 부하가 매우 높으면 최대 4A까지 소모될 수 있음.
- USB 포트에 다른 외장 HDD를 연결하려면 5V/6A PSU를 사용
- 12V/9V/15V PSU는 HC1과 함께 사용할 수 없음.

저 전력이다.. 그냥 라즈베리파이보다 빠른놈이니.. 쓸만한놈이다.(7배 빠르다고함 근데 지금 수준에서는 그냥 저전전력으로 돌릴만한 조그마한 서버로 이용하기에는 무리없어보인다.)

그럼 과정을 차차 보면될듯하다..

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

- 시스템 업데이트 시 부트 파티션이 잘 마운트되게 `/etc/fstab`에 추가:

루트(/) 파티션을 SSD/HDD로 변경해줍니다.

```
UUID=abcd-1234-ef56-7890 / ext4 errors=remount-ro,noatime 0 1
LABEL=boot /media/boot vfat defaults 0 1

```
---

## 7. 재부팅 \& 확인

1. SSD에 파일이 잘 복사됐는지 확인!

2. 재부팅!

```bash
sudo reboot
```

3. 부팅 후 루트가 SSD인지 확인!

```bash
mount | grep /dev/sda1

/dev/sda1 on / type ext4 (rw,noatime,errors=remount-ro)```

`/dev/sda1 on / type ext4` 이렇게 나오면 성공!

---

- 이제 microSD는 부트로더/커널만 담당하고,
실질적인 시스템 구동은 SSD/HDD에서 이뤄집니다!
- 속도도 빨라지고, SD카드 수명 걱정도 끝!
SSD 수명이 다할때까지 쭈~욱 사용해주도록하마... 

- SSD로 옮기면 정말 쾌적해져요. 강추👍

끝.

#Odroid #XU4 \#HC1 \#SSD부팅 \#microSD \#리눅스팁 \#갓성비NAS \#취미서버

