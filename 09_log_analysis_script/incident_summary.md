# DCO 교육용 샘플 로그 분석 결과

> 이 보고서는 교육 목적으로 만든 샘플 로그(`sample_dco_log.txt`)를
> Python 표준 라이브러리만으로 분석한 결과입니다. 실제 AWS 내부
> 장비/네트워크 정보가 아니며, 실제 장비 점검이나 외부 조치를
> 요구하는 내용이 아닙니다.

## 1. 전체 로그 줄 수

- 총 140건의 로그가 확인되었습니다.

## 2. 심각도(SEVERITY)별 개수

| 심각도 | 개수 |
|---|---|
| INFO | 135 |
| WARNING | 3 |
| ERROR | 2 |

## 3. 이벤트별 개수

| 이벤트 | 개수 |
|---|---|
| Normal heartbeat | 125 |
| Ticket opened | 3 |
| Ticket escalated | 3 |
| Maintenance completed | 3 |
| Fan Alert | 1 |
| Temperature warning | 1 |
| SSD failure warning | 1 |
| CRC error 증가 | 1 |
| Link Down | 1 |
| Link Up | 1 |

## 4. WARNING / CRITICAL 로그 목록

| 시간 | 장비 | 심각도 | 이벤트 | 메시지 |
|---|---|---|---|---|
| 2026-07-03 01:05:00 | DEMO_CORE_SW_02 | WARNING | Fan Alert | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: 198.51.100.2 |
| 2026-07-03 02:05:00 | EDU_SRV_R04_N12 | WARNING | Temperature warning | Chassis temperature reached 42C (Threshold: 40C). IP: 192.0.2.12 |
| 2026-07-03 03:05:00 | SAMPLE_TOR_SW_01 | WARNING | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |

## 5. 주요 이벤트 요약 (CRC_ERROR / LINK_DOWN / TICKET_ESCALATED)

| 구분 | 시간 | 장비 | 이벤트 | 메시지 |
|---|---|---|---|---|
| TICKET_ESCALATED | 2026-07-03 01:10:00 | DEMO_CORE_SW_02 | Ticket escalated | Ticket EDU-TKT-2026-0001 escalated to Local Infrastructure Team. |
| TICKET_ESCALATED | 2026-07-03 02:15:00 | EDU_SRV_R04_N12 | Ticket escalated | Ticket EDU-TKT-2026-0002 escalated to DCO Hardware Support. |
| CRC_ERROR | 2026-07-03 03:05:00 | SAMPLE_TOR_SW_01 | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |
| LINK_DOWN | 2026-07-03 03:06:00 | SAMPLE_TOR_SW_01 | Link Down | Interface Gi0/1 status changed to DOWN. Connection to server lost. |
| TICKET_ESCALATED | 2026-07-03 03:12:00 | SAMPLE_TOR_SW_01 | Ticket escalated | Ticket EDU-TKT-2026-0003 escalated to Onsite Cabling Team. |

---

## [ AI 활용 기록 ]

### 1. 사용한 도구

- Claude Code (Sonnet 5) — 로그 분석 Python 스크립트(`log_parser.py`) 초안 작성 및 결과 리포트 생성

### 2. AI가 생성한 내용 중 발견한 오류 또는 부족한 점

- 초기 버전에서는 '주요 이벤트 요약'을 이벤트명과 메시지를 합쳐서 키워드로 검색했는데, 그 결과 정상 복구를 알리는 하트비트 메시지(`0 CRC errors`)까지 CRC_ERROR로 잘못 분류되는 오탐(false positive)이 발생했습니다.
- 메시지 대신 이벤트명만 검사하도록 수정해서 오탐을 제거했습니다. AI가 만든 로직을 그대로 신뢰하지 않고 결과를 직접 확인하는 과정이 필요했습니다.

### 3. AI 결과에서 원본 자료와 다르거나 설명이 부족했던 부분

- (직접 작성) 원본 로그와 대조했을 때 실제로 다르거나 설명이 부족했던 부분을 이곳에 적어주세요. 예: 특정 심각도/이벤트 분류 기준, 표에 포함되지 않은 항목, 요약이 생략한 맥락 등.
