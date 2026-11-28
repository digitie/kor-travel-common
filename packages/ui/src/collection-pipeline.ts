// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)

export const COLLECTION_PIPELINE_TITLE = "수집 파이프라인";

export const COLLECTION_PIPELINE_MENU = [
  ["pipeline", "파이프라인"],
  ["datasets", "데이터셋"],
  ["offlineUploads", "오프라인 업로드"],
  ["poiCacheTargets", "POI 캐시 대상"],
  ["cacheStreams", "캐시 전파 스트림"],
  ["releases", "릴리스"]
] as const;

export type CollectionPipelineCapability = typeof COLLECTION_PIPELINE_MENU[number][0];

type CollectionRoute<Href extends string> = Href | { href: Href; label?: string };

/** 앱에서 제공하는 기능을 Map 운영 메뉴 순서에 맞춰 노출한다. */
export function collectionPipelineItems<Href extends string>(
  routes: Partial<Record<CollectionPipelineCapability, CollectionRoute<Href>>>
): Array<{ capability: CollectionPipelineCapability; href: Href; label: string }> {
  return COLLECTION_PIPELINE_MENU.flatMap(([capability, defaultLabel]) => {
    const route = routes[capability];
    if (route === undefined) return [];
    const href = typeof route === "string" ? route : route.href;
    const label = typeof route === "string" ? defaultLabel : route.label ?? defaultLabel;
    return [{ capability, href, label }];
  });
}

export function isPipelineErrorEvent(event: { level?: string | null; error?: unknown }): boolean {
  const level = event.level?.toUpperCase();
  return event.error != null || level === "ERROR" || level === "CRITICAL";
}
