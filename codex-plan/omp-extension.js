import { readFileSync } from "node:fs";

const PONYTAIL_MARKER = "PONYTAIL MODE ACTIVE — level:";
const PLAN_STATE_ENTRY = "codex-plan-state";
const PLAN_INSTRUCTIONS = readFileSync(new URL("./plan-prompt.md", import.meta.url), "utf8").trim();

export function resolvePlanState(entries) {
  if (!Array.isArray(entries)) return false;

  for (let i = entries.length - 1; i >= 0; i -= 1) {
    const entry = entries[i];
    if (entry?.type === "custom" && entry?.customType === PLAN_STATE_ENTRY) {
      return entry?.data?.active === true;
    }
  }

  return false;
}

export function removePonytailInstructions(systemPrompt) {
  const parts = Array.isArray(systemPrompt) ? systemPrompt : [String(systemPrompt || "")];

  return parts
    .map((part) => {
      const markerIndex = part.lastIndexOf(PONYTAIL_MARKER);
      return markerIndex === -1 ? part : part.slice(0, markerIndex).trimEnd();
    })
    .filter(Boolean);
}

export default function codexPlanPonytailBridge(pi) {
  let planActive = false;
  let lastCtx = null;

  pi.setLabel("Codex Plan / Ponytail Bridge");

  function syncStatus(ctx) {
    if (ctx) lastCtx = ctx;
    lastCtx?.ui?.setStatus?.(
      "codex-plan",
      planActive ? "Codex Plan · Ponytail suspended" : undefined,
    );
  }

  function setPlanActive(active, ctx) {
    if (planActive === active) {
      syncStatus(ctx);
      return;
    }

    planActive = active;
    pi.appendEntry(PLAN_STATE_ENTRY, { active });
    syncStatus(ctx);
  }

  pi.registerCommand("codex-plan", {
    description: "Start a persistent Codex Plan session; use /codex-plan end to exit",
    handler: async (args, ctx) => {
      const request = String(args || "").trim();
      if (/^end$/i.test(request)) {
        if (!planActive) {
          ctx?.ui?.notify?.("Codex Plan is not active.", "warning");
          return;
        }

        setPlanActive(false, ctx);
        ctx?.ui?.notify?.("Codex Plan ended; Ponytail full is active again.", "info");
        return;
      }

      if (!request) {
        ctx?.ui?.notify?.("Usage: /codex-plan <request> | /codex-plan end", "warning");
        return;
      }

      const wasActive = planActive;
      setPlanActive(true, ctx);
      if (!wasActive) {
        ctx?.ui?.notify?.("Codex Plan started; Ponytail is suspended until /codex-plan end.", "info");
      }

      if (ctx?.isIdle?.() === false) {
        pi.sendUserMessage(request, { deliverAs: "followUp" });
        return;
      }

      pi.sendUserMessage(request);
    },
  });

  pi.on("session_start", async (_event, ctx) => {
    const entries = ctx?.sessionManager?.getBranch?.() || ctx?.sessionManager?.getEntries?.() || [];
    planActive = resolvePlanState(entries);
    syncStatus(ctx);
    if (planActive) {
      ctx?.ui?.notify?.("Codex Plan resumed; Ponytail remains suspended.", "info");
    }
  });

  pi.on("before_agent_start", async (event) => {
    if (!planActive) return;

    const originalPrompt = Array.isArray(event?.systemPrompt)
      ? event.systemPrompt
      : [String(event?.systemPrompt || "")];
    const cleanedPrompt = removePonytailInstructions(originalPrompt);
    return { systemPrompt: [...cleanedPrompt, PLAN_INSTRUCTIONS] };
  });
}
