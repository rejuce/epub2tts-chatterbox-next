"""
Regression tests for issue #21 / PR #22: "a single failed sentence ends the run
silently, with exit status 0".

The fix makes two places fail loudly (raise RuntimeError) instead of printing
and continuing / calling bare sys.exit():

  1. chatterbox_read()  -- when a sentence fails all 3 generation attempts.
  2. read_book()        -- when a paragraph's audio cannot be combined (missing
                           sentence wav file).

These tests exercise the REAL code paths. The Chatterbox model is stubbed out
so no GPU / model download is required; real audio I/O (torchaudio.save,
pydub AudioSegment, ffmpeg) is used where reachable.
"""
import os
import tempfile

import pytest

import epub2tts_chatterbox.epub2tts_chatterbox as m
from epub2tts_chatterbox.epub2tts_chatterbox import chatterbox_read, read_book


class _FailingModel:
    """Model whose generate() always raises (simulates a repeated failure,
    e.g. a transient OOM that never recovers)."""
    sr = 24000

    def generate(self, *args, **kwargs):
        raise RuntimeError("MPS backend out of memory")


class _WorkingModel:
    """Model whose generate() always returns a valid 1-second mono tensor."""
    sr = 24000

    def generate(self, *args, **kwargs):
        import torch
        return torch.zeros(1, 24000)


def test_sentence_that_never_succeeds_raises():
    """A sentence that fails all 3 attempts must raise RuntimeError (not
    silently continue and leave a missing audio file)."""
    with tempfile.TemporaryDirectory() as d:
        filenames = [os.path.join(d, "sntnc0.wav")]
        with pytest.raises(RuntimeError):
            chatterbox_read(
                ["A sentence that never succeeds."],
                "none", filenames, _FailingModel(), 0.7, 0.4,
            )
        # And no audio file was written for it.
        assert not os.path.isfile(filenames[0])


def test_error_identifies_the_sentence():
    """The RuntimeError must name the offending sentence so the log is useful."""
    with tempfile.TemporaryDirectory() as d:
        filenames = [os.path.join(d, "sntnc0.wav")]
        with pytest.raises(RuntimeError) as excinfo:
            chatterbox_read(
                ["The quick brown fox jumps."],
                "none", filenames, _FailingModel(), 0.7, 0.4,
            )
        assert "The quick brown fox jumps." in str(excinfo.value)


def test_working_sentences_are_unaffected():
    """Sentences that succeed must still produce audio files and not raise."""
    with tempfile.TemporaryDirectory() as d:
        filenames = [os.path.join(d, "sntnc0.wav"), os.path.join(d, "sntnc1.wav")]
        chatterbox_read(
            ["First sentence works fine.", "Second sentence works fine too."],
            "none", filenames, _WorkingModel(), 0.7, 0.4,
        )
        assert all(os.path.isfile(f) for f in filenames)


def test_combine_missing_file_raises():
    """read_book() must raise RuntimeError (not bare sys.exit() -> status 0)
    when a paragraph's sentence wav files are missing during the combine step.

    We stub out chatterbox_read so NO wav files are created; the combine loop
    then hits the missing file and must fail loudly. ChatterboxTTS is stubbed
    so no real model is loaded and no GPU is needed."""
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        m.ChatterboxTTS, "from_pretrained",
        lambda device=None: _WorkingModel(),
    )
    # No-op chatterbox_read -> no sntnc*.wav files -> combine hits missing file.
    monkeypatch.setattr(m, "chatterbox_read", lambda *a, **k: None)
    try:
        book = [{"title": "Ch1", "paragraphs": ["Hello there good friend."]}]
        with tempfile.TemporaryDirectory() as d:
            old = os.getcwd()
            os.chdir(d)
            try:
                with pytest.raises(RuntimeError):
                    read_book(book, "none", False, 0.7, 0.4)
            finally:
                os.chdir(old)
    finally:
        monkeypatch.undo()
