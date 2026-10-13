---
layout: post
title: "삼성 EVO Plus로 산 SD 카드가 1TB로 잡혔는데, 실제로 기록되는 용량은 67GB였습니다 - macOS에서 가짜 용량 판별하기"
date: 2026-10-13 11:00:00 +0900
categories: [Hardware, Testing]
tags: [SD카드, 가짜용량, f3, macOS, 저장장치]
---
* 목차
{:toc}

---

## 들어가며

집에 놀고 있던 마이크로 SD 카드를 찾았습니다. 예전에 쿠팡에서 삼성전자 EVO Plus라고 해서 26,800원에 산 카드입니다. 맥에 꽂아 보니 1TB로 잡혔습니다. 그 값에 1TB라니 아무래도 이상해서 직접 확인해 보기로 했습니다.

결론은 뭐다 싼게 비지떡.. T.T

<img src="/assets/images/2026-10-13-sd-card-order.jpg" alt="SD 카드 주문 내역" width="60%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

실제로 쓸 수 있는 용량은 67GB 정도였습니다. 1TB의 6% 남짓이고, 그 뒤쪽에 저장한 데이터는 다시 읽어 보면 전부 깨져 있었습니다.

## 가짜 용량 카드는 어떻게 속이나

가짜 용량 카드는 컨트롤러 펌웨어를 조작해서 실제보다 큰 용량으로 인식되게 만든 카드입니다. 꽂아서 쓰는 것만으로는 정상 카드와 차이를 알기 어렵습니다.

- Finder나 탐색기에는 1TB로 표시됩니다.
- 포맷도 문제없이 됩니다.
- 실제 용량보다 많은 파일을 복사해도 **오류 없이 복사가 끝납니다.**
- 그런데 나중에 파일을 열어 보면 깨져 있습니다. 카드에 따라서는 앞에 저장해 둔 파일까지 망가집니다.

그래서 용량 표시는 믿을 수 없고, 데이터를 직접 써 보고 다시 읽어 봐야 진짜인지 알 수 있습니다.

## f3 소개

[f3](https://github.com/AltraMayor/f3)는 SD 카드나 USB 메모리가 표기된 용량과 속도를 제대로 내는지 검사하는 오픈소스 도구입니다. Fight Flash Fraud(또는 Fight Fake Flash)의 약자이고 라이선스는 GPL-3.0입니다. 윈도우에서 많이 쓰는 H2testw를 맥과 리눅스에서 쓸 수 있게 만든 도구라고 생각하면 됩니다.

f3는 카드에 난수 데이터를 가득 써 놓고 다시 읽어서, 쓴 값이 그대로 나오는지 비교합니다. 가짜 카드는 실제 용량을 넘어선 부분에 쓴 데이터를 저장하지 못하기 때문에, 그 부분을 읽으면 엉뚱한 값이 나옵니다.

Homebrew로 설치하면 아래 네 프로그램 중 `f3write`와 `f3read` 두 개만 깔립니다.

| 프로그램 | 하는 일 | 데이터 | macOS(Homebrew) |
|---|---|---|---|
| `f3write` | 마운트된 볼륨에 1GB 단위 시험 파일(`1.h2w`, `2.h2w` ...)을 쓰고 쓰기 속도를 잽니다 | 보존 (빈 공간만 사용) | 포함 |
| `f3read` | `f3write`가 쓴 파일을 읽어 손상 여부와 읽기 속도를 보고합니다 | 보존 | 포함 |
| `f3probe` | 장치에 직접 필요한 지점만 써서 실제 용량을 빠르게 찾습니다 | 삭제 | 없음 (리눅스 전용) |
| `f3fix` | 실제 용량에 맞는 파티션을 다시 만듭니다 | 삭제 | 없음 (리눅스 전용) |

`f3write`와 `f3read`는 일반 파일을 쓰고 읽는 방식이라 카드에 있던 파일은 그대로 둡니다. 그 대신 빈 공간을 끝까지 채웠다가 다시 다 읽어야 해서, 용량이 큰 카드는 시간이 아주 오래 걸립니다. 빠르게 검사하는 `f3probe`는 맥용이 없어서, 4단계에서는 같은 방식으로 동작하는 파이썬 스크립트를 직접 만들어 돌렸습니다.

## 시험 환경

| 항목 | 값 |
|---|---|
| 카드 | 삼성전자 EVO Plus로 판매된 마이크로 SD (V30 표기), 맥에서 1TB로 인식 |
| 리더 | Mac Pro 내장 SD 카드 리더 (PCIe 5.0 GT/s 연결) |
| 파일 시스템 | ExFAT (구매 상태 그대로) |
| 시험 도구 | `f3` 10.0 (`f3write`·`f3read`), 직접 작성한 파이썬 스크립트 |

## 1단계: 카드 기본 정보 확인

먼저 맥이 이 카드를 뭐라고 인식하는지 봤습니다.

```bash
diskutil info /Volumes/Untitled
system_profiler SPCardReaderDataType
```

| 항목 | 값 |
|---|---|
| 장치 | `/dev/disk4s1` |
| 전체 용량 | 1,073,674,715,136 바이트 (1.07TB) |
| 사용 중 | 872MB |
| Product Name | `??asdfg` |

용량은 1TB로 멀쩡하게 나왔는데 제품명이 `??asdfg`였습니다. 원래 이 자리에는 제조사 모델명이 들어가야 하는데, 키보드를 대충 두드린 것 같은 값이 들어 있었습니다. 삼성 정품이 이럴 리는 없으니 이때부터 가짜라는 티가 확실하게 났습니다.

## 2단계: f3로 속도와 앞쪽 데이터 확인

카드에 있던 파일을 지우지 않는 `f3write`·`f3read`로 앞쪽 3GB만 먼저 써 봤습니다. 속도도 재고 앞부분이 제대로 저장되는지도 보려고 했습니다.

```bash
brew install f3
f3write --end-at=3 /Volumes/Untitled/F3TEST    # 앞쪽 3GB만 쓰기
diskutil unmount /Volumes/Untitled             # 읽기 캐시를 비우려고 다시 마운트
diskutil mount disk4s1
f3read /Volumes/Untitled/F3TEST
```

| 확인 내용 | 결과 |
|---|---|
| 쓰기 속도 | 평균 18.7MB/s, 최저 7MB/s |
| 읽기 속도 | 평균 23.0MB/s |
| 앞쪽 3GB 무결성 | 3.00GB 정상, 손상 0 |

앞쪽 3GB는 멀쩡했습니다. 하지만 가짜 카드도 실제 용량 안쪽은 정상으로 동작하니, 이것만 보고 진짜라고 할 수는 없습니다.

속도는 많이 모자랐습니다. 카드에 적힌 V30은 SD 협회가 정한 비디오 스피드 클래스로, 쓰기 속도가 30MB/s 아래로 떨어지지 않는다는 표시입니다. 그런데 이 카드는 평균도 30MB/s가 안 나왔습니다. 혹시 리더가 느린가 싶어 확인해 봤는데, 맥 내장 리더는 UHS-I 최대 속도(104MB/s)보다 여유가 있어서 리더 탓은 아니었습니다.

## 3단계: 1TB 전체 시험에 걸리는 시간 계산

`f3`로 남은 996GB를 전부 채우고 다시 읽으면 실제 용량을 정확히 알 수 있습니다. 문제는 시간인데, 위에서 잰 속도로 계산해 보니 쓰는 데 15시간, 읽는 데 12시간 정도로 하루가 넘게 걸립니다.

하루를 기다릴 수는 없어서, 1TB를 다 채우는 대신 처음부터 끝까지 일정한 간격으로 표식만 찍어 보고 확인하기로 했습니다.

## 4단계: 표식 1,001개로 실제 용량 찾기

### 원리

1. 카드 원시 장치(`/dev/rdisk4`)의 0GB부터 끝까지 1GiB마다 한 곳씩, 모두 1,001곳을 고릅니다.
2. 각 위치에 1MiB짜리 난수 데이터를 기록합니다. 위치값을 시드로 난수를 만들기 때문에 위치마다 내용이 다르고, 나중에 같은 값을 다시 만들어 비교할 수 있습니다.
3. 전부 다시 읽어서 처음 쓴 값이 그대로 있는지 봅니다. 처음으로 값이 달라지는 곳이 실제 용량의 끝입니다.

가짜 카드 중에는 실제 용량을 넘는 주소에 쓴 데이터를 앞쪽 주소에 덮어쓰는 종류도 있습니다. 이런 카드에 앞에서부터 표식을 쓰면, 나중에 쓴 뒤쪽 표식이 앞쪽 표식을 덮어 버려서 경계를 잘못 찾게 됩니다. 그래서 **뒤에서부터 앞으로** 쓰게 했습니다. 앞쪽 표식을 맨 마지막에 쓰니 덮어써질 일이 없습니다.

> **주의:** 이 스크립트를 돌리면 카드 안의 파일이 전부 지워집니다. 필요한 파일은 미리 백업해 두세요. 원시 장치에 직접 쓰기 때문에 `sudo`로 실행해야 하고, 장치 이름(`/dev/rdisk4`)을 잘못 넣으면 엉뚱한 디스크가 지워집니다. 실행 전에 `diskutil list`로 꼭 확인하세요.

### 스크립트

```python
#!/usr/bin/env python3
"""SD 카드 가짜 용량 검사 (원시 장치에 직접 쓰므로 카드 내용이 모두 지워집니다).

동작 순서
  1. 카드 전체에서 1GiB 간격으로 검사 지점을 고릅니다.
  2. 지점마다 서로 다른 1MiB 난수 데이터를 씁니다. (뒤쪽 지점부터 앞쪽으로)
  3. 모든 지점을 다시 읽어 처음 쓴 데이터가 그대로 있는지 확인합니다.
  4. 처음으로 데이터가 달라진 지점을 실제 용량의 끝으로 보고합니다.
  5. 카드를 ExFAT 'Untitled' 로 다시 포맷합니다.

사용법: sudo python3 probe.py /dev/rdisk4
"""
import os
import random
import subprocess
import sys
import time

BLOCK_SIZE = 1024 * 1024         # 지점마다 쓰는 데이터 크기 (1MiB)
STEP = 1024 * 1024 * 1024        # 검사 지점 사이 간격 (1GiB)
GB = 1e9                         # 출력용 단위 (10진 GB, 카드 표기와 같은 기준)


def make_pattern(offset):
    """지점 위치를 시드로 1MiB 난수를 만든다.

    같은 위치를 넣으면 언제나 같은 값이 나오므로,
    읽을 때 다시 만들어서 비교할 수 있다.
    """
    seed = offset * 7919 + 12345
    return random.Random(seed).randbytes(BLOCK_SIZE)


def get_device_size(raw_device):
    """diskutil info 출력에서 장치 전체 크기(바이트)를 읽는다."""
    disk = raw_device.replace("rdisk", "disk")    # /dev/rdisk4 -> /dev/disk4
    info = subprocess.run(["diskutil", "info", disk],
                          capture_output=True, text=True, check=True).stdout
    for line in info.splitlines():
        # 예: "Disk Size: 1.1 TB (1073741824000 Bytes) ..."
        if "Disk Size" in line:
            return int(line.split("(")[1].split()[0])
    sys.exit("장치 크기를 읽지 못했습니다")


def choose_points(device_size):
    """0부터 장치 끝까지 STEP 간격의 지점 목록을 만든다. 마지막 블록도 포함한다."""
    last_block = (device_size - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
    points = list(range(0, last_block, STEP))
    points.append(last_block)
    return sorted(set(points))


def write_markers(fd, points):
    """모든 지점에 패턴을 쓴다.

    뒤쪽부터 쓰는 이유: 가짜 카드 중에는 실제 용량을 넘는 주소를
    앞쪽 주소에 덮어쓰는 종류가 있다. 앞쪽 지점을 마지막에 쓰면
    실제 영역의 표식이 덮이지 않고 남는다.
    """
    for offset in reversed(points):
        os.pwrite(fd, make_pattern(offset), offset)
    os.fsync(fd)    # 캐시에 남지 않고 카드에 실제로 기록되게 한다


def describe_bad_data(data, owner_of):
    """틀린 데이터가 어떤 종류인지 한 줄로 설명한다."""
    source = owner_of.get(data[:64])
    if source is not None:
        # 다른 지점에 쓴 데이터가 여기서 읽힌다 = 주소를 돌려 쓰는 카드
        return f"holds data of {source / GB:.1f} GB"
    if data.count(0) == BLOCK_SIZE:
        return "zeros"      # 쓰기를 버리고 0만 돌려주는 카드
    return "garbage"        # 쓴 값과 무관한 값


def check_markers(fd, points):
    """모든 지점을 읽어 패턴과 비교하고, 틀린 지점 목록을 돌려준다."""
    # 패턴 앞 64바이트로 "어느 지점의 데이터인지" 찾는 표
    owner_of = {make_pattern(p)[:64]: p for p in points}

    bad_points = []     # (위치, 설명) 목록
    for offset in points:
        data = os.pread(fd, BLOCK_SIZE, offset)
        if data != make_pattern(offset):
            bad_points.append((offset, describe_bad_data(data, owner_of)))
    return bad_points


def print_report(points, bad_points, device_size):
    """검사 결과를 출력한다."""
    good_count = len(points) - len(bad_points)
    print(f"good {good_count}/{len(points)}  bad {len(bad_points)}")

    for offset, kind in bad_points[:10]:            # 처음 10개만 보여 준다
        print(f"  bad @ {offset / GB:.1f} GB: {kind}")

    if not bad_points:
        print(f"RESULT: GENUINE - all {len(points)} points across "
              f"{device_size / GB:.1f} GB read back intact")
        return

    first_bad = bad_points[0][0]
    last_good = first_bad - STEP
    print(f"RESULT: FAKE - real capacity about {first_bad / GB:.1f} GB "
          f"(last good point {last_good / GB:.1f} GB)")


def main():
    if len(sys.argv) != 2:
        sys.exit("사용법: sudo python3 probe.py /dev/rdiskN")

    raw_device = sys.argv[1]
    disk = raw_device.replace("rdisk", "disk")

    device_size = get_device_size(raw_device)
    points = choose_points(device_size)
    print(f"device {raw_device}  size {device_size} bytes "
          f"({device_size / GB:.1f} GB)  points {len(points)}")

    # 마운트된 상태로는 원시 장치에 쓸 수 없으므로 먼저 언마운트한다
    subprocess.run(["diskutil", "unmountDisk", disk], check=True)

    fd = os.open(raw_device, os.O_RDWR)
    try:
        started = time.time()
        write_markers(fd, points)
        print(f"write done {time.time() - started:.0f}s")

        bad_points = check_markers(fd, points)
    finally:
        os.close(fd)

    print_report(points, bad_points, device_size)

    # 검사로 파일 시스템이 지워졌으므로 다시 포맷한다
    print("reformatting as ExFAT 'Untitled' ...")
    subprocess.run(["diskutil", "eraseDisk", "ExFAT", "Untitled", "MBR", disk],
                   check=True)


if __name__ == "__main__":
    main()
```

값이 틀린 곳은 읽힌 내용에 따라 이렇게 표시합니다.

| 표시 | 뜻 |
|---|---|
| `holds data of N GB` | 다른 지점(N GB)에 쓴 데이터가 들어 있습니다. 주소를 돌려 쓰는 카드입니다 |
| `zeros` | 0만 읽힙니다. 쓰기를 버리는 카드입니다 |
| `garbage` | 쓴 값과 무관한 값이 읽힙니다 |

### 실행 결과

```text
$ sudo python3 probe.py /dev/rdisk4
device /dev/rdisk4  size 1073741824000 bytes (1073.7 GB)  points 1001
Unmount of all volumes on disk4 was successful
write done 49s
good 63/1001  bad 938
bad @ 67.6 GB: garbage
bad @ 68.7 GB: garbage
bad @ 69.8 GB: garbage
...
RESULT: FAKE - real capacity about 67.6 GB (last good point 66.6 GB)
```

쓰는 데 49초, 전체로는 2분도 안 걸렸습니다.

| 확인 내용 | 기대 | 실제 |
|---|---|---|
| 정상 지점 | 1,001개 전부 | 63개 |
| 손상 지점 | 0개 | 938개, 모두 `garbage` |
| 정상으로 기록되는 마지막 지점 | 1,073.7GB | 66.6GB |
| 처음 손상된 지점 | 없음 | 67.6GB |

0GB부터 62GiB(66.6GB)까지 63곳만 제대로 읽혔고, 63GiB(67.6GB)부터 끝까지는 전부 엉뚱한 값이 나왔습니다. 실제 용량은 66.6GB와 67.6GB 사이입니다. 64GB짜리 메모리 칩에 1TB로 보이게 하는 펌웨어를 올린 카드가 아닐까 싶습니다(추정).

## 결과 정리

| 항목 | 표기 | 측정 | 판정 |
|---|---|---|---|
| 용량 | 1TB | 약 67GB | 표기의 약 6% |
| 쓰기 속도 (V30) | 30MB/s 이상 유지 | 평균 18.7MB/s | 미달 |
| 제품명 | 삼성 모델명 | `??asdfg` | 비정상 |

너무 싸서 처음부터 가짜일 거라고 의심하고 시작한 시험이었습니다. 용량도 1TB로 나오고 포맷도 잘 돼서 겉보기에는 멀쩡했지만, 데이터를 직접 써 보니 67GB까지만 제대로 저장됐습니다.

싸게 산 대용량 카드가 있다면 중요한 파일을 넣기 전에 꼭 한 번 확인해 보세요.
