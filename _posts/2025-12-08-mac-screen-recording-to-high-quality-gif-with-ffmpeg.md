---
layout: post
title: "[ffmpeg] 화면 녹화부터 고화질 GIF 변환까지"
date: 2025-12-08 10:19:00 +0900
categories: ffmpeg
tags:
- ffmpeg
- gif
- macos
- cli
---

* 목차
{:toc}

---

## [Mac 꿀팁] 화면 녹화부터 고화질 GIF 변환까지 

저는 Mac 을 이용 하고있어 이번에 글을쓰다가 Gif 로 변환할 일이 있어서 정리를 좀 하려고 작성을 하게되었어요.
Mac 기본 화면녹화를 하고 이걸 Gif 로 변환하는 걸 해보았는데요 그부분을 정리해봅니다. 

**화면 녹화한 MOV 파일을 고화질 GIF로 변환하는 방법**입니다. 

블로그 포스팅이나 GitHub README, 혹은 팀 메신저(Slack/Discord)에 작업물을 공유할 때 동영상 파일은 무겁고 재생 버튼을 눌러야 해서 불편할 때가 있죠? 그럴 때 **자동 재생되는 가벼운 GIF**가 정답입니다. 별도의 유료 앱 없이 터미널만으로 전문가처럼 변환하는 방법을 알려드릴게요.

-----

### 1단계: Mac 기본 기능으로 화면 녹화하기 (MOV 생성)

Mac에는 이미 강력한 화면 녹화 도구가 내장되어 있습니다. 무겁게 별도 프로그램을 설치할 필요가 없어요.

**가장 빠른 방법: 단축키 `Command` + `Shift` + `5`**

1.  키보드에서 **Command + Shift + 5**를 동시에 누르세요.

2.  화면 하단에 컨트롤 바가 나타납니다.

3.  **녹화 영역 선택**:

      * 네 번째 아이콘: **전체 화면 녹화**
      * 다섯 번째 아이콘: **선택한 영역만 녹화** (추천\! 필요한 부분만 깔끔하게 따세요)

4.  **옵션(Options) 설정**:

      * **마이크**: 나레이션이 필요 없다면 '없음'으로 설정하세요.
      * **저장 위치**: 파일 찾기 쉽게 '데스크탑(바탕화면)'으로 두는 것이 좋습니다.
      * **마우스 클릭 표시**: 튜토리얼을 만든다면 체크하는 것이 좋습니다.

5.  **기록(Record)** 버튼을 누르거나 선택 영역을 클릭하면 녹화가 시작됩니다.

6.  **녹화 종료**: 녹화중에는 메뉴가 안나옵니다. 당황하지 마시고(전 당황했어요.. 어떻게 정지하지?) 다시 `Command` + `Shift` + `5` **눌러  메뉴 막대 상단의 정지(⏹️) 버튼을 누르거나 `Command` + `Control` + `Esc`를 누르세요.

> **Tip:** 더 세밀한 설정이 필요하다면 `QuickTime Player` 앱을 실행하여 `파일 > 새로운 화면 기록`을 이용할 수도 있습니다.

-----

### 2단계: FFmpeg 설치하기 (변환 도구 준비)

이제 MOV 파일을 마법처럼 GIF로 바꿔줄 **FFmpeg** 을 설치할 차례입니다. 개발자들의 필수품인 `Homebrew`를 이용하면 아주 간단합니다.

**터미널(Terminal) 앱을 열고 아래 명령어를 입력하세요.**

1.  **Homebrew 설치** (이미 있다면 패스\!)

<!-- end list -->

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2.  **FFmpeg 설치**

<!-- end list -->

```bash
brew install ffmpeg
```

3.  **설치 확인**

<!-- end list -->

```bash
ffmpeg -version
```

위 명령어를 입력했을 때 버전 정보가 쫘르륵 뜬다면 준비 완료입니다\!

제가 현재 사용하는 버전은 아래와 같아요 

```
fmpeg version 8.0.1 Copyright (c) 2000-2025 the FFmpeg developers
built with Apple clang version 17.0.0 (clang-1700.4.4.1)
configuration: --prefix=/opt/homebrew/Cellar/ffmpeg/8.0.1 --enable-shared --enable-pthreads --enable-version3 --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libaribb24 --enable-libbluray --enable-libdav1d --enable-libharfbuzz --enable-libjxl --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librist --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvmaf --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox --enable-audiotoolbox --enable-neon
libavutil      60.  8.100 / 60.  8.100
libavcodec     62. 11.100 / 62. 11.100
libavformat    62.  3.100 / 62.  3.100
libavdevice    62.  1.100 / 62.  1.100
libavfilter    11.  4.100 / 11.  4.100
libswscale      9.  1.100 /  9.  1.100
libswresample   6.  1.100 /  6.  1.100
```
-----

### 3단계: MOV를 고품질 GIF로 변환하기 (핵심\!)

이제 GIF 로 변환하면됩니다. 
저장된 파일을 GIF 로 변환 간단하게 아래와 같은 명령어를 입력하면됩니다.

```
ffmpeg -i input.mov output.gif 
```
하지만 용량이 어마 어마 하게 커질거에요 저같은경우 
2MB 짜리 mov 파일이 gif 로 변환하니 17MB 로 나오는 마술이 일어놨죠..

그래서 단순 변환말고 **화질은 지키면서 용량은 줄이는 '최적화 명령어'** 를 알려드릴게요

#### 💡 추천 명령어 (복사해서 쓰세요\!)

```bash
ffmpeg -i input.mov -ss 10 -t 10 -vf "fps=10,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
```

  * `input.mov`: 원본 동영상 파일명
  * `output.gif`: 저장될 GIF 파일명

참고로 2MB 짜리를 398kb 로 변환된 Sample 입니다.

<table>
  <tr>
    <td><img src="/assets/images/20251208_gif_sample.gif" alt="gif sample" width="800" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></td>
  </tr>
</table>



#### 명령어 상세 분석 (알아두면 좋아요)

| 옵션 | 설명 | 비고 |
| :--- | :--- | :--- |
| **-ss 10** | **시작 시간** | 영상의 10초 지점부터 시작합니다. |
| **-t 10** | **길이(Duration)** | 10초 분량만 변환합니다. |
| **fps=10** | **프레임 속도** | 1초당 10장. 숫자가 높으면 부드럽지만 용량이 커집니다. |
| **scale=800:-1** | **크기 조정** | 너비를 800px로 고정, 높이는 비율에 맞춰 자동 조절합니다. |
| **palettegen/use** | **팔레트 생성** | **(중요)** GIF 전용 색상표를 새로 만들어 고화질을 보장합니다. |
| **-loop 0** | **반복 설정** | 0으로 설정하면 무한 반복됩니다. |

-----
상황에 따라 아래 명령어를 골라서 사용하세요. (`input.mov` 부분만 본인 파일명으로 바꾸면 됩니다\!)

**1. 전체 영상을 통째로 GIF로 변환할 때**

```bash
ffmpeg -i input.mov -vf "fps=10,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
```

**2. 특정 구간만 자르기 (예: 5초부터 10초간)**

```bash
ffmpeg -i input.mov -ss 5 -t 10 -vf "fps=10,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
```

**3. 용량을 확 줄여야 할 때 (모바일/웹 업로드용)**

  * 프레임(fps)을 5로 낮추고, 너비를 480px로 줄입니다.

<!-- end list -->

```bash
ffmpeg -i input.mov -ss 10 -t 10 -vf "fps=5,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 small_output.gif
```

**4. 고퀄리티가 필요할 때 (프레젠테이션용)**

  * 프레임을 15\~20으로 높이고, 너비를 1200px로 늘립니다.

<!-- end list -->

```bash
ffmpeg -i input.mov -ss 10 -t 10 -vf "fps=15,scale=1200:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 hq_output.gif
```

-----

이제 여러분도 깔끔하고 전문적인 GIF를 손쉽게 만들 수 있습니다. 

끝. 
