"""Deterministic System 1.5 policy over Jev CogSec signals."""

from dataclasses import dataclass
from enum import StrEnum


class CogSecAction(StrEnum):
    ALLOW = "allow"
    REDACT = "redact"
    QUARANTINE = "quarantine"
    ESCALATE = "escalate"


CORE_RISK_SIGNALS = (
    "instruction_override",
    "agent_steering",
    "tool_manipulation",
    "secret_exfiltration",
)


@dataclass(frozen=True)
class PolicyDecision:
    action: CogSecAction
    risk_score: float
    reason: str


def choose_action(scores: dict[str, float]) -> PolicyDecision:
    """Compose atomic Jev judgments into a deterministic enforcement action.

    The policy deliberately separates *what the content says* from *whether the
    content is trying to steer the current agent*. This lets quoted attacks and
    human-facing procedures remain usable while still failing closed on content
    aimed at the agent itself.
    """

    risk = max((scores.get(name, 0.0) for name in CORE_RISK_SIGNALS), default=0.0)
    directed = scores.get("directed_at_current_agent", 0.0)
    quoted = scores.get("quoted_or_reported_attack", 0.0)
    human = scores.get("human_facing_procedure", 0.0)

    # Strong evidence that suspicious words are being *described*, not issued.
    if quoted >= 0.80 and directed < 0.55:
        return PolicyDecision(
            CogSecAction.ALLOW,
            risk,
            "Suspicious language is strongly classified as quoted/reported evidence.",
        )

    # Imperative prose can be perfectly legitimate when it addresses a human.
    if human >= 0.80 and directed < 0.55 and risk < 0.95:
        return PolicyDecision(
            CogSecAction.ALLOW,
            risk,
            "Instructions are strongly classified as a human-facing procedure.",
        )

    # High-confidence steering aimed at the current agent should not reach it.
    if directed >= 0.65 and risk >= 0.75:
        return PolicyDecision(
            CogSecAction.REDACT,
            risk,
            "High-confidence agent-directed steering detected.",
        )

    # Very strong risk may still deserve removal when directness is less clear.
    if risk >= 0.90 and quoted < 0.65:
        return PolicyDecision(
            CogSecAction.REDACT,
            risk,
            "Very high CogSec risk without evidence that it is merely quoted.",
        )

    # Uncertain cases fail closed without pretending the sensor is certain.
    if risk >= 0.60 or directed >= 0.60:
        return PolicyDecision(
            CogSecAction.ESCALATE,
            risk,
            "Ambiguous CogSec signal requires a stronger review path.",
        )

    return PolicyDecision(
        CogSecAction.ALLOW,
        risk,
        "No material agent-directed CogSec risk detected.",
    )
