// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import "../../../tools/sync_frontend_policy.mjs";
import { copyFileSync } from "node:fs";
copyFileSync(new URL("../../../frontend-dependencies.json", import.meta.url), new URL("../dependency-policy.json", import.meta.url));
copyFileSync(new URL("../../../tools/check_frontend_dependencies.mjs", import.meta.url), new URL("../check-dependencies.mjs", import.meta.url));
