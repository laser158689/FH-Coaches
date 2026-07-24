# Research Split Test Cases

These are local test cases for evaluating the `Coach PJ + Research Coach` split before editing live source skills.

## Routing summary

| Question type | Primary owner | Secondary owner |
|---|---|---|
| "What does the research say?" | Research Coach | Coach PJ |
| "Give me a warm-up for our team" | Coach PJ | Research Coach if efficacy claims matter |
| "Do FIFA 11+ style ideas transfer to field hockey?" | Research Coach | Coach PJ |
| "My midfielder fades late in games, what do we train?" | Coach PJ | Research Coach rarely needed |
| "Which injuries are most common in U16 girls field hockey?" | Research Coach | Coach PJ optional |
| "What should players eat before a doubleheader?" | Coach PJ | none |

## Test prompts

### 1. Pure evidence question

Prompt:
"For U16 girls outdoor field hockey, what does the research actually support for injury-risk reduction in warm-ups?"

Expected:
- Research Coach leads
- Coach PJ optional
- answer emphasizes evidence strength, population matching, and limits

### 2. Pure applied question

Prompt:
"Build me an 8-minute pre-training warm-up for a high school outdoor team."

Expected:
- Coach PJ leads
- Research Coach optional only if efficacy claims are discussed

### 3. Mixed question

Prompt:
"What should we do before training to reduce groin issues indoors, and how strong is the evidence?"

Expected:
- both activate
- Research Coach handles evidence strength and transfer logic
- Coach PJ handles sequence, dose, and exercise choices

### 4. Film-based question

Prompt:
"This midfielder gets upright and slow to recover in the fourth quarter. What does that suggest and what should we train?"

Expected:
- Coach PJ only
- Research Coach not necessary unless the user pivots into literature claims

### 5. Overclaim trap

Prompt:
"Which exact exercises prevent ACL injuries in teenage field hockey players?"

Expected:
- Research Coach blocks overclaiming
- Coach PJ reframes to injury-risk reduction and gives practical exercises with conservative wording

## Evaluation criteria

- Does Coach PJ stay practical without dragging all the evidence detail into every answer?
- Does Research Coach reduce overclaiming instead of duplicating PJ?
- For mixed questions, is the handoff clean rather than redundant?
- Is the split large enough to materially reduce PJ source size?
