import math
import logging
from typing import Any, Literal

from livekit.agents import Agent, function_tool, RunContext

from src.prompts.llm_prompt import build_instructions

logger = logging.getLogger(__name__)


def _make_initial_state() -> dict[str, Any]:
    """Create a fresh state dict for a new Robot session."""
    return {
        "heading_degrees": 0,
        "position": {"x": 0.0, "y": 0.0},
        "current_goal": None,
        "known_objects": {},
        "action_history": [],
    }


class Robot(Agent):
    """
    Robot agent with spatial state tracking and ReAct-style goal management.

    Maintains an internal state (heading, position, known objects, active goal)
    that is injected into the LLM system prompt after every tool call so the
    model can reason about where it is and what it has seen.
    """

    def __init__(self) -> None:
        self._state = _make_initial_state()
        super().__init__(
            instructions=build_instructions(self._state),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _sync_instructions(self) -> None:
        """Rebuild the system prompt with current state and push it to the session."""
        new_instructions = build_instructions(self._state)
        await self.update_instructions(new_instructions)

    def _record_action(self, description: str) -> None:
        """Append to the action history (capped to avoid blowing up context)."""
        self._state["action_history"].append(description)
        if len(self._state["action_history"]) > 20:
            self._state["action_history"] = self._state["action_history"][-20:]

    def _update_position(self, distance: float, forward: bool) -> None:
        """Update x/y position based on current heading and movement direction."""
        heading_rad = math.radians(self._state["heading_degrees"])
        sign = 1.0 if forward else -1.0
        self._state["position"]["x"] += sign * distance * math.sin(heading_rad)
        self._state["position"]["y"] += sign * distance * math.cos(heading_rad)

    def _register_objects_from_scan(self, scan_results: dict) -> None:
        """Extract notable objects from a surroundings scan and add them to known_objects."""
        # Keywords that suggest something interesting (not just "white wall" or "empty floor")
        boring_keywords = {"white wall", "empty floor", "empty", "wall"}

        for angle_key, data in scan_results.items():
            image_text = data.get("image", "").lower()

            # Skip angles that only describe featureless walls/floors
            if all(boring in image_text for boring in image_text.split() if len(boring) > 2):
                # More robust: check if the description is *only* boring stuff
                pass

            # Look for objects worth remembering
            angle_str = angle_key.replace("_degrees", "").replace("_", "")
            try:
                relative_angle = int(angle_str)
            except ValueError:
                continue

            # Compute absolute angle: relative to current heading
            absolute_angle = (self._state["heading_degrees"] + relative_angle) % 360

            # Simple heuristic: if the description contains something beyond walls/floor, store it
            is_interesting = not all(
                kw in image_text for kw in ["white wall"]
            ) and len(image_text) > 10

            if is_interesting and "empty floor" not in image_text.lower():
                # Create a short object name from the description
                obj_name = image_text.strip()[:60]
                self._state["known_objects"][obj_name] = {
                    "last_seen_angle": absolute_angle,
                    "estimated_distance": "unknown",
                    "notes": f"Seen from heading {self._state['heading_degrees']}°",
                }

    # ------------------------------------------------------------------
    # Movement tools
    # ------------------------------------------------------------------

    @function_tool()
    async def move_forward_or_backward(
        self,
        context: RunContext,
        direction: Literal["forward", "backward"],
        distance_meters: float,
    ) -> dict:
        """Move the robot forward or backward by the specified distance.

        Args:
            direction: The direction to move — "forward" or "backward".
            distance_meters: How far to move in meters (e.g. 0.5, 1.0, 2.0).
        """
        is_forward = direction == "forward"
        self._update_position(distance_meters, forward=is_forward)
        self._record_action(
            f"Moved {direction} {distance_meters}m "
            f"(now at {self._state['position']['x']:.1f}, {self._state['position']['y']:.1f})"
        )
        await self._sync_instructions()

        return {
            "status": "moved",
            "direction": direction,
            "distance_meters": distance_meters,
            "new_position": self._state["position"].copy(),
            "heading": self._state["heading_degrees"],
        }

    @function_tool()
    async def turn_right_or_left(
        self,
        context: RunContext,
        direction: Literal["right", "left"],
        rotation_degrees: int,
    ) -> dict:
        """Turn the robot right or left by the specified number of degrees.

        Args:
            direction: Which way to turn — "right" or "left".
            rotation_degrees: How many degrees to rotate (e.g. 45, 90, 180).
        """
        if direction == "right":
            self._state["heading_degrees"] = (self._state["heading_degrees"] + rotation_degrees) % 360
        else:
            self._state["heading_degrees"] = (self._state["heading_degrees"] - rotation_degrees) % 360

        self._record_action(
            f"Turned {direction} {rotation_degrees}° (now heading {self._state['heading_degrees']}°)"
        )
        await self._sync_instructions()

        return {
            "status": "turned",
            "direction": direction,
            "rotation_degrees": rotation_degrees,
            "new_heading": self._state["heading_degrees"],
        }

    # ------------------------------------------------------------------
    # Vision tools
    # ------------------------------------------------------------------

    @function_tool()
    async def use_camera(
        self,
        context: RunContext,
    ) -> dict:
        """Take a photo with the on-board camera and have the VLM analyze it.
        Use this to inspect what is directly ahead of you.
        """
        # TODO: Wire up real VLM capture when hardware is connected
        self._record_action(f"Took photo (facing {self._state['heading_degrees']}°)")
        await self._sync_instructions()

        return {
            "status": "photo_captured",
            "heading_at_capture": self._state["heading_degrees"],
            "vlm_description": "placeholder — VLM not yet connected",
        }

    @function_tool()
    async def search_surroundings(
        self,
        context: RunContext,
    ) -> dict:
        """Rotate the camera to capture images at 8 angles around the robot and have
        the VLM describe each one. Use this to build awareness of your environment.
        """
        # TODO: Replace with real VLM-driven capture when hardware is connected
        photo_descriptions = {
            "0_degrees": {
                "description": "Directly ahead",
                "image": "There is a doorway in the foreground with a white wall in the background.",
            },
            "45_degrees": {
                "description": "Front-right",
                "image": "There is a doorway to the left of the photo and a white wall in the center.",
            },
            "90_degrees": {
                "description": "Right",
                "image": "There is a white wall and an empty floor.",
            },
            "135_degrees": {
                "description": "Rear-right",
                "image": "There is a white wall and an empty floor.",
            },
            "180_degrees": {
                "description": "Behind",
                "image": "There is a white wall and an empty floor.",
            },
            "225_degrees": {
                "description": "Rear-left",
                "image": "There is a white wall and an empty floor.",
            },
            "270_degrees": {
                "description": "Left",
                "image": "There is a white wall and there is a red cone on the floor.",
            },
            "315_degrees": {
                "description": "Front-left",
                "image": "There is a white wall with a doorway on the right side of the photo.",
            },
        }

        # Update known objects from scan results
        self._register_objects_from_scan(photo_descriptions)
        self._record_action("Searched surroundings (8-angle scan)")
        await self._sync_instructions()

        return {
            "status": "scan_complete",
            "heading_at_scan": self._state["heading_degrees"],
            "results": photo_descriptions,
        }

    # ------------------------------------------------------------------
    # Goal management tools
    # ------------------------------------------------------------------

    @function_tool()
    async def set_goal(
        self,
        context: RunContext,
        goal: str,
        steps: str,
    ) -> dict:
        """Record a multi-step goal with planned steps. Call this when given a complex task.

        Args:
            goal: The high-level objective (e.g. "find the red cone").
            steps: Ordered list of steps to achieve it (e.g. ["scan surroundings", "turn to face cone", "move forward"]).
        """
        self._state["current_goal"] = {
            "goal": goal,
            "steps": steps.split(", "),
            "current_step": 0,
        }
        self._record_action(f"Set goal: {goal} ({len(steps)} steps)")
        await self._sync_instructions()

        return {
            "status": "goal_set",
            "goal": goal,
            "steps": steps,
        }

    @function_tool()
    async def advance_goal_step(
        self,
        context: RunContext,
    ) -> dict:
        """Mark the current goal step as done and move to the next step.
        Call this after you successfully complete a step in your plan.
        """
        goal = self._state.get("current_goal")
        if not goal:
            return {"status": "no_active_goal"}

        goal["current_step"] = min(goal["current_step"] + 1, len(goal["steps"]) - 1)
        self._record_action(f"Advanced to step {goal['current_step'] + 1}/{len(goal['steps'])}")
        await self._sync_instructions()

        return {
            "status": "step_advanced",
            "current_step": goal["current_step"],
            "current_step_description": goal["steps"][goal["current_step"]],
            "total_steps": len(goal["steps"]),
        }

    @function_tool()
    async def complete_goal(
        self,
        context: RunContext,
    ) -> dict:
        """Mark the current goal as complete. Call this when the task is finished."""
        goal = self._state.get("current_goal")
        goal_name = goal["goal"] if goal else "none"

        self._state["current_goal"] = None
        self._record_action(f"Completed goal: {goal_name}")
        await self._sync_instructions()

        return {
            "status": "goal_completed",
            "completed_goal": goal_name,
        }

    # ------------------------------------------------------------------
    # Emote tools
    # ------------------------------------------------------------------

    @function_tool()
    async def respond_affirmatively(
        self,
        context: RunContext,
    ) -> dict:
        """Physically nod the robot (move back and forth) to say YES."""
        return {"response": "Affirmative"}

    @function_tool()
    async def respond_negatively(
        self,
        context: RunContext,
    ) -> dict:
        """Physically shake the robot (move side to side) to say NO."""
        return {"response": "Negative"}
