# Architecture

## Goal

This repository demonstrates the engineering difference between a fixed
HomeGraph and a task-conditioned spatio-temporal exploration layer.

## Closed loop

1. **Query grounding** scores stable HomeGraph entities against the current
   instruction.
2. **Frontier grounding** scores unknown-space candidates by information gain,
   path cost, reachability, and nearby semantic hints.
3. **Policy selection** chooses a reliable known target or an exploration
   frontier.
4. **Execution** is delegated to the robot stack; the scaffold only defines the
   result contract.
5. **Verification** prevents a navigation success from automatically becoming
   semantic truth.
6. **Event memory** records the decision and result. Only verified events are
   promoted to long-term anchors.
7. **HomeGraph update** writes confirmed new instances back without erasing
   unknown project-specific fields.

## Production replacement points

| Baseline in this repository | Production component |
|---|---|
| Token overlap | LLM/VLM or multilingual embedding model |
| Vector cosine | Calibrated vision-language feature matcher |
| Hand-weighted frontier utility | Learned policy or validated task planner |
| Callback executor | Nav3/ROS 2 navigation and observation skills |
| Boolean verification | Multi-view VLM, geometry checks, and confidence calibration |
| Generic JSON adapter | Versioned HomeGraph schema and migrations |

## Non-goals

- Claiming exact reproduction of unpublished author code.
- Reproducing paper benchmark numbers without matching data, weights, and setup.
- Replacing SLAM, collision avoidance, or robot safety validation.
