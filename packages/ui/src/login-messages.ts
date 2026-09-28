// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)

/** 서버 응답 원문을 사용자에게 노출하지 않는 기본 상태 코드 사전이다. */
export function getLoginErrorMessage(status?: number): string {
  switch (status) {
    case 503: return "로그인 설정을 확인할 수 없습니다. 관리자에게 문의해 주세요.";
    case 429: return "로그인 시도가 너무 많습니다. 잠시 후 다시 시도해 주세요.";
    case 403: return "허용되지 않은 요청입니다. 접속 경로를 확인해 주세요.";
    default: return "아이디 또는 비밀번호를 확인해 주세요.";
  }
}
