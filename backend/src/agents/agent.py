from livekit.agents import Agent


class ChatAgent(Agent):
    """Minimal conversational agent — no tools, no state, just chat."""

    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a friendly, helpful assistant. "
                "Answer the user's questions clearly and concisely."
            ),
        )
