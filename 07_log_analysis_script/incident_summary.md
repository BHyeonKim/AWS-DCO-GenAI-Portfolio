# 교육용 샘플 DCO 로그 분석 결과

*이 문서는 실제 AWS 내부 로그가 아니라 교육용 샘플 로그(`sample_dco_log.txt`)를 Python 표준 라이브러리로 분석한 결과입니다. 원인은 하나로 단정하지 않고, 로그에 나타난 내용만 정리했습니다.*

## 1. 전체 로그 줄 수

총 140줄의 로그를 확인했습니다.

## 2. 심각도별 개수

| 심각도 | 개수 |
| --- | --- |
| INFO | 135 |
| WARNING | 3 |
| ERROR | 2 |

## 3. 이벤트별 개수

| 이벤트 | 개수 |
| --- | --- |
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

## 4. WARNING 또는 CRITICAL 로그 목록

- `2026-07-03 01:05:00` | DEMO_CORE_SW_02 | WARNING | Fan Alert | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: 198.51.100.2
- `2026-07-03 02:05:00` | EDU_SRV_R04_N12 | WARNING | Temperature warning | Chassis temperature reached 42C (Threshold: 40C). IP: 192.0.2.12
- `2026-07-03 03:05:00` | SAMPLE_TOR_SW_01 | WARNING | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1

## 5. 주요 이벤트 요약 (CRC_ERROR / LINK_DOWN / TICKET_ESCALATED)

### CRC_ERROR

- `2026-07-03 03:05:00` | SAMPLE_TOR_SW_01 | WARNING | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1

### LINK_DOWN

- `2026-07-03 03:06:00` | SAMPLE_TOR_SW_01 | ERROR | Link Down | Interface Gi0/1 status changed to DOWN. Connection to server lost.

### TICKET_ESCALATED

- `2026-07-03 01:10:00` | DEMO_CORE_SW_02 | INFO | Ticket escalated | Ticket EDU-TKT-2026-0001 escalated to Local Infrastructure Team.
- `2026-07-03 02:15:00` | EDU_SRV_R04_N12 | INFO | Ticket escalated | Ticket EDU-TKT-2026-0002 escalated to DCO Hardware Support.
- `2026-07-03 03:12:00` | SAMPLE_TOR_SW_01 | INFO | Ticket escalated | Ticket EDU-TKT-2026-0003 escalated to Onsite Cabling Team.

---

> 이 요약은 교육용 시나리오 분석 연습 결과이며, 실제 장비 점검이나 실제 네트워크 진단 결과가 아닙니다. 원인 판단이 필요한 부분은 Escalation 필요 여부로 남기고, 사람이 다시 확인하는 것을 권장합니다.
