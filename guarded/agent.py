from cogsec.jev_gate import jev_web_guard
from common.agent_factory import build_agent

root_agent = build_agent(
    name="jev_cogsec_guarded",
    after_tool_callback=jev_web_guard,
)
