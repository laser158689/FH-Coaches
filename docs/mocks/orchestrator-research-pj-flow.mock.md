# Orchestrator -> Research -> PJ Flow Mock

This is a local architecture mock only. It does not change deployable source skills.

## Routing rule

For topics historically covered by Coach PJ alone, route in this order:

1. `Field Hockey Coaching Staff` identifies the question as belonging to the physical-preparation lane.
2. `Research Coach` runs first and establishes:
   - population
   - field-hockey demands
   - injury / physiology considerations
   - evidence strength
   - claim boundaries
3. `Strength & Conditioning Coach (Coach PJ)` applies that analysis into:
   - session design
   - warm-up / cool-down structure
   - exercise selection
   - load management
   - fueling / recovery basics

## Trigger scope

This flow should apply to questions about:
- strength and conditioning
- practice conditioning
- warm-ups and cool-downs
- injury-risk reduction
- physical preparation
- fatigue / film-based movement breakdown
- return-to-play loading
- hydration / fueling / recovery / sleep in a performance context

## Why this flow exists

Coach PJ answers should always be evidence-governed, especially when:
- the population matters materially
- injury patterns differ by sex / level / format
- RED-S or female-athlete physiology may matter
- the user is asking for best practice at elite level

## Output model

The user should receive one coordinated answer, not two disconnected mini-answers.

Internal sequence:
- Research Coach frames the evidence and limits.
- Coach PJ gives the practical recommendation.

User-facing sequence:
- disclaimer
- issue
- fix
- result
- optional brief evidence note
- final attribution line

## Failure mode to avoid

Do not let Coach PJ answer first and Research Coach merely audit afterward. The whole point is that Research Coach constrains the applied answer before PJ prescribes.
