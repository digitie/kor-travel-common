// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { createRoot } from "react-dom/client";
import { Preview } from "./Preview.js";
const project = new URLSearchParams(location.search).get("project") ?? "map";
createRoot(document.getElementById("root")!).render(<Preview projectId={project} />);
