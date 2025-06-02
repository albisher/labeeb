#!/usr/bin/env python3
"""
AI-driven command interpreter for Labeeb.
This module replaces regex-based pattern matching with AI-driven command interpretation.
"""
import logging
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import json
from dataclasses import dataclass, field
from datetime import datetime
import inspect

from labeeb.core.logging_config import get_logger
from labeeb.core.file_operations import handle_file_operation
from labeeb.core.ai.tools.json_tool import JSONTool
from labeeb.core.ai.tools.tool_registry import ToolRegistry
import re
from labeeb.tools.sound_tool import SoundTool
from labeeb.tools.weather.weather import WeatherPlugin

logger = get_logger(__name__)


@dataclass
class CommandHistoryEntry:
    """Data class for storing command history entries."""

    command: str
    language: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PlanStep:
    """Data class for storing plan steps."""

    step: int
    description: str
    operation: str
    parameters: Dict[str, Any]
    confidence: float
    condition: Optional[str] = None
    on_success: List[int] = field(default_factory=list)
    on_failure: List[int] = field(default_factory=list)
    explanation: Optional[str] = None


@dataclass
class InterpretedCommand:
    """Data class for storing interpreted commands."""

    plan: List[PlanStep]
    overall_confidence: float
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    language: str = "en"


@dataclass
class StepResult:
    """Data class for storing step execution results."""

    step: int
    description: str
    status: str
    output: Optional[Any] = None
    error: Optional[str] = None


class AICommandInterpreter:
    """AI-driven command interpreter for natural language processing."""

    def __init__(self) -> None:
        """Initialize the AI command interpreter."""
        self.command_history: List[CommandHistoryEntry] = []
        self.context: Dict[str, Any] = {}
        self.json_tool = JSONTool()
        self.weather_plugin = None
        try:
            # Try to load weather plugin with config if available
            from labeeb.core.config_manager import ConfigManager
            config = ConfigManager().get("weather", {})
            self.weather_plugin = WeatherPlugin(api_key=config.get("api_key"))
        except Exception:
            pass
        self.sound_tool = SoundTool()

    def interpret_command(self, command: str, language: str = "en") -> InterpretedCommand:
        """
        Interpret a natural language command using AI.

        Args:
            command: The natural language command
            language: The language of the command ('en' or 'ar')

        Returns:
            InterpretedCommand containing the interpreted command details
        """
        # Detect Arabic if present
        if any("\u0600" <= c <= "\u06ff" for c in command):
            language = "ar"

        # --- Intent mapping ---
        plan = []
        cmd = command.strip().lower()
        step = 1
        # Weather (English/Arabic)
        weather_patterns = [
            r"weather in ([\w\s]+)",
            r"ما هو الطقس في ([^؟]+)",
            r"ما هو الطقس ب([\w\s]+)",
            r"ما هو الطقس الآن",
        ]
        match = None
        for pat in weather_patterns:
            m = re.search(pat, cmd)
            if m:
                match = m
                break
        if match:
            city = match.group(1).strip() if match.lastindex else ""
            if not city:
                city = "الكويت" if "الكويت" in cmd else "your city"
            plan.append(PlanStep(
                step=step,
                description=f"Get current weather for {city}",
                operation="weather_tool.get_weather_data",
                parameters={"city": city},
                confidence=0.99,
                explanation="Fetches current weather using the weather tool."
            ))
        # Screenshot (English/Arabic)
        elif any(x in cmd for x in ["screenshot", "لقطة شاشة", "خذ لقطة"]):
            plan.append(PlanStep(
                step=step,
                description="Take a screenshot of the desktop",
                operation="screen_control.take_screenshot",
                parameters={},
                confidence=0.99,
                explanation="Takes a screenshot using the screen control tool."
            ))
        # Calculator (English/Arabic)
        elif any(x in cmd for x in ["calculate", "احسب", "حاسبة", "اجمع", "اضرب", "اطرح", "اقسم"]):
            expr = re.findall(r"\d+[\s\+\-\*/xX×÷]+\d+", cmd)
            expression = expr[0] if expr else cmd
            plan.append(PlanStep(
                step=step,
                description=f"Calculate expression: {expression}",
                operation="calculator.calculate",
                parameters={"expression": expression},
                confidence=0.98,
                explanation="Performs calculation using the calculator tool."
            ))
        # Clipboard (copy text)
        elif any(x in cmd for x in ["copy the text", "انسخ النص"]):
            text = re.findall(r"copy the text (.+)", cmd)
            text = text[0] if text else re.findall(r"انسخ النص (.+)", cmd)
            text = text[0] if text else ""
            plan.append(PlanStep(
                step=step,
                description=f"Copy text to clipboard: {text}",
                operation="clipboard_tool.set_text",
                parameters={"text": text},
                confidence=0.97,
                explanation="Copies text to clipboard using the clipboard tool."
            ))
        # Play sound/audio
        elif any(x in cmd for x in ["play the file", "شغل الملف"]):
            fname = re.findall(r"play the file ([\w\.]+)", cmd)
            fname = fname[0] if fname else re.findall(r"شغل الملف ([\w\.]+)", cmd)
            fname = fname[0] if fname else "music.wav"
            plan.append(PlanStep(
                step=step,
                description=f"Play sound file: {fname}",
                operation="sound_tool.play_sound",
                parameters={"filename": fname},
                confidence=0.97,
                explanation="Plays a sound file using the sound tool."
            ))
        # Web search/news
        elif any(x in cmd for x in ["search the web", "ابحث في الإنترنت"]):
            query = re.findall(r"search the web for (.+)", cmd)
            query = query[0] if query else re.findall(r"ابحث في الإنترنت عن (.+)", cmd)
            query = query[0] if query else "AI news"
            plan.append(PlanStep(
                step=step,
                description=f"Search the web for: {query}",
                operation="WebTool.search_web",
                parameters={"query": query},
                confidence=0.97,
                explanation="Performs a web search using the web tool."
            ))
        # Fallback: echo
        else:
            plan.append(PlanStep(
                step=step,
                description="Echo the command (fallback)",
                operation="echo",
                parameters={"text": command},
                confidence=0.5,
                explanation="Fallback: just echo the command."
            ))

        self.command_history.append(CommandHistoryEntry(command=command, language=language))
        return InterpretedCommand(plan=plan, overall_confidence=0.96, language=language)

    async def process_plan_async(self, plan: List[PlanStep]) -> List[StepResult]:
        """
        Async version: Process and execute each step in the plan.
        """
        results: List[StepResult] = []
        step_results: Dict[int, StepResult] = {}

        for step in plan:
            result = StepResult(step=step.step, description=step.description, status="skipped")
            try:
                # Parse operation as tool_name.method
                if "." in step.operation:
                    tool_name, method = step.operation.split(".", 1)
                    # Special bridging for weather and sound tools
                    if tool_name == "weather_tool":
                        if self.weather_plugin and hasattr(self.weather_plugin, "get_current_weather"):
                            output = self.weather_plugin.get_current_weather(**step.parameters)
                            result.status = "success"
                            result.output = output
                        else:
                            result.status = "error"
                            result.error = "Weather plugin not available."
                    elif tool_name == "sound_tool":
                        if hasattr(self.sound_tool, method):
                            func = getattr(self.sound_tool, method)
                            output = func(**step.parameters)
                            result.status = "success"
                            result.output = output
                        else:
                            result.status = "error"
                            result.error = f"Method '{method}' not found in SoundTool."
                    else:
                        ToolClass = ToolRegistry.get_tool(tool_name)
                        if ToolClass is None:
                            result.status = "error"
                            result.error = f"Tool '{tool_name}' not found."
                        else:
                            tool = ToolClass()
                            if hasattr(tool, method):
                                func = getattr(tool, method)
                                if inspect.iscoroutinefunction(func):
                                    output = await func(**step.parameters)
                                else:
                                    output = func(**step.parameters)
                                result.status = "success"
                                result.output = output
                            else:
                                # Try .execute or ._execute_command fallback
                                if hasattr(tool, "execute"):
                                    exec_func = getattr(tool, "execute")
                                    if inspect.iscoroutinefunction(exec_func):
                                        output = await exec_func(method, step.parameters)
                                    else:
                                        output = exec_func(method, step.parameters)
                                    result.status = "success"
                                    result.output = output
                                elif hasattr(tool, "_execute_command"):
                                    exec_func = getattr(tool, "_execute_command")
                                    if inspect.iscoroutinefunction(exec_func):
                                        output = await exec_func(method, step.parameters)
                                    else:
                                        output = exec_func(method, step.parameters)
                                    result.status = "success"
                                    result.output = output
                                else:
                                    result.status = "error"
                                    result.error = f"Method '{method}' not found in tool '{tool_name}'."
                elif step.operation == "echo":
                    result.status = "success"
                    result.output = step.parameters.get("text")
                else:
                    result.status = "unknown_operation"
                    result.output = f"Unknown operation: {step.operation}"
            except Exception as e:
                result.status = "error"
                result.error = str(e)
            results.append(result)
            step_results[step.step] = result
        return results

    def process_plan(self, plan: List[PlanStep]) -> List[StepResult]:
        """
        Sync wrapper for async plan processing (for legacy compatibility).
        """
        import asyncio
        return asyncio.get_event_loop().run_until_complete(self.process_plan_async(plan))

    def process_command(self, command: str, language: str = "en") -> str:
        """
        Process a natural language command using the new plan-based structure.

        Args:
            command: The natural language command
            language: The language of the command ('en' or 'ar')

        Returns:
            Response message summarizing execution
        """
        try:
            # Detect Arabic if present
            if any("\u0600" <= c <= "\u06ff" for c in command):
                language = "ar"
            # Interpret the command using AI (plan-based)
            interpreted = self.interpret_command(command, language)

            # Process the plan
            results = self.process_plan(interpreted.plan)

            # Summarize results
            summary = []
            for res in results:
                summary.append(f"Step {res.step}: {res.description} - {res.status}")
                if res.error:
                    summary.append(f"  Error: {res.error}")

            return "\n".join(summary)
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return f"Error processing command: {str(e)}"

    def get_command_history(self) -> List[CommandHistoryEntry]:
        """Get the command history."""
        return self.command_history

    def clear_context(self) -> None:
        """Clear the current context."""
        self.context = {}

    def save_context(self, filepath: Optional[Path] = None) -> None:
        """
        Save the current context to a file.

        Args:
            filepath: Path to save the context file
        """
        if filepath is None:
            filepath = Path("context.json")

        with open(filepath, "w") as f:
            f.write(self.json_tool.dump(self.context, pretty=True))

    def load_context(self, filepath: Optional[Path] = None) -> None:
        """
        Load context from a file.

        Args:
            filepath: Path to load the context file from
        """
        if filepath is None:
            filepath = Path("context.json")

        if filepath.exists():
            with open(filepath, "r") as f:
                self.context = self.json_tool.load(f.read())
