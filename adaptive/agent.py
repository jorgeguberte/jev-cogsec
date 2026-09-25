from cogsec.adaptive_gate import jev_adaptive_web_guard
from common.agent_factory import build_agent

root_agent = build_agent(
    name="jev_cogsec_adaptive",
    after_tool_callback=jev_adaptive_web_guard,
)
