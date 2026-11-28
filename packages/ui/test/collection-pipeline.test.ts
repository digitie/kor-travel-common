// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)

import { describe, expect, it } from "vitest";
import { collectionPipelineItems, isPipelineErrorEvent } from "../src/collection-pipeline";

describe("공용 수집 메뉴", () => {
  it("지원 경로만 공용 순서로 표시하고 제품별 라벨을 유지한다", () => {
    expect(collectionPipelineItems({
      releases: { href: "/releases", label: "제품 릴리스" },
      pipeline: "/pipeline",
      offlineUploads: "/upload"
    })).toEqual([
      { capability: "pipeline", href: "/pipeline", label: "파이프라인" },
      { capability: "offlineUploads", href: "/upload", label: "오프라인 업로드" },
      { capability: "releases", href: "/releases", label: "제품 릴리스" }
    ]);
    expect(collectionPipelineItems({})).toEqual([]);
  });

  it("이벤트 오류와 오류 로그 수준을 모두 인식한다", () => {
    expect(isPipelineErrorEvent({ error: { name: "Failure" } })).toBe(true);
    expect(isPipelineErrorEvent({ level: "error" })).toBe(true);
    expect(isPipelineErrorEvent({ level: "CRITICAL" })).toBe(true);
    expect(isPipelineErrorEvent({ level: "INFO", error: null })).toBe(false);
  });
});
