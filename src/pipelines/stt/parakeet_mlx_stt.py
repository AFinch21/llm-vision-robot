from __future__ import annotations

import logging
import time
import platform
from typing import Literal
import tempfile
import wave

import numpy as np
from faster_whisper import WhisperModel
from mlx_audio.stt.generate import generate_transcription
from mlx_audio.stt.utils import load_model


from livekit.agents import stt, APIConnectOptions, utils
from livekit.agents.types import NOT_GIVEN, NotGivenOr

__all__ = ["ParakeetMLX"]

logger = logging.getLogger(__name__)

class ParakeetMLX(stt.STT):
    """
    Parakeet TDT 0.6B v3 STT plugin using MLX Audio.

    Args:
        model: The model to use.
            Options: "mlx-community/parakeet-tdt-0.6b-v3"
            Recommended: "mlx-community/parakeet-tdt-0.6b-v3"
    """

    def __init__(
        self,
        model: str = "mlx-community/parakeet-tdt-0.6b-v3",
    ) -> None:
        super().__init__(
            capabilities=stt.STTCapabilities(
                streaming=False,
                interim_results=False
            )
        )
        self._model = load_model(model)

        logger.info(f"Loading Parakeet model: {model}")

        logger.info(f"Parakeet ready")

    async def _recognize_impl(
        self,
        buffer: utils.AudioBuffer,
        *,
        language: NotGivenOr[str] = NOT_GIVEN,
        conn_options: APIConnectOptions
    ) -> stt.SpeechEvent:
        """
        Process audio buffer and return transcription.

        Handles both single AudioFrame and lists of AudioFrames from LiveKit.
        Audio is normalized to float32 [-1, 1] range for Parakeet processing.
        """
        # Convert AudioBuffer to numpy array
        if isinstance(buffer, list):
            all_data = []
            for frame in buffer:
                frame_data = np.frombuffer(frame.data, dtype=np.int16)
                all_data.append(frame_data)
            audio_data = np.concatenate(all_data).astype(np.float32) / 32768.0
        else:
            audio_data = np.frombuffer(buffer.data, dtype=np.int16).astype(np.float32) / 32768.0

        # pick a sample rate from the frames
        if isinstance(buffer, list):
            sample_rate = buffer[0].sample_rate
        else:
            sample_rate = buffer.sample_rate

        # convert float32 [-1, 1] to int16 PCM
        pcm16 = np.clip(audio_data, -1.0, 1.0)
        pcm16 = (pcm16 * 32767.0).astype(np.int16)

        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            with wave.open(tmp.name, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(pcm16.tobytes())

            result = self._model.generate(tmp.name)

        return stt.SpeechEvent(
            type=stt.SpeechEventType.FINAL_TRANSCRIPT,
            alternatives=[stt.SpeechData(
                text=result.text,
                start_time=0,
                end_time=0,
                language="en"
            )],
        )