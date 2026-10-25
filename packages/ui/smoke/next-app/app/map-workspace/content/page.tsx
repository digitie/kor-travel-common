// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import { useState } from "react";
import { MapDetailOverlay, MapStage, MapWorkspace } from "@kor-travel/ui/map-controls";

/** 실제 재현의 오류·가격·지연 시각 조합을 고정 자료로 검증한다. 조회·가격 계산은 없다. */
export default function SummaryContentSmoke() {
  const [selected, setSelected] = useState(false);
  return <main style={{ height: "100dvh", display: "flex", flexDirection: "column", padding: 8, boxSizing: "border-box" }}>
    <header id="content-shell-header" style={{ flex: "0 0 213px" }}>
      <h1 style={{ fontSize: 16 }}>재현 자료 · API 호출 없음</h1>
      <button type="button" onClick={() => setSelected((value) => !value)}>선택 상세 전환</button>
    </header>
    <MapWorkspace>
      <MapStage summary={<div style={{ display: "grid", gap: 4, fontSize: ".875rem", lineHeight: 1.5 }}>
        <p data-essential="error" style={{ margin: 0, padding: 4, background: "var(--kt-surface-card)" }}>VWorld 지도 키가 없어 지도를 표시하지 못합니다. 위의 목록 보기에서 장소를 선택해 주세요.</p>
        <section style={{ display: "grid", gap: 4, padding: 8, border: "1px solid var(--kt-border)", borderRadius: 8, background: "var(--kt-surface-card)" }}>
          <h2 style={{ fontSize: ".875rem", margin: 0 }}>현재 지도 범위 · 휘발유</h2>
          <dl data-essential="prices" style={{ display: "flex", flexWrap: "wrap", gap: "4px 16px", margin: 0 }}>
            <div><dt>평균</dt><dd style={{ margin: 0 }}>1,750원/L</dd></div>
            <div><dt>최저</dt><dd style={{ margin: 0 }}>1,650원/L</dd></div>
          </dl>
          <p data-essential="stale" style={{ margin: 0 }}>갱신 지연 · 가격 갱신 2026. 10. 25. 오후 3:00</p>
        </section>
      </div>} detail={selected ? <MapDetailOverlay header="경부선 서울역의 긴 선택 장소 제목과 운영 기관 표시" collapsible onDismiss={() => setSelected(false)}>
        {Array.from({ length: 30 }, (_, index) => <p key={index}>선택 상세 {index + 1}</p>)}
      </MapDetailOverlay> : null}>
        <div style={{ background: "var(--kt-surface-subtle)" }}>지도 대체 영역</div>
      </MapStage>
    </MapWorkspace>
  </main>;
}
