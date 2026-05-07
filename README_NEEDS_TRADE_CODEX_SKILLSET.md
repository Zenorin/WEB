# NEEDS TRADE Codex Skillset

생성 시각: 2026-05-07 19:16:40 KST

이 파일셋은 `codex-skillset-starter-v4.9.5-dev-ops-r1-lite.zip` 기준으로 생성한 NEEDS TRADE 웹 리뉴얼용 Codex dev-kit입니다.

## 목적
- 기존 `www.needstrade.com`을 단순 수정 대상으로 보지 않고, 중국 소싱/OEM/굿즈제작/검수/통관/KC/원산지/창고/로켓그로스 입고 준비를 통합 운영하는 웹페이지로 재기획합니다.
- 레퍼런스 페이지는 clean-room 역할 분석용으로만 사용합니다.
- Codex가 바로 구현으로 뛰지 않도록 PRD, IA, WBS, command queue, phase gate를 먼저 생성·검증하게 합니다.

## 우선 사용 스킬
- `$needs-trade-web-renewal-intake`
- `$webpage-reference-renewal`
- `$project-reference-mapper`
- `$needs-trade-renewal-ui`
- `$quote-intake-contract`
- `$china-sourcing-ops-model`
- `$rocket-growth-inbound-flow`
- `$evidence-pack`

## 보안
실제 도메인, 호스팅, 서버, API, 쿠팡, 1688, 이메일, 카카오, DB 계정 정보는 이 repo와 문서에 넣지 않습니다. 로컬 `.env` 또는 secret store에만 넣습니다.
