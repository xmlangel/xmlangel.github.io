AI(Gemini)를 활용하여 체계적인 품질관리를 위한 지라(Jira) 이슈 분석 비서 만들기
James
James

Follow
19 min read
·
Jul 11, 2025
192



AI를 이용해 소프트웨어 개발 프로젝트에 참여하는 누군가는 요구사항 분석에 도움을 받고, 누군가는 프로그램 설계와 개발에 도움을 받고, 누군가는 문서 작성에 도움을 받기도 합니다. 저는 품질관리 관점에서 가장 많이 보고 접하는 이슈라는 녀석을, AI를 이용해서 도움을 받아보고자 합니다.

Zoom image will be displayed
품질에 AI를 활용할 수 있을까?
품질관리를 위한 AI 활용 방법
안녕하세요. 크몽에서 QA를 담당하는 제임스입니다.

많은 회사가 Jira라는 도구를 이용해서 이슈(해결해야 하는 문제 혹은 사건)나 자신이 해야 하는 작업(Task)을 관리하고 있습니다.

크몽도 역시 이슈와 업무 관리를, Jira를 이용하고 있습니다. Jira에는 많은 히스토리와 앞으로의 계획, 그리고 지금 우리가 하는 일에 대해서 가장 잘 기록된 현재 진행형 백과사전과 같은 존재라 생각합니다.

대부분의 QA라 불리는 사람들은 이슈라는 녀석을 자신의 동반자와 같이 살아왔고, 앞으로도 살아가야 할 텐데요. 저 또한, 이 녀석과 함께 살아온 날짜를 세려야 셀 수 없을 정도가 된 것 같습니다.

크몽의 QA는 품질 관리에 AI를 어떤 목적을 가지고, 어떤 방법을 이용하여 AI를 활용하는지 설명해 드리려 합니다. 비서를 만들기 위한 재료는 아래와 같습니다.

로우 데이터: Jira
데이터 수집: Jira Cloud for Sheets
수집된 데이터 AI 분석: App Script
리포트 전송: Slack
매일 같이 생성되는 이슈를 하나하나 확인하기는 현실적으로 어려운 일이라 생각합니다. 더군다나 내가 하는 일이 아닌 다른 팀이나 부서에서 하는 일은 더욱이 알기 어렵습니다.

저 또한 제가 등록한 이슈나 해야 하는 일, 팀에서 해야 하는 일은 잘 알지만, 다른 팀에서 등록한 이슈나 관리해야 하는 이슈는 알기 어려운 것이 현실입니다.

품질 관리를 정말 잘하기 위해서는 최대한 이슈에 민감하게 반응해야 한다고 생각합니다. 작은 이슈든 큰 이슈든, 혹은 정말 테스트의 누락으로 발생한 이슈인지 알게 된다면 개선점을 찾고, 앞으로 해야 하는 일에 실수나 오류를 줄일 수 있을 거로 생각하게 되었습니다.

“특정 기간 내의 등록된 이슈 추이에 대해서 누가 정리를 해주면 좋겠는데?”

데이터 수집하기
Jira에서 Search Filter를 통해 분석이 필요한 이슈 목록을 추출합니다. JQL을 이용해서 특정 기간(-1W)에 누가(QA) 어떤 유형(Bug, Improvement)의 이슈를 등록했는지에 대한 목록을 추출했습니다.

reporter in (QA) and issuetype in (Bug, Improvement) and created >= -1W 
구글 시트 확장 프로그램인 Jira Cloud for Sheets를 이용해서 자동 갱신되도록 세팅합니다. 해당 기간 내의 갱신된 새로운 데이터(구글 시트에 정리된 Jira 이슈 목록)에 대해서 AI는 분석하고 향후 슬랙으로 리포트를 전송해 줄 수 있을 거로 가정합니다.

Jira Cloud for Sheets 세팅 방법입니다.

https://docs.google.com/spreadsheets/ 에 접속합니다.
임의 구글 시트를 생성합니다.
메뉴바 > 확장 프로그램 > Jira Cloud for Sheets > [Open]을 클릭합니다.
우측 사이드바 > [Get issues from Jira]를 클릭합니다.
Tab: ISSUES > Import type을 [JQL]로 변경합니다.
JQL 쿼리 입력 후 [REFRESH ISSUES] 버튼을 클릭합니다.
쿼리가 제대로 입력되었다면 Jira에서 필터링한 목록이 구글 시트에 로드됨을 확인할 수 있습니다. 또한, Tab: FIELDS에서 분석에 필요한 데이터 필드를 수정할 수 있으니 참고 바랍니다.

Jira Cloud for Sheets’s를 적극 활용해 보자.
Jira Cloud for Sheets’s tab FIELDS Edit
수집된 데이터 AI 분석: API 세팅
AI를 활용하기 위해 2가지를 세팅해야 합니다.

슬랙 Webhook URL 만들기
Gemini API 키 발급
슬랙 Webhook URL 만들기 방법입니다.

AI가 이슈에 대해서 분석한 내용을 슬랙에 전송하기 위해서 Webhook을 사용합니다. 참고로 Webhook 지원하는 어떠한 도구도 상관없습니다.

https://api.slack.com/apps 에 접속합니다.
[Create New app > From scratch] 클릭합니다.
App Name을 설정하고, Pick a workspace to develop your app in: 에서 연결할 슬랙 공간 선택합니다.
(선택) Display Information에서 슬랫봇을 원하는 디자인으로 꾸며봅니다.
Incoming Webhooks에서 Activate Incoming Webhooks의 토글: On으로 변경합니다.
아래 Webhook URLs for Your Workspace에서 [Add New Webhook]을 클릭합니다.
연결할 채널을 선택한 후, [허용]을 클릭합니다.
만들어진 Webhook URL을 [Copy] 합니다.
[6] 번의 경우 회사의 슬랙에 접근 권한 요청이 필요할 수 있습니다. 보안팀이나 슬랙 권한 관리자의 문의가 필요할 수 있으니 참고해 주세요.

Get James’s stories in your inbox
Join Medium for free to get updates from this writer.

Enter your email
Subscribe
혹은 연결이 되지 않는 에러 메시지가 발생한다면

App Home에서 Your App’s Presence in Slack의 App Display Name의 [Edit] 버튼을 클릭하여 Display Name (Bot Name)과 Default username 모두 설정한 후, [Save] 버튼을 클릭한 후 재시도합니다.
Gemini API 키 발급 방법입니다.

GPT API가 아닌 Gemini API를 사용하는 이유는 누구나 무료로 사용할 수 있기도 하고 크몽은 회사에서 지원되어 Gemini Pro를 사용할 수 있기 때문에 활용하게 되었습니다.

https://cloud.google.com/?hl=ko 에 접속합니다.
우측 상단 [콘솔]을 클릭합니다.
[새 프로젝트]를 클릭합니다.
프로젝트 이름 입력 후, [만들기]를 클릭합니다.
Google Cloud 로고 > 우측에 [프로젝트]를 클릭합니다.
https://aistudio.google.com/prompts/new_chat 에 접속합니다.
[Get API Key]를 클릭합니다.
[+ API 키 만들기]를 클릭합니다.
[복사]를 클릭합니다.
수집된 데이터 AI 분석: App Script
기본적인 동작 방식은 아래와 같습니다.

데일리 or 위클리 or 사용자 커스텀한 시간에 구글 시트 목록을 갱신합니다.
구글 시트 목록이 갱신되면 App Script가 동작하고 AI 분석이 시작됩니다.
App Script의 트리거가 시작되면 슬랙으로 메시지가 전송됩니다.
Jira 이슈 목록을 가져온 구글 시트 파일에서 메뉴바 > 확장 프로그램 > App Script를 클릭합니다. URL은 https://script.google.com/ 입니다.

Gemini를 실행시키기 위한 Script를 작성합니다.