import os
from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, function_tool, room_io, RunContext
from livekit.plugins import silero
# from livekit.plugins.turn_detector.multilingual import MultilingualModel

from livekit.plugins import openai as lk_openai
from livekit.plugins import silero

from src.agents.robot import Robot
from src.pipelines.stt.whisper_stt import FasterWhisperSTT
from src.pipelines.stt.parakeet_mlx_stt import ParakeetMLX
from src.pipelines.stt.whisper_mlx_stt import WhisperMLX
from src.pipelines.tts.piper_tts import PiperTTS

load_dotenv(".env")

print("OLLAMA_HOST=", os.getenv("OLLAMA_HOST"))
print("OLLAMA_BASE_URL=", os.getenv("OLLAMA_BASE_URL"))
print("OPENAI_BASE_URL=", os.getenv("OPENAI_BASE_URL"))

# --- Local STT (FasterWhisper) ------------------
device = "cuda" if os.getenv("USE_CUDA") == "1" else "cpu"
# On CPU backends (common on macOS), float16 is not supported/efficient in ctranslate2.
compute_type = "float16" if device == "cuda" else "int8"
# stt = FasterWhisperSTT(
#     model_size="medium",      # tiny, base, small, medium, large-v3
#     device=device,
#     compute_type=compute_type,   # quantization strategy for faster inference
# )
stt = ParakeetMLX(model="mlx-community/parakeet-tdt-0.6b-v3")

# stt = WhisperMLX(model="mlx-community/whisper-large-v3-turbo-asr-fp16")

# --- Local TTS (Piper) -------------------------
# Put path to your downloaded Piper ONNX model here:
piper_model = "/Users/andrewfinch/Projects/local_models/piper/en_US-ryan-high.onnx"
tts = PiperTTS(
    model_path=piper_model,
    use_cuda=False,           # use CPU for Piper if CUDA issues
    speed=1.0,
)

# --- Local LLM Endpoint (Ollama) ----------------
# This will call Ollama as if it were an OpenAI API server
# llm = lk_openai.LLM.with_ollama(
#     model="qwen3-vl:8b"
# )

llm = lk_openai.LLM.with_ollama(
    model="llama3.1:8b"
)

# # --- VAD (optional) -----------------------------
vad = silero.VAD.load()


# --- Set up the LiveKit AgentSession -----------
server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=vad,
        # turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Robot(),
        # room_options=room_io.RoomOptions(
        #     audio_input=room_io.AudioInputOptions(
        #         noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
        #     ),
        # ),
    )

if __name__ == "__main__":
    agents.cli.run_app(server)
