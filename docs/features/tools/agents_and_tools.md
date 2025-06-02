# Agents and Tools in Labeeb

## Agent Tool Architecture Update (2024)

All agent tools must now inherit from `BaseAgentTool`, defined in `src/labeeb/tools/base_tool.py`, following the project agent-tool separation and naming conventions. The legacy/duplicate `base_tool.py` in `core/ai/tools` has been removed. All imports and usages have been updated for compliance. See the project TODO for ongoing audit of agent tool compliance and documentation.

**Distinction:**
- **Tools**: Atomic, single-purpose, technical operations (see `BaseTool`).
- **Agent Tools**: Agent-facing, orchestratable, and stateful tools for agent workflows (see `BaseAgentTool`).

## Agents
| Name         | Location                                 | Specialty/Role                                                                 |
|--------------|------------------------------------------|-------------------------------------------------------------------------------|
| Agent        | `src/labeeb/core/ai/agent.py`            | Main agentic core: plan/execute loop, workflow orchestration, memory, state   |
| LLMPlanner   | `src/labeeb/core/ai/agent.py`            | (Stub/real) LLM-based planner for decomposing natural language into actions   |
| InformationCollectorAgent | `src/labeeb/core/ai/agents/information_collector.py` | Gathers data from tools (system, web, files) |
| ResearcherAgent          | `src/labeeb/core/ai/agents/researcher.py`            | Plans research, guides collector, writes reports |
| ResearchEvaluatorAgent   | `src/labeeb/core/ai/agents/research_evaluator.py`    | Evaluates research quality, checks completeness |

## Tools
| Name                | Location                                 | Specialty/Role                                                      |
|---------------------|------------------------------------------|---------------------------------------------------------------------|
| EchoTool            | `src/labeeb/core/ai/agent_tools.py`      | Echoes text, basic test tool                                        |
| FileTool            | `src/labeeb/core/ai/agent_tools.py`      | File operations: create, read, write, delete, search, list          |
| SystemResourceTool  | `src/labeeb/core/ai/agent_tools.py`      | Reports CPU, memory, disk, and system resource info                 |
| DateTimeTool        | `src/labeeb/core/ai/agent_tools.py`      | Provides current date and time                                      |
| WeatherTool         | `src/labeeb/core/ai/agent_tools.py`      | (Stub) Returns weather info (to be implemented)                     |
| CalculatorTool      | `src/labeeb/core/ai/agent_tools.py`      | Performs math calculations                                          |
| ToolRegistry        | `src/labeeb/core/ai/agent.py`            | Registers and manages available tools for the agent                 |
| safe_path           | `src/labeeb/core/ai/agent.py`            | Ensures all file outputs are safe and in correct directories        |
| SystemAwarenessTool  | `src/labeeb/core/ai/agent_tools.py`      | Reports mouse, screen, window, and system info                      |
| MouseControlTool     | `src/labeeb/core/ai/agent_tools.py`      | Moves mouse, clicks, drags, scrolls, etc.                           |
| KeyboardInputTool    | `src/labeeb/core/ai/agent_tools.py`      | Types text, presses keys, simulates keyboard input                  |
| BrowserAutomationTool| `src/labeeb/core/ai/agent_tools.py`      | Opens browser, types, clicks, automates web browsing                |
| WebSurfingTool       | `src/labeeb/core/ai/agent_tools.py`      | Automates browsing, clicking, typing, and navigation                |
| WebSearchingTool     | `src/labeeb/core/ai/agent_tools.py`      | Performs web searches and returns results                           |
| FileAndDocumentOrganizerTool | `src/labeeb/core/ai/agent_tools.py` | Organizes files and documents by rules/tags                         |
| CodePathUpdaterTool  | `src/labeeb/core/ai/agent_tools.py`      | Updates code import paths and references                            | 