---
layout: post
title: "[PostgreSQL 테스트] PostgreSQL regression 사전지식"
date: 2026-01-27 00:00:00 +0900
categories: [PostgreSQL, Testing]
tags: [PostgreSQL, JUnit, QA]
---
* 목차
{:toc}

---
안녕하세요!

올해의목표가 2주에 한번은 글을 기록해서 하나하나 남겨놓자가 목표인데 쓰다보니 계속쓰게되네요 

아무튼.. 

오늘은 PostgreSQL 기반의 테스트를 진행하면서 마주친 문제가 있었어요 그걸 하면서 효율성 개선에 대한 이야기를 좀 해보려고 하는데요  

그러기에 앞서 PostgreSQL regression 테스트를 어떻게 하는지 간단히 이야기 해볼게요.

처음에는 하나로 글작성 하려고 했는데 너무 길면 지루해서 두개로 나눴어요.
 
---
## 사전지식

혹시 "어? regression 테스트가 뭐지? 이 파일들은 어디서 나오는 거지?"라고 생각한 분이 있을 거예요.

그래서 PostgreSQL의 테스트 시스템이 어떻게 작동하는지, 그리고 이 파일들이 정확히 어디서 나오는지 한번 집어보고 가려고요.

차근차근 따라가다 보면, "아, 그래서 이런 파일들이 나오는 거구나"하고 이해가 될 거예요.

---

## PostgreSQL의 자동화된 테스트 시스템

PostgreSQL은 거대한 오픈소스 데이터베이스에요. 매년 새로운 기능이 추가되고, 버그 픽스가 들어가고, 최적화가 이루어집니다.

근데 이렇게 계속 변경이 들어가다 보면 한 가지 걱정이 생기죠:

"어? 이 새로운 기능을 추가했는데, 혹시 기존 기능을 망가뜨린 건 아닐까?"

이 걱정을 덜기 위해 PostgreSQL은 **자동화된 테스트 시스템**을 갖춰두고 있어요. 이걸 **regression 테스트**라고 부릅니다.

"Regression"은 "회귀"라는 뜻인데, 즉 "기존에 잘 작동하던 기능이 다시 망가지지 않았는가?"를 확인하는 것이 목표라는 의미에요.

---

## make check: 한 줄의 명령으로 전체 테스트 실행

PostgreSQL 소스 코드를 받아서 빌드했다면, 다음과 같이 테스트를 실행할 수 있어요:

```bash
$ cd src/test/regress
$ make check
```

딱 이 두 줄이면 됩니다. 그러면 뒤에서 어떤 일들이 일어날까요?

### 1단계: 테스트 서버 시작

먼저 PostgreSQL이 **임시 서버 인스턴스**를 하나 만들어요. 실제 운영 중인 데이터베이스는 건드리지 않고, 테스트용 별도의 서버를 띄우는 거죠.

```
[테스트 시작] PostgreSQL 임시 서버 시작
Port: 5555 (테스트용 포트)
Data Directory: /tmp/pg_test_XXXXX
```

### 2단계: 테스트 SQL 스크립트 실행

이제 미리 준비해둔 SQL 테스트 스크립트들을 실행합니다. 예를 들어:

- `aggregates.sql` - 집계 함수 테스트
- `bitmapops.sql` - 비트맵 연산 테스트
- `plisql.sql` - PL/SQL 호환성 테스트
- `packages.sql` - 패키지 기능 테스트

이들이 **순차적으로** 또는 **병렬로** 실행돼요. 최신 PostgreSQL은 병렬 실행을 지원해서 시간을 많이 단축할 수 있죠.

```
[진행 중] aggregates.sql 실행 중...
[진행 중] bitmapops.sql 실행 중...
[진행 중] plisql.sql 실행 중...
```

### 3단계: 결과 비교

각 테스트가 실행되면 결과가 나와요. 예를 들어:

```
SELECT COUNT(*) FROM table;
(1 row)

 count
-------
 1000
```

이 결과를 **미리 저장해둔 기대값**과 비교합니다. 같으면 "ok", 다르면 "not ok"가 기록돼요.

### 4단계: 테스트 서버 종료

모든 테스트가 끝나면 임시 서버를 정리합니다.

```
[완료] 테스트 종료
[정리] 임시 서버 제거
```

전체 과정은 보통 **2~5분** 정도 걸려요. (테스트 개수에 따라 다름)

---

## 테스트 결과는 어디에 저장될까?

테스트가 끝나면 여러 파일들이 생성돼요. 구조는 이래요:

```
src/test/regress/
├── regression.out          ← 전체 테스트 실행 결과 (plain text)
│                             모든 테스트의 pass/fail 요약
├── regression.diffs        ← 기대값과 실제값의 diff만 모아둔 파일
│                             실패한 테스트의 상세 비교
├── results/                ← 각 테스트별 실제 출력 결과
│   ├── aggregates.out
│   ├── bitmapops.out
│   ├── plisql.out
│   ├── packages.out
│   └── ... (개별 테스트 파일들)
└── log/                    ← 테스트 실행 로그
    ├── regress.log         (테스트 프레임워크 로그)
    ├── aggregates.log
    ├── bitmapops.log
    └── ... (개별 로그)
```

각 파일의 역할을 하나씩 설명해볼게요.

---

## regression.out: 전체 테스트 결과 요약

가장 먼저 확인하는 파일이에요. 어떤 테스트가 성공했고, 어떤 테스트가 실패했는지를 **한눈에** 볼 수 있거든요.

```
# initializing database system by running initdb
# using temp instance on port 55317 with PID 14189
ok 1         - test_setup                                139 ms
not ok 2     - packages                                  100 ms
not ok 3     - plisql                                    100 ms
...
# 64 of 239 tests failed.
```

각 라인의 의미:

- `ok`: 테스트 성공 
- `not ok`: 테스트 실패 
- 숫자: 테스트 번호 (순서)
- 이름: 테스트 파일명 (aggregates, bitmapops 등)
- `ms`: 실행 시간 (밀리초)

**# parallel group** 부분은 병렬로 실행되는 테스트들을 표시해요. PostgreSQL은 테스트를 그룹으로 나눠서 동시에 여러 개를 실행할 수 있거든요.

이 파일을 보면 "아, 총 239개 테스트 중 64개가 실패했네"라는 걸 빠르게 파악할 수 있어요.

---

## regression.diffs: 실패한 테스트의 상세 정보

이제 "왜 실패했을까?"를 알아야 하죠. 그걸 보여주는 파일이 `regression.diffs`에요.

실패한 테스트만 모아서, **기대값과 실제값의 차이**를 diff 형식으로 저장합니다:

```
Test 'bitmapops' failed.
--- DIFF ---
diff -U3 /home/rockylinux/.../expected/bitmapops.out /home/rockylinux/.../results/bitmapops.out
--- /home/rockylinux/.../expected/bitmapops.out   2026-01-22 07:03:35.000000000 +0000
+++ /home/rockylinux/.../results/bitmapops.out   2026-01-27 06:37:10.482541734 +0000
@@ -100,5 +100,7 @@
  기대값
- 1000
+ 2828.97
  (1 row)
```

이 파일을 해석하면:

- `---`: 기대값 파일 (expected/bitmapops.out)
- `+++`: 실제 결과 파일 (results/bitmapops.out)
- `-` 줄: 기대했던 값
- `+` 줄: 실제로 나온 값

즉, "1000이 나올 줄 알았는데, 2828.97이 나왔네?"라는 의미에요.

---

## results/ 디렉터리: 각 테스트별 실제 출력값

각 테스트가 실행되면 그 결과가 개별 파일로 저장돼요:

```
results/
├── aggregates.out      ← aggregates 테스트의 전체 출력
├── bitmapops.out       ← bitmapops 테스트의 전체 출력
├── plisql.out
├── packages.out
└── ...
```

예를 들어 `aggregates.out` 파일은 aggregates.sql 스크립트를 실행한 결과를 **전부** 담고 있어요. 엄청 커요. 수백 줄이 될 수 있거든요.

이 파일들과 `expected/` 디렉터리에 미리 저장해둔 기대값을 비교해서 `regression.diffs`를 만드는 거랍니다.

---

## log/ 디렉터리: 테스트 실행 로그

테스트 실행 중에 발생한 모든 메시지들이 기록돼요:

```
log/
├── regress.log         ← 테스트 프레임워크 로그
│                         (서버 시작/종료, 테스트 실행 순서 등)
├── aggregates.log
├── bitmapops.log
└── ...
```

예를 들어 `regress.log`에는:

```
2026-01-27 06:37:27.092 UTC postmaster[14189] Starting PostgreSQL test server...
2026-01-27 06:37:27.092 UTC postmaster[14189] Server started on port 5555
2026-01-27 06:37:27.092 UTC postmaster[14189] WARNING:   - Start date/time   : 
2026-01-27 06:37:27.465 UTC client backend[15749] pg_regress/oidjoins CONTEXT:  PL/pgSQL function inline_code_block line 42 at RAISE
2026-01-27 06:37:27.465 UTC client backend[15749] pg_regress/oidjoins WARNING:  FK VIOLATION IN pg_proc({pronamespace}): ("(126,15)",14915)
2026-01-27 06:37:27.950 UTC checkpointer[14190] LOG:  checkpoint starting: shutdown immediate
2026-01-27 06:37:27.951 UTC checkpointer[14190] LOG:  checkpoint complete: wrote 45 buffers (0.3%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.001 s, sync=0.001 s, total=0.001 s; sync files=0, longest=0.000 s, average=0.000 s; distance=159 kB, estimate=87070 kB; lsn=0/120B16D0, redo lsn=0/120B16D0
2026-01-27 06:37:27.971 UTC postmaster[14189] LOG:  database system is shut down
```
이런 식으로 기록돼요. 뭔가 잘못되면 이 로그를 확인해서 원인을 찾을 수 있어요.

오늘은 여기까지하고.. 

다음글에서.

**다음 글 미리보기**: 

regression.diffs 파일을 Python으로 간단히 변환해서 **JUnit XML** 형식으로 만들고, Jenkins 대시보드 나 기타 툴들엣 한눈에 볼수 있다.

끝.