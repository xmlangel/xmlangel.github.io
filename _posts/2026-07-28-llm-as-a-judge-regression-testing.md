---
layout: post
title: "비결정론적 LLM 답변을 회귀 테스트하는 방법 - LLM-as-a-Judge 실무 적용기"
date: 2026-07-28 00:00:00 +0900
categories: [AI, Testing]
tags: [LLM, LLM-as-a-Judge, QA, BDD, GraphRAG, Evaluation]
---
* 목차
{:toc}

---

## 들어가며

안녕하세요. 간만에 글을 올려봅니다.

이번에는 개발이나 기능 구현 이야기 대신, QA 엔지니어 관점의 검증(Evaluation) 이야기를 해보려고 합니다.

요즘 너도나도 AI 모델을 연동해 서비스를 빠르게 '만드는' 데 몰두하고 있습니다. 하지만 RAG나 파이프라인을 붙여 기능 형태를 갖추는 것과, 그 AI가 매 순간 내놓는 답변을 "과연 믿고 실제 서비스로 내보내도 되는가?"는 전혀 다른 차원의 문제입니다. 코드로 짜인 로직과 달리 LLM은 만들어 두었다고 해서 항상 올바른 답을 내놓지 않고, 환각이나 미세한 오답을 낼 위험이 늘 상존하기 때문입니다. 그래서 서비스를 구축하는 것보다 그 답변을 검증하고 보장하는 과정이 훨씬 가혹한 관문이 됩니다.

현재 저희는 규정, 법률, 판례, 기술지원 문서, 뉴스 데이터 등 다양한 비정형 데이터를 지식 그래프(Knowledge Graph)로 구조화하여 답변을 생성하는 GraphRAG 기반 서비스의 품질을 QA하고 있습니다. 매번 사람이 눈으로 답변을 검수하는 현실적인 한계를 극복하고자, "LLM-as-a-Judge(LLM을 활용한 LLM 자동 평가)" 시스템을 실무에 도입했습니다.

AI 기반 질의응답 서비스를 테스트하다 보면 결국 하나의 본질적인 질문과 마주치게 됩니다.

> "AI가 올바른 근거를 가지고 답했는가?"

특히 규정, 법률, 기술지원 문서, 뉴스/판례 등 복잡한 비정형 데이터 도메인에서 이 질문이 갖는 무게는 상당합니다. 문서 간의 위계가 명확할 뿐만 아니라, 본문 조항 사이에 예외·면책 조항이나 부칙, 특정 시스템 버전 노트, 시점별 기사 맥락 등이 복잡하게 얽혀 있기 때문입니다.

예를 들어 법률/규정 도메인에서 "3급 기관사 면허 취득에 필요한 승무 경력"을 질의했을 때를 보겠습니다. LLM이 본문 조항(원칙적인 승무 경력 2년 필요)만 그럴듯하게 인용하고, 부칙에 명시된 "특정 자격증 소지자나 개정 전 입사자에 대한 경과 조치(1년 단축 규정)"를 빠뜨렸다고 가정해 봅시다. 이 답변은 핵심 키워드("승무 경력", "3급 기관사", "면허")가 모두 겹치기 때문에 전통적인 키워드 매칭이나 문자열 유사도(Cosine Similarity) 측정 방식으로는 90% 이상의 높은 점수가 나옵니다. 하지만 실질적으로는 사용자에게 잘못된 요건을 안내하는 '치명적인 누락 오답'입니다.

기술지원(Tech Support) 문서에서도 마찬가지입니다. 장비 오류 조치 가이드를 물었을 때 일반 절차만 나열하고 "단, v2.4 이상 업데이트 환경에서는 B 절차를 우선 적용한다"는 하단 부록 노트를 누락하면 가용성 장애로 이어질 수 있습니다. 뉴스나 판례 분석 역시 최신 판결이나 최근 경과 기사를 반영하지 않고 과거 시점의 내용만 그럴듯하게 인용하는 허점이 자주 발생했습니다.

이처럼 단순 문자열 겹침이나 유사도 검사로는 도메인 맥락상의 치명적인 허점을 절대 구분해낼 수 없었습니다.

더 큰 문제는 검증 대상인 답변 자체가 비결정론적(Non-deterministic)이라는 점이었습니다. 같은 질문을 두 번 던져도 문장 순서나 인용하는 조항 수가 달라졌고, 요약의 길이도 매번 변했습니다. 모델을 바꾸거나 리트리버(Retriever) 설정에 손을 댈 때마다 답변의 결이 완전히 달라졌죠. 결국 기존 API 테스트에서 쓰던 방식, 즉 '응답 텍스트와 기댓값(Expected Answer)을 1:1로 비교하는 검증'은 완전히 무용지물이었습니다.

```python
# 이런 코드를 쓸 수 없는 대상을 어떻게 회귀 테스트에 넣을까요
assert response.json()["answer"] == expected
```

결국 사람이 원문 조문과 답변 내용을 하나하나 대조하며 전수 검사를 해야 했습니다. 답변 단 하나를 확인하는 데 평균 15분이 소요됐고, 더 큰 문제는 검수자에 따라 평가 기준이 들쑥날쑥했다는 점입니다. 어떤 검수자는 '조항 번호 인용 누락'을 사유로 FAIL을 줬고, 어떤 검수자는 '핵심 내용이 맞았으니 PASS'로 처리했습니다. 동일한 답변이 검수자에 따라 결과가 바뀌다 보니, 이 평가 기록을 회귀 테스트(Regression Test)의 신뢰할 수 있는 기준선으로 삼는 것조차 불가능했습니다.

여기에 결정적인 현실적 제약이 더해졌습니다. QA 인력은 한정되어 있는데, 검증해야 할 프로젝트와 도메인은 계속해서 늘어났습니다. 도메인마다 별도의 평가셋을 가져야 했고, 규정이 개정될 때마다 정답지(Ground Truth)를 업데이트한 뒤 이전 질의에 대해 일일이 재검증을 수행해야 했습니다. 검증 부하가 단순히 더하기(+)가 아니라 곱하기(*)로 폭발하는 구조였습니다.

<img src="/assets/images/20260728_01_scale_problem.svg" alt="검증할 건수는 곱셈으로 늘어납니다" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

프로젝트 수 × 도메인 × 평가셋 크기 × 개정 이력. 각 요소가 조금만 늘어나도 전체 검증 건수는 기하급수적으로 불어납니다. 반면 투입 가능한 QA 인력은 늘 고정된 수평선에 가깝습니다. 이 두 선이 만나는 순간, 검증 작업은 전체 개발 속도를 막아서는 가장 큰 병목(Bottleneck)이 되어버립니다.

이런 상황에서 우리에게 남은 선택지는 두 가지였습니다. **검증 범위를 줄이거나, 검증을 자동화하거나.**

규정/법률 QA에서 '검증 범위를 줄이는 것'은 결코 답이 될 수 없었습니다. 오답 한 건이 단순한 품질 버그를 넘어 서비스 전체의 신뢰도 추락으로 이어지기 때문입니다. 결국 답은 자동화뿐이었습니다. 그것도 단순 스크립트 실행이 아니라, **규정의 도메인 맥락(Context)을 이해하고 채점할 수 있는 자동 검증**이 절실했습니다.

하지만 기존의 전통적인 소프트웨어 테스트처럼 '항상 고정된 정답'이 나오는 시스템이 아니었기에, 비결정론적인 LLM 답변을 도대체 무엇을 기준으로 어떻게 검증해야 할지 막막했습니다. 그렇게 우리는 정답을 찾기 위해 관련 학술 연구와 논문들을 탐색하기 시작했습니다.

## 그래서 논문부터 찾아봤습니다

LLM에게 채점을 맡기는 방식은 이미 연구가 꽤 쌓여 있었습니다. 하지만 제가 확인하고 싶었던 것은 단 하나였습니다.

**"과연 믿을 만한가?"**

채점 프로세스를 자동화해서 숫자나 통계를 잔뜩 뽑아내는 건 어렵지 않았습니다. 정말 중요한 것은 **그 숫자를 근거로 서비스 배포 여부(Go/No-Go)를 판단할 수 있느냐**였습니다. 

그래서 논문을 읽기 시작했습니다. 새로운 기법을 배우는 것보다, LLM 평가 방식이 가진 **한계와 맹점을 미리 파악하는 것**이 더 시급했기 때문입니다.

### MT-Bench: LLM Judge를 어디까지 믿을 수 있나

처음 접한 논문은 UC Berkeley 등이 NeurIPS 2023에 발표한 [`Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena`](https://arxiv.org/abs/2306.05685)(arXiv:2306.05685v4)였습니다. LLM이 다른 LLM의 답변을 채점할 때 인간 평가자의 판정과 얼마나 일치하는지를 대규모로 검증한 대표적인 연구입니다. 저희는 규정과 법률 문서를 근거로 GraphRAG 답변을 생성하고 있었고, 단순 문자열 비교나 키워드 매칭으로는 품질을 측정할 수 없었기에 "LLM에게 채점을 맡겨도 되는가?"에 대한 근본적인 답이 필요했습니다.

저자들은 MT-Bench의 80개 질문에 대해 6개 모델의 답변을 생성한 뒤, 58명의 전문가 라벨러로부터 약 3,000건의 평가 데이터를 모았습니다. Chatbot Arena에서도 실제 대화 데이터 30,000건 중 3,000건을 추출해 대조했습니다. 전문가 인적 평가와 견줄 만한 유의미한 표본 크기였습니다.

논문에서 가장 눈에 띈 문장은 이 대목이었습니다.

> "strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over **80% agreement, the same level of agreement between humans**."

동점 투표를 제외하면 **GPT-4와 인간 평가자 간의 일치도는 85%**로, **인간 평가자 상호 간의 일치도(81%)**와 대등한 수준이었습니다. GPT-4가 사람보다 뛰어나다기보다는, 사람끼리도 주관이 갈리는 영역에서 '사람 수준의 일관성'은 보여준 셈입니다. 특히 판정이 갈렸을 때 GPT-4의 판정 근거를 재제시하자, 인간 평가자의 75%가 관점이 다르더라도 타당성을 인정했고 34%는 자신의 평가 결과를 바꾸기까지 했습니다. 이 대목을 읽고 LLM 채점 방식을 QA 파이프라인에 도입해볼 만하다고 확신했습니다.

이어서 연구진이 밝혀낸 Judge의 취약점과 오류 양상을 짚어보았습니다. 아래 그래프처럼 비교 대상인 두 모델 간 성능 차이가 클 때는 일치도가 100% 가까이 상승하지만, 성능이 비슷할수록 일치도는 70% 수준으로 떨어집니다. 즉, 성능이 비등비등한 두 답변을 미세하게 가려내는 일은 LLM Judge에게도 까다롭다는 뜻입니다. 이를 저희 서비스에 대입해보면, 치명적인 회귀(Regression)나 명백한 오답은 잘 잡아내겠지만 미세한 품질 변화는 놓칠 위험이 있음을 인지했습니다.

<img src="/assets/images/20260728_07_mtbench_agreement.png" alt="두 모델의 승률 차이가 클수록 GPT-4 와 사람의 일치도가 올라간다" width="60%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

*출처: MT-Bench 논문(arXiv:2306.05685) Figure 5*

논문의 §3.3에는 Judge가 범하기 쉬운 편향(Bias)들이 잘 정리되어 있습니다. 
첫째, **위치 편향(Position Bias)**은 두 답변 중 먼저 제시된 답변을 선호하는 현상입니다. 답변 순서를 바꿨을 때 판정을 일정하게 유지하는 비율이 Claude-v1은 23.8%, GPT-3.5는 46.2%, GPT-4는 65.0%에 불과했습니다. 저희는 단일 답변을 절대 기준표로 채점하는 방식이라 직접 노출되진 않지만, 프롬프트 서식이나 순서만 바뀌어도 점수가 흔들릴 수 있다는 주의 신호였습니다.

<img src="/assets/images/20260728_08_mtbench_position_bias.png" alt="LLM Judge 별 위치 편향 측정 결과" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

*출처: MT-Bench 논문(arXiv:2306.05685) Table 2*

<img src="/assets/images/20260728_03_bias_and_mitigation.svg" alt="MT-Bench 가 짚은 Judge 의 맹점" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

둘째, **장황함 편향(Verbosity Bias)**은 저희 도메인과 더 직접적으로 연결되어 있었습니다. 연구진은 번호 목록이 포함된 답변 23개를 골라, GPT-4에게 "새 정보 추가 없이 표현만 바꿔 앞에 재나열하라"고 지시했습니다. 내용은 동일하지만 길이만 2배로 불어난 답변에 대한 Judge의 평가 결과는 충격적이었습니다.

| Judge | 길어진 답변을 더 낫다고 판정한 비율 |
|---|---|
| Claude-v1 | 91.3% |
| GPT-3.5 | 91.3% |
| GPT-4 | 8.7% |

GPT-4를 제외한 모델들은 알맹이 없이 길기만 한 답변에 완전히 속아 넘어갔습니다. 규정 QA에서도 관련 조항을 무의미하게 길게 늘어놓은 답변이 더 우수해 보일 위험이 크므로, 채점 프롬프트 수립 시 매우 경계해야 할 대목이었습니다.

셋째, **자기 강화 편향(Self-Enhancement Bias)**도 확인했습니다. GPT-4는 자신이 생성한 답변에 대해 승률을 10% 높게 주었고, Claude-v1은 25%나 높게 평가했습니다. 정답을 생성한 모델과 채점하는 모델을 동일하게 가져가면 평가 오염이 발생한다는 사실을 분명히 깨달았습니다. (이 문제는 향후 Preference Leakage 논문을 참고해 시스템 구조를 개선하는 계기가 됩니다.)

마지막으로 가장 실무적인 힌트를 얻은 곳은 **수학·추론 채점 실험**이었습니다. LLM은 본인이 직접 풀 수 있는 문제조차 채점 과정에서는 헛갈려 하곤 합니다. 10개 추론 문제에 대해 오채점 건수를 비교한 결과는 다음과 같았습니다.

| 프롬프트 구성 | 오채점 횟수 (총 20회 중) |
|---|---|
| 기본 프롬프트 | 14회 |
| Chain-of-Thought (CoT) 적용 | 6회 |
| **참조 답안 제공 (Reference-Guided)** | **3회** |

기본 프롬프트의 오채점률(70%)이 참조 답안(Reference)을 함께 제공하자 15%로 급감했습니다. CoT만 적용해도 오채점이 줄어들긴 했지만, Judge가 답변의 오류를 그대로 따라가는 현상이 관찰되었습니다. 

이 결과는 저희 도메인에 완벽히 들어맞았습니다. 규정 및 법률 QA는 근거가 되는 원문 조항이 명확하고, GraphRAG는 검색 단계에서 이미 해당 조항들을 끌어옵니다. 따라서 평가 시 답변만 달랑 넘기지 않고 **원문 조항(Ground Truth)을 기준 참조 답안으로 함께 프롬프트에 주입하는 Reference-Guided 채점 방식**을 핵심 설계로 채택했습니다.

가져오지 않은 대응 기법도 있습니다. 순서를 바꿔 두 번 채점하는 위치 편향 방지법은 저희가 단일 답변 채점을 수행하므로 대상이 아니었고, Few-shot 예시는 일관성을 일부 높여주지만 프롬프트가 길어져 API 비용이 4배로 뛰기 때문에 대규모 반복 QA에는 부적합하다고 판단했습니다.

### CheckEval: 모호한 점수 척도의 흔들림을 잡는 체크리스트 방식

MT-Bench가 "LLM 채점 방식을 써도 된다"는 당위성을 제공했다면, [`CheckEval`](https://arxiv.org/abs/2403.18771)(arXiv:2403.18771v3) 논문은 "어떻게 채점기를 설계해야 하는가"를 근본적으로 되돌아보게 만들었습니다. 당시 저희는 1~4점 척도로 채점 후 3점 이상을 PASS로 다루고 있었는데, 하필 그 3점과 4점의 경계선이 가장 취약한 지점임을 이 논문을 통해 알게 되었습니다.

저자들은 기존의 주관적 평가 기준과 **Likert 척도(점수제)**의 조합이 심각한 일관성 결여를 유발한다고 지적합니다. 1~5점 사이의 수치를 부여하게 하면, 모델이 미세하게 우수한 텍스트를 안정적으로 구분하지 못할 뿐만 아니라 평가자 모델 종류에 따라 점수 변동 폭이 극심해진다는 것입니다. 연구진은 이를 검증하기 위해 평가자 모델 간 일치도를 나타내는 **IEA(Inter-Evaluator Agreement)** 지표를 제시합니다.

> "While correlation with human judgments is a main metric in LLM-as-a-Judge, **high correlation alone does not guarantee reliability.**"

인간 평가 점수와의 상관관계가 높게 나오더라도, 채점 모델이 바뀔 때마다 점수대가 흔들린다면 실무 운영 지표로 사용할 수 없습니다. 규정 QA 시스템에서 동일한 답변이 어제는 3점(PASS), 오늘은 4점 혹은 2점(FAIL)으로 흔들린다면 평가의 신뢰성은 무너집니다.

12개 평가 모델을 대상으로 한 Table 2의 결과는 매우 선명했습니다. (Krippendorff α 기준)

| 모델군 | G-Eval (α) | SEEval (α) | CheckEval (α) |
|---|---|---|---|
| 전체 모델 | 0.09 | 0.08 | **0.48** |
| 대형 모델 | 0.05 | 0.16 | **0.67** |
| GPT 계열 | 0.08 | 0.13 | **0.56** |
| 상위 3개 모델 | 0.09 | 0.09 | **0.65** |

전통적인 점수 부여 방식인 G-Eval의 IEA는 0.05~0.09 수준에 불과해 모델 간 합의가 거의 이뤄지지 않았습니다. 반면 체크리스트 방식을 도입한 CheckEval은 0.48~0.67의 높은 일치도를 보여주었습니다. 특히 대형 모델군의 0.67은 인간 검수자 간의 일치도(κ ≈ 0.7)에 육박하는 수치였습니다. 핵심은 점수 산출 방식에 있었습니다. **"몇 점인가?"를 묻는 점수제보다 "이 세부 요소를 충족했는가?"를 묻는 이진 체크리스트 방식이 평가 흔들림을 획기적으로 줄여준다**는 인사이트를 얻었습니다.

<img src="/assets/images/20260728_04_likert_vs_checklist.svg" alt="Likert 척도와 체크리스트 방식 비교" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

논문의 원인 진단도 저희가 겪던 상황과 정확히 일치했습니다. 저자들은 기존 Likert 방식의 한계로 **'하나의 평가 차원에 여러 세부 기준이 혼재되어 있다는 점'**과 **'인접한 점수 간의 구분이 모델별로 보정되지 않는다는 점'**을 꼽았습니다. 3점과 4점의 차이를 아무리 프롬프트로 장황하게 설명해 둔 들, 모델마다 그 모호한 경계를 서로 다르게 해석하기 때문입니다. 하필 저희 시스템이 바로 그 3점과 4점 사이를 PASS/FAIL의 절대적 분기점으로 삼고 있었습니다.

연구진은 체크리스트 방식을 적용할 때 인간 평가와의 상관관계도 크게 향상됨을 입증했습니다. Llama3.1-8B 모델로 Topical-Chat을 평가할 때 G-Eval의 상관계수(ρ)는 0.11에 불과했지만, CheckEval은 0.46으로 대폭 상승했습니다. 저자들의 주안점은 상관관계를 높이는 것 자체보다 '체크리스트 기반의 일관된 신뢰성 확보'에 있었고, 높은 상관관계는 그에 따른 자연스러운 부산물이었던 셈입니다.

또한 **비용 효율성** 측면에서도 매우 중요한 힌트를 얻었습니다. 실험 1회당 비용이 GPT-4 Turbo는 약 $66, GPT-4o는 $22인 반면, **gpt-4o-mini는 $1.30**에 불과했습니다. 무려 50배의 비용 차이가 발생함에도 불구하고, 체크리스트 방식을 채택하면 경량 모델에서도 충분한 판정 일관성이 유지되었습니다. 저희가 최종 채점 모델로 상대적으로 가벼운 `gpt-4o-mini`를 고른 강력한 근거가 여기에 있습니다. 매번 수백 건 이상의 답변을 반복 채점해야 하는 실무 QA 환경에서는, 가장 비싼 모델 하나에 의존하기보다 '자주 굴릴 수 있는 경제적이고 안정적인 구성'이 훨씬 현실적이기 때문입니다.

결과적으로 이 논문을 통해 저희는 **'채점 모델 선택의 근거'**와 **'Likert 척도의 구조적 한계'**를 똑똑히 인지하게 되었습니다. 비록 이진 체크리스트 판정과 IEA 측정 지표를 당장 모든 시스템에 완성형으로 반영하진 못했지만, 향후 골든셋(Golden Set)을 구축할 때 가장 우선적으로 해결해야 할 핵심 과제로 남겨두었습니다.

### 서베이 논문으로 전체 지형 조망하기 

개별 연구 논문들을 읽다 보니, LLM-as-a-Judge 분야의 전체적인 지형(Taxonomy)을 조망해보고 싶어졌습니다. 그때 큰 도움을 받은 곳이 [llm-as-a-judge.github.io](https://llm-as-a-judge.github.io/) (Arizona State University의 Dawei Li 연구 그룹)와 이들이 관리하는 [Awesome-LLM-as-a-judge](https://github.com/llm-as-a-judge/Awesome-LLM-as-a-judge) 저장소였습니다.

이 지형도의 중심이 되는 논문은 EMNLP 2025에 발표된 [`From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge`](https://arxiv.org/abs/2411.16594)(arXiv:2411.16594)입니다. 저자들은 초록에서 기존의 단순 매칭 방식이나 소형 모델 기반 평가가 '개방형 및 동적 시나리오(open-ended and dynamic scenarios)'를 커버하기에 턱없이 부족하다고 지목합니다. 저희가 현장에서 겪던 난제가 학술적인 문장으로 정교하게 정의된 순간이었습니다. 규정 QA 답변은 정답 문장이 하나로 픽스되지 않으며, 동일한 원문 조항을 근거로 삼더라도 서술 방식과 구성은 무궁무진하기 때문입니다.

특히 이 논문에서 가장 실용적으로 활용한 것은 **LLM 채점 체계를 분석하는 3가지 프레임워크**였습니다.

> "we introduce a systematic taxonomy to explore LLM-as-a-judge along three dimensions: **what to judge, how to judge, and how to benchmark**."

이 세 가지 축에 저희가 구축한 시스템을 직접 대입해 보았습니다.
- **What to judge (무엇을 평가할 것인가):** 답변의 내용적 사실성과 원문 조항 근거의 적합성
- **How to judge (어떻게 평가할 것인가):** Reference-Guided 기반의 단일 답변 채점 및 1~4점 척도
- **How to benchmark (평가기 자체를 어떻게 검증할 것인가):** **(비어 있음)**

세 번째 축인 'How to benchmark'를 대입하는 순간 아차 싶었습니다. 채점기(Judge) 자체를 검증하는 체계가 비어 있다면, "채점기 스스로가 맞게 채점하고 있는지"를 입증할 길이 없기 때문입니다. 평가기의 신뢰성을 검증하지 못한다면 자동화된 품질 측정의 당위성도 오래 버틸 수 없습니다. 이 서베이 논문을 통해 저희 시스템에 비어 있던 치명적인 헛점을 발견한 것이 가장 큰 수확이었습니다.

동일 연구 그룹이 발표한 후속 논문들도 함께 살폈습니다.

- [`Preference Leakage: A Contamination Problem in LLM-as-a-judge`](https://arxiv.org/abs/2502.01534) (ICLR 2026): 정답 생성 모델과 평가 모델 간의 연관성으로 인해 발생하는 '선호 오염(Leakage)'을 다룹니다.
- [`Who's Your Judge? On the Detectability of LLM-Generated Judgments`](https://arxiv.org/abs/2509.25154): 채점기가 작성한 판정문 자체의 LLM 생성 여부와 품질을 탐지하는 연구입니다.
- [`ToolPRMBench`](https://arxiv.org/abs/2601.12294) (ACL 2026): 최종 답변뿐만 아니라 단계별(Step-level) 도구 사용 과정을 채점하는 기법입니다.

이 중 저희가 즉시 아키텍처에 반영한 것은 **Preference Leakage(선호 오염)**에 관한 연구였습니다. 당시 저희 파이프라인은 정답(Ground Truth) 추출과 답변 채점을 동일한 모델이 수행하고 있었습니다. MT-Bench에서 접했던 '자기 강화 편향'을 단순 가능성 정도로만 넘겼었는데, 이 논문을 통해 생성 모델과 평가 모델의 연관성이 채점 결과를 어떻게 오염시키는지 명확히 확인한 후 **생성 모델과 채점 모델을 서로 다른 계열로 완전히 분리**하는 구조 개편을 감행했습니다. 

나머지 두 연구는 메모해두고 장기 과제로 돌렸습니다. 당장은 판정문의 텍스트 탐지나 단계별 공정 채점보다는, 답변 단위의 사실성 확보와 합불 안정성을 먼저 잡는 일이 급선무였기 때문입니다.

---

## 제품 테스트 체계에 적용하기: BDD 파이프라인

방법론을 정한 뒤에는 이를 실제 제품 QA 체계에 올리는 작업으로 넘어갔습니다. 단순히 `pytest` 스크립트로 짜서 돌려도 됐지만, 실무에서는 몇 가지 현실적인 걸림돌이 있었습니다.

첫째, **평가 기준을 잡는 사람과 테스트 코드를 짜는 사람이 달랐습니다.** 어떤 조항이 정답의 핵심 근거인지, 어떤 수치 누락이 치명적 오류인지는 도메인 담당자가 가장 잘 압니다. QA 엔지니어가 임의로 기준을 판단해서 코드로 작성할 수는 없는 노릇이었습니다.

둘째, **실행 요청이 매번 제각각이었습니다.** "0409 시트 2~5행만 평가해서 TCC(TestCaseCraft)에 올려줘", "0515 시트 전체 다시 돌려줘", "채팅 호출 없이 기존 답변만 채점해 줘" 같은 식이었죠. 이걸 매번 QA 엔지니어가 코드를 고쳐가며 대응하면, 병목이 '검증'에서 '테스트 코드 개발'로 옮겨갈 뿐이었습니다.

결국 **테스트 케이스 자체가 실행 가능한 명세서**가 되어야 했습니다. 그래서 BDD 프레임워크인 `behave`를 도입하고 `# language: ko` 설정을 붙였습니다. 도메인 담당자도 읽고 쓸 수 있는 한글 `조건 / 만약 / 그러면` 시나리오 구조로 평가 파이프라인(`tests/features` 디렉터리)을 구성한 이유입니다.

```gherkin
# language: ko
기능: BERT/LLM Judge 모델 실행
  bert_llm_judge-file.py 스크립트를 다양한 파라미터로 실행하고 결과를 확인한다.

  @evaluate
  시나리오: EVALUATE 모드로 특정 시트를 대상으로 실행
    조건 "tests/utils/bert_llm_judge-file.py" 스크립트가 존재함
    만약 "EVALUATE" 모드와 "Sheet2" 시트 파라미터로 스크립트를 실행하면
    그러면 스크립트가 성공적으로 종료되어야 함

  @evaluate_rows
  시나리오: 특정 행 범위 평가 및 TCC 업로드
    만약 "0409-25" 시트의 2행부터 5행까지 평가를 실행하면
    그러면 평가 결과가 TestCaseCraft에 업로드되어야 함
```

이 시나리오 파일은 그냥 읽기용 문서로 끝나는 게 아니라, 아래처럼 터미널에서 한 줄로 바로 돌리는 실제 테스트 코드입니다.

```bash
uv run behavex -t @evaluate_rows tests/features/bert_llm_judge.feature
```

`@evaluate`(전체 배치), `@evaluate_all`(전체 실행 + TCC 업로드), `@evaluate_rows`(행 범위 지정)처럼 태그 단위로 실행을 쪼개두었습니다. 덕분에 전체를 돌릴지 일부만 검증할지 도메인 담당자가 시나리오 안의 태그와 행 번호만 바꿔서 직접 평가를 수행할 수 있게 되었습니다.

<img src="/assets/images/20260728_02_bdd_judge_pipeline.svg" alt="BDD 기반 LLM Judge 평가 파이프라인" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

### 스텝(Step)은 얇게, 로직은 서비스 레이어로

Gherkin 시나리오의 문장은 파이썬 스텝 정의 함수에 1:1로 매핑됩니다. 자연어 문장과 실제 동작 코드를 이어주는 다리 역할을 하는 셈입니다.

```python
# tests/steps/bert_llm_judge_steps.py
from behave import given, when, then

@when('"{sheet_name}" 시트의 {start_row:d}행부터 {end_row:d}행까지 평가를 실행하면')
def step_eval_rows(context, sheet_name, start_row, end_row):
    """특정 행 범위만 평가하고 TCC에 업로드."""
    from tests.services.post_evaluation_service import PostEvaluationService
    context.success = PostEvaluationService().run(
        sheet_name=sheet_name,
        start_row=start_row,
        end_row=end_row,
        spreadsheet_id=getattr(context, 'gs_spreadsheet_id', None),
        tcc_execution_id=getattr(context, 'tcc_execution_id', None),
    )

@then('평가 결과가 TestCaseCraft에 업로드되어야 함')
def step_eval_uploaded(context):
    assert context.success is True, "평가 실행 또는 TCC 업로드에 실패했습니다."
```

`{start_row:d}` 처럼 타입을 지정해두면 "2행부터 5행까지"라는 한글 문장에서 파이썬 `int` 값이 알아서 파싱되어 넘어옵니다. 도메인 담당자는 시나리오 속 숫자만 바꾸면 되고 코드는 손댈 필요가 없습니다.

여기서 가장 신경 쓴 원칙은 **스텝 레이어는 최대한 얇게 유지하고, 실제 평가/채점 로직은 `services/`와 `utils/llm/` 내부로 밀어 넣는 것**이었습니다. 스텝 함수 안에 구현 로직이 쌓이기 시작하면 문장과 실제 동작 간의 불일치가 생기고, "시나리오가 곧 제품 명세서"라는 전제가 금세 무너지기 때문입니다.

디렉터리별로 책임을 어떻게 나누었는지는 아래 그림과 같습니다.

<img src="/assets/images/20260728_06_bdd_code_structure.svg" alt="tests 디렉터리 구조와 레이어별 책임" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

시나리오가 바뀔 때는 위쪽 두 칸만 손대고, 채점 로직 자체를 고칠 때만 아래쪽 두 칸을 건드립니다. 도메인 담당자가 파이썬 코드를 몰라도 `.feature` 파일의 시트명과 행 번호만 고쳐서 새 검증을 돌릴 수 있는 이유가 바로 이 구조 분리 덕분입니다.

## 채점 로직과 프롬프트 설계

MT-Bench 논문에서 가져온 핵심 구조는 **참조 답안 기반 채점(Reference-Guided Grading)**입니다. [질문], [기준 정답(Ground Truth)], [후보 답변] 3가지를 주어, 정답을 기준으로 후보 답변을 평가하게 했습니다.

초기에는 단순하게 이진 판정(True/False)으로 만들었습니다.

```python
# 초기 버전 (현재는 주석으로 남아 있습니다)
# 반드시 JSON으로만 답변: {"is_correct": true/false, "score": 0~1, "reason": "..."}
```

하지만 실무에 적용해 보니 곧바로 문제가 드러났습니다. "내용은 맞는데 근거 조항 번호를 누락한 답변"을 어떻게 처리해야 할지 애매했기 때문입니다. `true`로 넘기자니 조항 누락이라는 결함이 숨겨지고, `false`로 떨어뜨리자니 90% 이상 맞춘 답변이 완전히 실패로 처리되었습니다. 결과가 모 아니면 도여서, 모델 업데이트 후 답변 품질이 살짝 나빠졌을 때 회귀 감지를 할 수 없었습니다.

그래서 1~4점 척도로 세분화하고, 각 점수의 의미를 프롬프트에 명시했습니다.

```python
# tests/utils/llm/services/openai_service.py
def llm_judge(self, question, ground_truth, candidate):
    prompt = f"""You will be given a [Question], a [Ground Truth] answer, and a [Candidate Answer].
Your task is to provide a 'Total rating' scoring how well the [Candidate Answer] answers
the [Question], using the [Ground Truth] as the ultimate reference for correctness.

Give your answer on a scale of 1 to 4:
1: The answer is terrible: completely irrelevant, or very partial/incorrect vs the Ground Truth.
2: mostly not helpful: misses key aspects or contains significant inaccuracies.
3: mostly helpful: generally correct, but could be improved in detail or directness.
4: excellent: relevant, direct, detailed, and addresses all concerns accurately.

[Question]: {question}
[Ground Truth]: {ground_truth}
[Candidate Answer]: {candidate}

Return strictly JSON:
- "is_correct": boolean (true if the score is 3 or 4)
- "score": number (1 to 4)
- "reason": string (rationale in Korean)
"""
    response = self.client.chat.completions.create(
        model=self.model,                          # gpt-4o-mini
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a strict QA evaluator. Always respond in JSON format."},
            {"role": "user", "content": prompt},
        ],
    )
```

몇 가지 핵심 설정들의 목적은 다음과 같습니다.

- **`temperature=0`**: 판정 결과의 흔들림을 최소화하기 위함입니다. 다만 이걸 "100% 동일한 결과가 보장된다"고 표현하는 건 사실이 아닙니다. OpenAI API는 temperature 0에서도 약간의 변동성이 존재하기 때문입니다. 완전한 재현성보다는 "판정 일관성을 최대한 다잡는 최소 장치"로 사용했습니다.
- **`response_format={"type": "json_object"}`**: JSON 출력 형식을 강제하여 파싱 에러를 지웠습니다. 이전에는 LLM이 서두에 "다음은 채점 결과입니다" 같은 서술을 덧붙여 파이썬의 `json.loads()`가 터지는 일이 잦았는데, 이 옵션 적용 후 파싱 관련 예외가 깔끔히 해결되었습니다.
- **`reason` (한글 사유)**: 채점 이유를 한글로 출력하게 한 점이 실무에서 큰 도움이 되었습니다. FAIL이 났을 때 단순 점수뿐만 아니라 감점 원인이 원문과 함께 남기 때문에, 채점 결과를 바로 디버깅 리포트로 활용할 수 있었습니다. 추후 사람이 2차 검수하는 '휴먼 인 더 루프' 단계에서도 판단 시간을 크게 줄여주었습니다.

### 정답지(Ground Truth)가 없을 때는 어떻게 하나

채점 프레임워크를 갖추고 나서 바로 부딪힌 현실적인 벽은 **평가에 쓸 정답지(Ground Truth)가 따로 없었다**는 점입니다.

규정 원문 마크다운(.md) 파일과 질의 목록은 있었지만, 각 질문에 1:1로 대응하는 모범 답안(Reference)이 준비되어 있지 않았습니다. Reference-Guided 방식을 채택했으나, 정작 참조할 정답이 비어 있어 닭과 계란처럼 무엇이 먼저인지 알 수 없는 막막한 상황이었죠.

이 문제를 풀기 위해 평가 스크립트에 **4가지 실행 모드**를 나누어 구현했습니다. 정답지가 없으면 규정 원문에서 정답 구절을 먼저 자동으로 뽑아내고, 필요하면 추출 직후 바로 채점까지 연달아 이어지도록 흐름을 잡았습니다.

| 모드 | 역할 |
|---|---|
| `EVALUATE` | 기존 시트에 있는 정답지(GT)와 후보 답변을 대조해 채점 |
| `EXTRACT_GT` | 규정 원문(.md)에서 질문에 대응하는 근거 조항 추출 (파일·페이지·조항명) |
| `GENERATE_QA` | 규정 원문을 훑어서 평가용 Q&A 세트를 자동 생성 |
| `QA_RESULT` | 정답 추출 직후 후보 답변과 곧바로 대조 평가 |

특히 `EXTRACT_GT` 모드는 단순 답변 텍스트만 뽑는 것이 아니라, 근거가 숨어 있는 문서 파일명과 조항 위치까지 정확히 파싱해 줍니다.

```python
def extract_ground_truth(self, question, context):
    prompt = f"""당신은 규정 해석 전문가입니다. [규정 내용]을 바탕으로 [질문]의 답을 추출하세요.
지침:
1. 페이지 마커로 **파일이름**과 **페이지**를 식별
2. 답변이 포함된 **조항 이름** 추출
3. 조항 본문을 **생략 없이 전문** 추출
4. 1000자 내외 모범 답변 요약
반드시 JSON: {{"file_name", "page", "item", "text", "answer"}}
...
[질문]: {question}"""
```

여기서 조항 전문(`text`)과 요약본(`answer`)을 굳이 나누어 추출하는 파이썬 구조도 실무적인 이유 때문이었습니다. LLM Judge가 채점 기준표로 삼을 때는 생략 없는 조항 전문(`text`)이 들어가야 엄격하게 평가할 수 있고, 나중에 사람이 결과를 훑어보거나 검수할 때는 1000자 요약본(`answer`)이 훨씬 가독성이 좋았기 때문입니다.

이러한 모드 분리 덕분에 정답지가 완전히 비어 있던 초기 상태에서도 규정 원문으로부터 정답지를 자체 추출해가며 평가를 돌릴 수 있었습니다.

### KoBERTScore 병행과 현실적인 한계

LLM Judge 하나에만 채점을 온전히 맡기기에는 솔직히 불안했습니다. MT-Bench 논문에서 읽었던 장황함 편향이나, 그럴듯해 보이지만 원문 맥락을 살짝 비튼 환각 답변을 LLM 채점기 혼자 감지하지 못할 위험이 늘 따라다녔기 때문입니다.

그래서 텍스트의 문맥 의미 유사도를 측정하는 `KoBERTScore`를 교차 검증용 독립 신호로 함께 묶었습니다.

```python
# tests/utils/llm/evaluator.py
if self.config.eval_type in ["BOTH", "BERT"]:
    bert_score = self.bert.calculate([candidate], [ground_truth])

if self.config.eval_type in ["BOTH", "LLM"]:
    res, tk = self.openai.llm_judge(question, ground_truth, candidate)
    llm_score = res.get("score", 0)
```

`eval_type` 파라미터로 `BOTH / BERT / LLM` 옵션을 스위칭할 수 있게 구현했습니다. 매일 돌리는 가벼운 정량 모니터링 때는 BERT만 빠르게 돌려 비용을 아끼고, 배포 직전 정밀 검증을 할 때는 둘 다 실행하는 방식입니다.

하지만 솔직히 짚고 넘어갈 한계점도 있습니다. **현재 시스템의 최종 합불 판정은 결국 LLM 점수만으로 결정**됩니다. 3점 이상인지 나타내는 `is_correct` 값만 시트와 TCC(TestCaseCraft)의 통과 기준으로 반영되고, KoBERTScore는 참고용 스코어로 기록되는 데 그치고 있습니다.

두 점수의 척도가 달랐던 탓이 큽니다. KoBERTScore는 0~1 사이의 float 값이고, LLM 점수는 1~4점 사이의 점수인데, 적절한 정규화(Normalization) 기준 없이 합치면 지표 자체가 왜곡될 수 있었기 때문입니다. 원래 목표는 '두 개의 독립 신호를 융합한 완전한 교차 검증'이었지만, 실제 현장에서는 'LLM 판정 + BERT 참고 스코어'의 보조 구조로 운용하고 있는 것이 솔직한 현실입니다.

채점 실행 결과는 터미널 CLI에서 바로 확인할 수 있도록 표 형태로 출력되게 해두었습니다.

```text
+-----+---------+--------+-----+--------+--------+------------------------------+
| row | correct | bert   | llm | final  | tokens | reason                       |
+-----+---------+--------+-----+--------+--------+------------------------------+
| 5   | PASS    | 0.8123 | 4   | 2.7249 | 1204   | 정답 조항을 정확히 인용하고… |
+-----+---------+--------+-----+--------+--------+------------------------------+
```

## 채팅 응답부터 자동 평가, 이력 관리까지 한 번에 잇기

파이프라인 구축의 마지막 단계는 실제 GraphRAG 서비스에 질문을 던지고, 응답이 오는 즉시 자동 채점 후 그 결과를 테스트 관리 시스템(TestCaseCraft, TCC)에 올리는 전체 흐름을 하나로 매끄럽게 연결하는 작업이었습니다.

검증 결과를 로컬 파일로만 남기면 시간이 지날수록 이력을 추적하거나 모델 버전별 품질 변화를 비교 관리하기가 벅찼습니다. 그래서 TCC와 연동하여 모든 평가 이력이 중앙에서 자동으로 기록되도록 설계했습니다.

```gherkin
# language: ko
기능: Thread API 관리 (자동 평가 포함)

  배경:
  먼저 채팅 완료 후 자동 평가를 활성화함     # 이 줄을 주석 처리하면 평가 OFF

@thread
시나리오: 3급면허취득-30
  먼저 구글 시트 ID "1LaJ..."와 시트 이름 "0515"를 사용함
  그리고 TestCaseCraft 테스트 실행 ID를 "885d..."로 지정한다
  먼저 로그인된 사용자임
  만약 제목 "K200 면허취득 테스트", 내용 "3급면허취득", assistant_id 30로 Thread 생성을 요청하면
  그러면 응답 상태 코드는 201이어야 함
  먼저 CSV 파일 "tests/data/chat_contents_vector_book.csv"에서 대화 내용을 로드함
  만약 생성된 Thread ID로 모든 대화 내용에 대해 채팅 후 즉시 평가를 순차로 요청하면
  그러면 채팅 응답이 성공적으로 수신되어야 함
```

`배경(Background)` 절의 문장 하나로 평가 실행 유무를 제어하도록 구성했습니다.

```python
@given('채팅 완료 후 자동 평가를 활성화함')
def step_enable_post_eval(context):
    context.enable_post_eval = True   # 각 시나리오 끝의 평가 step이 이 플래그를 본다
```

채팅 기능만 빠르게 검증할 때는 해당 스텝 줄 앞에 `#`을 붙여 끄고, 평가와 TCC 업로드까지 통으로 돌릴 때는 주석을 풀면 됩니다. 시나리오를 실행하면 CSV 파일에 있는 질문을 순서대로 읽어서 채팅을 실행하고, 곧이어 채점 결과를 TCC에 올려두는 루프가 행 단위로 돌아갑니다.

### CI 파이프라인에 이식하기

로컬 수동 실행 방식에서 벗어나 `behavex` 기반으로 병렬 실행 환경을 꾸렸습니다. 젠킨스(Jenkins) 배치 Job으로 등록해 주기적으로 회귀 테스트를 돌리도록 했습니다.

```bash
# 특정 행 범위만, 2개 프로세스로 병렬 실행
uv run behavex -t @evaluate_rows tests/features/bert_llm_judge.feature --parallel-processes 2

# 채팅 + 평가 통합 시나리오 실행
uv run behavex -t @thread tests/features/localTest_with_eval.feature
```

실행 시점에 `-D ASSISTANT_ID=30`, `-D GS_SHEET_NAME=0515`, `-D TCC_EXECUTION_ID=NEW` 같은 동적 파라미터를 넘겨 환경변수를 유연하게 바꿉니다. 실행 결과는 JUnit XML로 생성되어 TestCaseCraft에 자동 반영되고, Allure 대시보드 리포트로도 함께 남습니다.

## 실제 운영하며 개선한 작업들

- **Pass/Fail 이진 판정에서 1~4점 척도로 개편**: 3점이던 점수가 2점으로 내려가는 미세한 변화 자체가 신호가 되었습니다. 이진 판정이었다면 통과로 숨겨졌을 감점 사유들이 명확히 보이기 시작했습니다.
- **채점 사유(`reason`) 필수 수집**: FAIL 목록을 열었을 때 "조항 번호 누락", "예외 조항 미인용", "잘못된 조항 인용" 같은 감점 사유가 한눈에 들어와 디버깅 시간을 크게 아낄 수 있었습니다.
- **JSON 응답 강제 및 Temperature 0 설정**: 파싱 에러와 판정 일관성을 다잡는 최소한의 장치가 되었습니다.
- **프롬프트 캐싱(Prompt Caching) 적중 확인**: 규정 전문을 프롬프트에 통째로 넣는 방식이라 입력 토큰이 긴 편인데, OpenAI 프롬프트 캐싱이 적중하면 비용과 응답 대기 시간이 절반 가까이 줄어듭니다. 이를 모니터링하도록 로그를 남겨 두었습니다.

```python
def _log_token_usage(self, response, action_name):
    if response.usage and getattr(response.usage, 'prompt_tokens_details', None):
        cached = getattr(response.usage.prompt_tokens_details, 'cached_tokens', 0)
        if cached and cached > 0:
            logger.info(f"[캐싱 적중/{action_name}] {cached} 토큰 재사용")
```

- **구글 시트 API 배치(Batch) 업데이트**: 행 단위로 요청을 날리던 방식에서 20건씩 묶어 업데이트하는 방식으로 수정했습니다. API 호출 횟수가 1/20로 줄어들면서 시트 API Rate Limit 오류가 해결되었습니다.
- **`behavex` 프로세스 병렬화**: 시트 데이터를 순차적으로 채점하던 방식에서 `--parallel-processes` 옵션으로 분산 처리했습니다. LLM API 응답 대기 시간(I/O Bound)이 긴 작업 특성상, 프로세스를 나누는 것만으로 전체 테스트 소요 시간이 획기적으로 줄었습니다.

### 정답 생성 모델과 채점 모델의 분리

학술 논문을 읽고 실제 파이프라인 코드를 고치게 만든 대표적인 계기가 바로 이 항목이었습니다.

처음 시스템을 구축할 때는 `config.py`에 `default_model = "gpt-4o-mini"` 하나만 선언해 두었습니다. `EXTRACT_GT`로 정답을 추출하는 역할과 `llm_judge`로 답변을 채점하는 역할을 모두 동일한 모델이 전담한 셈입니다. 정답지가 없는 상태에서 우선 파이프라인을 굴리는 것이 급했기에 별다른 문제의식 없이 가장 간편한 방식을 택했습니다.

하지만 [`Preference Leakage`](https://arxiv.org/abs/2502.01534)(arXiv:2502.01534, ICLR 2026) 논문을 읽으면서 저희 아키텍처가 오염에 무방비로 노출되어 있음을 깨달았습니다. 논문의 초록에 저희가 구현했던 구조가 정확히 짚여 있었기 때문입니다.

> "we expose **preference leakage**, a contamination problem in LLM-as-a-judge caused by the **relatedness between the synthetic data generators and LLM-based evaluators.**"

합성 데이터(정답지)를 만든 모델과 이를 채점하는 평가자 모델 간에 연관성이 높을수록 편향 오염이 발생한다는 지적입니다. 저자들은 이 연관성의 단계를 3가지로 나누었습니다.

| 연관성 단계 | 설명 | 바꾸기 전 저희 상태 |
|---|---|---|
| **동일 모델** | 정답 생성기와 평가자가 100% 동일한 모델 | **여기에 직접 해당했습니다** |
| **상속 관계** | 한쪽 모델이 다른 쪽에서 파생/파인튜닝된 모델 | 해당 없음 |
| **동일 패밀리** | 동일한 계열(Family)의 다른 크기/버전 모델 | 해당 없음 |

저희는 가장 위험도가 높은 1단계(동일 모델)에 그대로 노출되어 있었습니다. 특히 `QA_RESULT` 모드는 규정에서 정답을 추출한 직후 동일한 모델이 곧바로 그 정답을 기준으로 채점을 수행했으므로, 논문이 경고한 오염 경로가 단 하나의 함수 실행 안에서 일어나는 구조였습니다.

특히 이 논문에서 가장 서늘했던 경고는 **"선호 오염은 기존의 다른 편향들보다 외부 탐지가 훨씬 어렵다"**는 대목이었습니다. 위치 편향은 답변 순서를 스왑해보면 바로 드러나고, 장황함 편향은 답변 길이와 점수의 상관관계를 뜯어보면 잡힙니다. 그러나 정답 생성기와 평가자가 같아서 생기는 오염은 밖에서 볼 때 그저 "채점 점수가 안정적으로 높게 잘 나오는 상태"로만 보입니다. 지표가 좋게 나오는데 이것이 모델의 실제 성능 때문인지 오염에 의한 착시인지 구분하기가 매우 까다롭습니다. 저희 역시 그 착시 속에 수개월간 테스트를 돌렸던 셈입니다.

논문을 읽은 직후 GT 추출 모델과 채점 모델 설정을 즉시 분리했습니다.

```python
# 바꾸기 전: 동일한 모델이 정답 추출과 채점을 모두 담당
default_model: str = "gpt-4o-mini"

# 바꾼 뒤: 정답 추출과 채점 모델을 서로 다른 계열로 완전 분리
gt_model: str = "..."      # 정답(GT) 추출 전용 모델
judge_model: str = "..."   # 채점 전용 모델 (gt_model과 타사/다른 계열 사용)
```

논문 기준으로는 동일 계열(Same Family) 모델끼리도 관련성 오염 범위에 포함되므로, 가능한 한 완전히 다른 모델 계열로 배치하는 편이 안전합니다. API 관리 포인트가 늘어나고 비용이 살짝 상승하더라도, "자기가 만든 정답지로 자기가 채점하는" 구조적인 맹점을 방치하는 것보다는 훨씬 건강한 검증 체계라고 판단했습니다.

## 실패(FAIL) 건만 사람이 검수하는 Human-in-the-Loop 워크플로

LLM-as-a-Judge 파이프라인을 설계하며 세운 가장 중요한 원칙 중 하나는 **'100% 전량 자동화'를 목표로 삼지 않는 것**이었습니다.

MT-Bench 연구에서도 입증되었듯, 인간 평가자와 LLM 채점기 간의 일치도는 약 85% 수준이며, 답변 간 품질 차이가 미세해질수록 일치도는 70%선까지 하락합니다. 실제로 실무 QA 현장에서 마주치는 회귀(Regression)의 대다수는 바로 이 미세한 구간에서 발생합니다.

이 상황에서 판정을 100% 자동 채점기에만 맡겨버리면, 잘못 판정된 오탐(False Alarm)이 리포트에 그대로 남게 됩니다. 정상적인 답변을 FAIL로 잘못 판정하는 오탐은 검증 대시보드 전체의 신뢰도를 빠르게 무너뜨립니다. 일단 "대시보드 수치를 믿을 수 없다"는 분위기가 형성되면 아무리 고도화된 자동화 도구라도 외면받게 됩니다.

그래서 저희는 검수 프로세스 중간에 '사람'을 두었습니다. 전수 검사를 진행하는 대신, **LLM Judge가 FAIL로 분류한 케이스들만 검수 큐(Queue)에 넣어 사람이 2차로 확인**하도록 시스템을 설계했습니다.

<img src="/assets/images/20260728_05_human_in_the_loop.svg" alt="실패 케이스만 사람이 보는 구조" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

```
전체 케이스 → LLM Judge 채점 → PASS → 자동 통과 (결과 기록)
                              → FAIL → 사람 2차 검수 큐
```

이 구조 덕분에 사람 검수자의 역할과 작업 성격이 크게 바뀌었습니다. 기존에는 질문과 원문 조항, 답변을 처음부터 끝까지 일일이 대조해야 했지만, 이제는 LLM Judge가 남긴 `reason`(감점 사유)을 먼저 읽고 **"이 판정 사유가 타당한가?"**를 1차로 확인합니다. 근거가 타당하면 버튼 클릭 한 번으로 확정하고, 판정이 애매할 때만 조항 전문을 직접 대조합니다.

MT-Bench 실험에서도 사람에게 GPT-4의 채점 근거를 보여주었을 때 75%가 그 타당성을 인정하고 34%는 자신의 선택을 바꾸었다는 결과가 있습니다. 저희는 그 학술적 실험 구조를 실제 검수 워크플로로 이식한 셈입니다. 사람은 '전수 판정자'에서 '결함 검토자'로 이동했습니다.

사람이 검수하는 데이터의 양은 전체 질의 중 FAIL로 판정된 비율만큼 대폭 줄었습니다. 중요한 점은 검수 자체를 없앤 것이 아니라 **검수의 범위를 좁혔다는 사실**입니다. 검수를 완전히 없애면 품질 보증 책임이 모호해지지만, 검수 범위를 좁히면 책임은 유지하면서 작업 부하만 획기적으로 낮출 수 있습니다.

다만 한 가지 주의할 점이 있었습니다. 검수자가 읽는 `reason` 문장 역시 LLM이 작성한 글이라는 점입니다. 채점기가 편향이나 환각에 빠져 잘못된 판정을 내리더라도, 이유 서술 문장은 그럴듯하게 출력될 수 있습니다. 검토자가 문장의 매끄러움에 속아 판정을 무심코 통과시킨다면 검수 절차가 무용지물이 될 수 있습니다.

이 문제를 다룬 논문이 바로 [`Who's Your Judge?`](https://arxiv.org/abs/2509.25154)(arXiv:2509.25154)입니다. 저자들은 LLM이 생성한 채점 판정문 자체를 탐지하는 'Judgment Detection' 과제를 제안하며, 단순 텍스트 탐지기만으로는 점수와 후보 답변 내용 사이의 상호작용을 포착하기 어렵다고 지적합니다.

저희는 이 논문을 바탕으로 **판정문 자체도 검증 대상**이라는 관점을 채택했습니다. 이를 위해 FAIL 검토 UI 화면을 개선하여, LLM의 채점 사유(`reason`)만 보여주는 것이 아니라 **관련 원문 조항 텍스트를 나란히 띄워(Side-by-side) 대조**할 수 있도록 했습니다. 검토자가 근거와 원문을 동시에 훑어봄으로써, Judge가 엉뚱한 조항을 근거로 삼았을 때 즉시 잡아낼 수 있도록 2차 안전장치를 마련했습니다.

무엇보다 큰 결실은 **평가 기준이 누구나 읽을 수 있는 명확한 자연어 명세서로 정립되었다는 점**입니다. 공공, 금융, 제조 등 새로운 도메인으로 검증을 확장할 때도 파이프라인 코드를 고칠 필요 없이 규정 마크다운(.md) 파일과 시나리오 몇 줄만 교체하면 즉시 QA를 수행할 수 있게 되었습니다.

## 참고한 논문의 저자 목록을 보며

참고 문헌을 정리하다 보니 재미있는 공통점이 눈에 띄었습니다.

인용한 6편의 논문 중 4편에서 Dawei Li, Zhen Tan, Bohan Jiang, Huan Liu 같은 연구자 이름이 반복해 등장하고, MT-Bench 역시 Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Hao Zhang 등의 연구진으로 연결됩니다. 전반적으로 중국계 연구자들의 비중이 꽤 높은 편입니다.

다만 소속 기관을 함께 볼 필요가 있습니다. MT-Bench는 UC Berkeley, UCSD, CMU, Stanford 소속이고, 서베이 관련 4편은 Arizona State University, UIUC, UCLA, Notre Dame 등 **대부분 미국 주요 대학과 연구 기관**에 기반을 두고 있습니다. 국적을 떠나 미국 연구 기관을 거점으로 형성된 두터운 연구 생태계의 힘을 실감하게 됩니다.

이 저자 목록을 보면서 가장 깊게 남은 생각은 평가 방법론의 '연구 밀도'였습니다. 평가 연구가 두껍게 쌓인 생태계일수록 모델을 개선하는 피드백 루프(Feedback Loop)가 비약적으로 빠르게 돕니다. Kimi나 DeepSeek, Qwen 같은 모델들이 짧은 주기로 괄목할 성장을 내놓는 배경에도 이러한 평가 연구의 높은 밀도가 자리 잡고 있다고 봅니다.

모델을 잘 만드는 능력과 정확히 평가하는 능력은 선순환 구조로 함께 성장합니다. 평가 체계가 정밀해야 무엇을 고쳐야 할지가 명확히 보이고, 그래야 다음 버전으로 이어지는 개선 루프가 빨라집니다. 반대로 평가 체계가 부실하면 결국 감에 의존해 개발하게 됩니다.

앞으로 벌어질 진짜 격차는 단순한 모델 성능 지표보다 **개선 루프의 회전 속도**일 것입니다. 성능은 자본과 컴퓨팅 자원으로 추격할 수 있지만, 루프의 속도는 조직이 평가 체계를 얼마나 정교하게 다루는지에서 나오기 때문입니다.

반가운 논문도 있었습니다. 이 글에서 가장 핵심적인 방법론으로 인용한 CheckEval의 저자진이 서울대학교, KAIST, NAVER, SK텔레콤, Boston University 소속의 한국 연구진이었습니다. 최신 평가 체계의 단단한 발판 하나를 국내 연구진이 미리 만들어 둔 셈입니다.

사내 QA 파이프라인에 최신 논문의 평가 방법론을 붙이는 일 자체는 거창한 학술 연구가 아닙니다. 그럼에도 현장에서 부딪치며 쌓은 경험과 시행착오를 기록해 나누는 시도가 더 늘어나야 한다고 믿습니다. 특히 규정 QA처럼 한국어 특수성이 강한 영역의 평가 체계는 결국 현장의 엔지니어들이 직접 만들어 나갈 수밖에 없습니다. 영어권 벤치마크로는 조항 간 위계나 부칙 해석 같은 맥락을 검증하기 어렵기 때문입니다.

공개 블로그 형태로 다듬어 글을 나누는 이유도 여기에 있습니다.

긴글 읽어주셔서 감사합니다.

---

## 참고 문헌

- Zheng, L., Chiang, W-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., Stoica, I. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023 Datasets and Benchmarks Track. arXiv:2306.05685v4
  <https://arxiv.org/abs/2306.05685> · 코드 <https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge>
- Lee, Y., Kim, J., Kim, J., Cho, H., Kang, J., Kang, P., Kim, N. (2025). *CheckEval: A reliable LLM-as-a-Judge framework for evaluating text generation using checklists.* EMNLP 2025. arXiv:2403.18771v3
  <https://arxiv.org/abs/2403.18771> · 코드 <https://github.com/yukyunglee/CheckEval>
- Fabbri, A. R., Kryściński, W., McCann, B., Xiong, C., Socher, R., Radev, D. (2021). *SummEval: Re-evaluating Summarization Evaluation.* TACL. <https://arxiv.org/abs/2007.12626>
  (CheckEval 이 사람 평가자 간 일치도 κ ≈ 0.7 의 근거로 인용한 논문입니다)
- Li, D., Jiang, B., Huang, L., Beigi, A., Zhao, C., Tan, Z., Bhattacharjee, A., Jiang, Y., Chen, C., Wu, T., Shu, K., Cheng, L., Liu, H. (2025). *From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge.* EMNLP 2025. arXiv:2411.16594
  <https://arxiv.org/abs/2411.16594>
- Li, D., Sun, R., Huang, Y., Zhong, M., Jiang, B., Han, J., Zhang, X., Wang, W., Liu, H. (2025). *Preference Leakage: A Contamination Problem in LLM-as-a-judge.* ICLR 2026. arXiv:2502.01534
  <https://arxiv.org/abs/2502.01534>
- Li, D., Tan, Z., Zhao, C., Jiang, B., Huang, B., Ma, P., Alnaibari, A., Shu, K., Liu, H. (2025). *Who's Your Judge? On the Detectability of LLM-Generated Judgments.* arXiv:2509.25154 (심사 중)
  <https://arxiv.org/abs/2509.25154>
- Li, D., Yao, Y., Tan, Z., Liu, H., Guo, R. (2026). *ToolPRMBench: Evaluating and Advancing Process Reward Models for Tool-using Agents.* ACL 2026. arXiv:2601.12294
  <https://arxiv.org/abs/2601.12294>
- 위 네 편은 <https://llm-as-a-judge.github.io/> 와 <https://github.com/llm-as-a-judge/Awesome-LLM-as-a-judge> 에 정리되어 있습니다.
- Judge 프롬프트의 채점 척도와 H100 트릭은 HuggingFace Open-Source AI Cookbook 의 RAG 평가 레시피를 참고했습니다.
  <https://huggingface.co/learn/cookbook/en/rag_evaluation>
