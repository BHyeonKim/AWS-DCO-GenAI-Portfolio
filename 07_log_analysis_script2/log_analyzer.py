"""
교육용 샘플 서버 로그에서 CRC error, Link Down 발생 횟수를 서버별로 세는 스크립트

- 이 스크립트는 실제 장비 로그가 아니라 교육용 샘플 로그(server*.log)만 사용합니다.
- Python 표준 라이브러리(re, pathlib, collections)만 사용합니다.
- 실제 장비 점검이나 네트워크 진단을 수행하지 않고, 이미 저장된 텍스트 파일만 읽습니다.

이번에 반영한 수정 사항:
1. 대소문자 구분 없이 인식 (예: "CRC ERROR", "Crc Error", "crc error" 모두 동일하게 처리)
2. 여러 줄에 걸쳐 기록된 오류를 하나의 사건(이벤트)으로 묶어서 계산
   - 예: "ERROR CRC ERROR detected on eth0" 다음에 이어지는
         "    -> frame check sequence mismatch, 832 bad frames" 같은 상세 설명 줄은
         새로운 오류가 아니라 바로 앞 오류에 대한 부연 설명이므로 별도로 세지 않습니다.

집계에서 제외한 것:
- "CRCcheck OK", "CRC error recovered", "interface up, no CRC error found",
  "linkdown_timer reset", "Link status: UP" 처럼 실제 오류가 아니거나 이미 복구된 안내성 로그
  (심각도가 ERROR로 기록된 줄만 "실제 발생"으로 인정합니다.)
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE_PATTERN = "server*.log"

# 대소문자를 구분하지 않고 "crc"와 "error" 사이에 공백이 있는 경우만 인정합니다.
# ("linkdown_timer"처럼 붙어 있는 표현은 오탐이므로 \s+ 로 공백을 강제합니다.)
CRC_ERROR_PATTERN = re.compile(r"crc\s+error", re.IGNORECASE)
LINK_DOWN_PATTERN = re.compile(r"link\s+down", re.IGNORECASE)

# 심각도는 "서버이름 바로 뒤에 오는 단어"로만 판단합니다.
# (메시지 안에 "error"라는 단어가 들어간 INFO 줄, 예: "no CRC error found",
#  "CRC error recovered" 까지 오류로 잘못 인식하지 않도록 위치를 고정합니다.)
SEVERITY_PATTERN = re.compile(r"\bserver\d+\s+(ERROR|INFO)\b", re.IGNORECASE)


def is_continuation_line(line):
    """줄 앞에 공백/탭이 있으면, 앞선 오류에 이어지는 상세 설명 줄로 판단합니다."""
    return line[:1] in (" ", "\t")


def is_error_line(line):
    """
    새로운 오류 이벤트가 시작되는 줄인지 확인합니다.
    심각도 표시(ERROR)는 대소문자를 구분하지 않고, 서버 이름 바로 뒤 위치를 기준으로 확인합니다.
    """
    if is_continuation_line(line):
        return False
    match = SEVERITY_PATTERN.search(line)
    return bool(match) and match.group(1).upper() == "ERROR"


def count_events_in_file(log_path):
    """
    로그 파일 하나를 읽어서 (CRC error 개수, Link Down 개수)를 반환합니다.
    여러 줄에 걸친 오류 하나는 한 번만 셉니다.
    """
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    crc_count = 0
    link_down_count = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        if not is_error_line(line):
            i += 1
            continue

        # 오류 이벤트 한 건을 시작 줄 + 뒤따르는 상세 설명 줄까지 하나의 블록으로 묶습니다.
        event_block = [line]
        j = i + 1
        while j < len(lines) and is_continuation_line(lines[j]):
            event_block.append(lines[j])
            j += 1

        block_text = " ".join(event_block)
        if CRC_ERROR_PATTERN.search(block_text):
            crc_count += 1
        if LINK_DOWN_PATTERN.search(block_text):
            link_down_count += 1

        i = j  # 블록 전체를 건너뛰고 다음 이벤트부터 다시 확인합니다.

    return crc_count, link_down_count


def main():
    log_files = sorted(SCRIPT_DIR.glob(LOG_FILE_PATTERN))

    if not log_files:
        print(f"'{LOG_FILE_PATTERN}' 패턴에 맞는 로그 파일을 찾지 못했습니다.")
        return

    results = {}  # {서버 이름: (crc_count, link_down_count)}
    for log_path in log_files:
        server_name = log_path.stem  # 예: server01.log -> server01
        results[server_name] = count_events_in_file(log_path)

    print("서버별 CRC error / Link Down 발생 횟수 (ERROR로 기록된 이벤트만 집계, 대소문자 무시)")
    print("-" * 55)
    print(f"{'서버':<12}{'CRC error':<15}{'Link Down':<15}")

    total_crc = 0
    total_link_down = 0
    for server_name, (crc_count, link_down_count) in results.items():
        print(f"{server_name:<12}{crc_count:<15}{link_down_count:<15}")
        total_crc += crc_count
        total_link_down += link_down_count

    print("-" * 55)
    print(f"{'합계':<12}{total_crc:<15}{total_link_down:<15}")


if __name__ == "__main__":
    main()
