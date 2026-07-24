# Research -> PJ Sample Answers

These are local mock examples for testing the orchestrator -> Research -> PJ flow.

## 1. Elite women national-team conditioning

Prompt:
"Let's get a practice/conditioning session built for my women's national team - truly elite field hockey players!"

Expected internal flow:

- Staff: this is PJ-domain, so route to Research first
- Research:
  - population = elite adult women
  - demands = repeated acceleration, braking, COD, repeat sprint, high training density
  - physiology/injury considerations = adductors, calves, hamstrings, lower-limb load, RED-S / recovery vigilance, match congestion
  - evidence = likely mix of field-hockey direct + near-direct + elite practice-based application
  - limits = avoid pretending one exact template is literature-proven
- PJ:
  - session design
  - dose and progression
  - practical load controls

Expected user-facing result:
- one answer
- practical session
- conservative evidence framing

## 2. Warm-up for senior men's league

Prompt:
"What warm-up should our men's senior league team use?"

Expected internal flow:

- Staff -> Research -> PJ
- Research still runs, even though the answer will be simple
- PJ gives the actual sequence

Expected value of the split:
- age / level / session context still get considered
- injury-risk claims stay conservative

## 3. Film fatigue question

Prompt:
"My midfielder gets upright and slow to recover late in games. What does that suggest and what should we train?"

Expected internal flow:

- Research identifies likely demand and risk context
- PJ handles exercise mapping and load design

Expected risk to watch:
- if Research output is too heavy, it slows down a question that is mostly applied

## Evaluation questions

- Does Research meaningfully sharpen the answer before PJ applies it?
- Does the answer still feel like one coach, not two stitched together?
- Is the extra routing worth the cost on straightforward applied questions?
