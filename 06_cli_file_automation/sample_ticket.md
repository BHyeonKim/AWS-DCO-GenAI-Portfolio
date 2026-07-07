# [교육용 샘플 데이터 사용] SAMPLE Network Incident Ticket

> [!IMPORTANT]
> **본 문서는 교육용 샘플 데이터를 사용하고 있으며, 실제 AWS 내부 정보, 실제 장비명, 실제 IP 주소, 실제 고객 정보 또는 실제 절차를 포함하고 있지 않습니다.**

## 1. 티켓 정보 (Ticket Information)
* **티켓 ID (Ticket ID):** EDU-TICKET-2026-0707-001
* **발생 시간 (Event Time):** 2026-07-07 14:00:00 KST
* **심각도 (Severity):** Medium (Severity 3 - Educational Sample)
* **진행 상태 (Status):** Open

## 2. 장비 및 이벤트 정보 (Equipment & Event Details)
* **샘플 장비명 (Sample Hostname):** SAMPLE_TOR_SW_01
* **대상 포트 (Target Port):** Eth1/10 (EDU-Sample-Interface)
* **탐지 이벤트 (Detected Event):** CRC Error Rate Exceeded & Link Down Event

## 3. 관찰 내용 (Observations)
* **13:55:00 KST:** `SAMPLE_TOR_SW_01` 장비의 `Eth1/10` 포트에서 CRC 에러 카운터가 지속적으로 증가하는 현상 탐지 (임계값 100/min 초과).
* **13:58:30 KST:** 해당 인터페이스가 최종적으로 `Link Down` 상태로 전환됨을 확인.
* **이전 이력:** 최근 24시간 내 동일 장비의 타 포트 혹은 인접 장비에서 유사한 CRC 에러 보고 이력 없음.

## 4. 에스컬레이션 필요 여부 (Escalation Required)
* **필요 여부:** Yes (예)
* **에스컬레이션 대상:** EDU Network Operations Team (교육용 가상 네트워크 운영팀)
* **사유:** 가상 포트 리셋(Shutdown/No Shutdown) 시도 후에도 Link가 Up되지 않으며, 물리 계층(케이블 혹은 커넥터 인터페이스) 점검 및 트랜시버 진단이 필요한 상황으로 모의함.

## 5. 보안 및 정보보호 주의사항 (Security Precautions)
* 티켓 코멘트 및 상세 설명 작성 시 **실제 고객 정보, 실제 IP 주소, 실제 네트워크 대역, 장비 시리얼 번호, 자산 태그**를 기재하지 마십시오.
* 교육 목적 외의 실제 환경 정보나 비공개 명령어 실행 결과를 문서에 삽입하는 것은 엄격히 금지됩니다.
