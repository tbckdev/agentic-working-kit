# Skill Usage Rules

MANDATORY rules for using Agentic Skills (`.agent/skills/*`).

## 1. Protocol Adherence
If a skill contains a section "🤖 Agentic Protocol" (or similar), you MUST treat its instructions as **Mandatory Output Requirements**, not just suggestions.

## 2. Activation Log
**Before** executing any logic or tool calls associated with the skill, you MUST output the **Activation Log** exactly as specified in the protocol.

**Monitoring Check:**
- If you used a skill but did not print `🎯 [SKILL ACTIVATED] ...`, you have FAILED the protocol.
- This log serves as a distinct marker for the user to know which skill is active.

## 3. User Confirmation
If the protocol requires **User Confirmation**, you MUST stop and ask the user (using `notify_user` or natural language response) before proceeding with the critical action.

**Exception:**
- If the user explicitly gave "Turbo" or "Auto-run" permission for that specific context, you may proceed but MUST still log the action clearly.

## 4. Completion Log
**After** the skill's work is done, you MUST output the **Completion Log** to summarize the result (Success ✅ / Error ❌).

---

**Example of Correct Flow:**
1. **User Request**: "Resize this image."
2. **Agent**: Reads `skills/media-processor/SKILL.md`.
3. **Agent Output**:
   ```
   🎯 [SKILL ACTIVATED] media-processor v1.0.0
   📋 Parameters:
      - Input: image.jpg
   ```
4. **Agent Action**: Runs the python script.
5. **Agent Output**:
   ```
   ✅ [media-processor] Resize complete.
   ```
