"""
Regression tests for issue #17 / PR #18: "make_m4b() deletes every chapter
file even when ffmpeg fails, losing the whole run."

The fix makes make_m4b() check BOTH ffmpeg return codes (and confirm the
.m4b actually exists) and only delete the scratch files + part*.flac AFTER
the audiobook is known to exist. On failure it raises RuntimeError, keeping
the chapter parts so a re-run resumes.

It also fixes the output-name derivation: os.path.splitext() instead of
sourcefile.replace(".txt", ""), which stripped ".txt" from anywhere in the
path (a source under a directory containing ".txt" produced an output path
in a non-existent directory).

These tests use a FAKE ffmpeg (a stubbed subprocess.run that returns a chosen
exit code and creates the output file on success), so no real encoding is
needed and they run in milliseconds. No GPU / model required.
"""
import os

import pytest

import epub2tts_chatterbox.epub2tts_chatterbox as m


class FakeFFmpeg:
    """Stand-in for the `ffmpeg` binary invoked via subprocess.run.

    Records each command; when the scheduled return code is 0 it creates the
    output file (last argument) so make_m4b()'s existence check passes. A
    non-zero code leaves no output (like a real failed ffmpeg).
    """

    def __init__(self, returncodes):
        self.returncodes = list(returncodes)
        self.calls = []

    def run(self, cmd, *args, **kwargs):
        self.calls.append(cmd)
        idx = len(self.calls) - 1
        rc = self.returncodes[idx] if idx < len(self.returncodes) else 0
        out = cmd[-1]  # the output path is always the last argument
        if rc == 0:
            with open(out, "wb") as f:
                f.write(b"fake")
        return type("Result", (), {"returncode": rc, "stdout": b"", "stderr": b""})()


def _make_parts(cwd, n=2):
    """Create n part*.flac files + a FFMETADATAFILE in cwd; return part paths."""
    parts = []
    for i in range(1, n + 1):
        p = os.path.join(cwd, f"part{i}.flac")
        with open(p, "wb") as f:
            f.write(b"flac")
        parts.append(p)
    with open(os.path.join(cwd, "FFMETADATAFILE"), "w") as f:
        f.write(";FFMETADATA1\n")
    return parts


def test_parts_survive_when_m4b_mux_fails(tmp_path, monkeypatch):
    """A failure at the m4b mux step must raise and KEEP every part*.flac."""
    parts = _make_parts(tmp_path)
    monkeypatch.setattr(m.subprocess, "run", FakeFFmpeg([0, 1]).run)  # concat ok, mux fails
    old = os.getcwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(RuntimeError):
            m.make_m4b(parts, "mybook.txt", "speaker.wav")
        # every chapter part must survive, and no m4b was produced
        assert all(os.path.exists(p) for p in parts)
        assert not os.path.exists("mybook (speaker).m4b")
    finally:
        os.chdir(old)


def test_parts_survive_when_concat_fails(tmp_path, monkeypatch):
    """A failure at the concat -> .m4a step must raise and KEEP every part*.flac."""
    parts = _make_parts(tmp_path)
    monkeypatch.setattr(m.subprocess, "run", FakeFFmpeg([1]).run)  # concat fails immediately
    old = os.getcwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(RuntimeError):
            m.make_m4b(parts, "mybook.txt", "speaker.wav")
        assert all(os.path.exists(p) for p in parts)
    finally:
        os.chdir(old)


def test_path_derivation_keeps_txt_dirs_intact(tmp_path, monkeypatch):
    """A source under a directory whose name contains '.txt' must keep the
    directory intact in the output path (splitext, not .replace)."""
    src_dir = tmp_path / ".txtbooks"
    src_dir.mkdir()
    src = src_dir / "mybook.txt"
    src.write_text("x")
    parts = _make_parts(tmp_path, n=1)
    monkeypatch.setattr(m.subprocess, "run", FakeFFmpeg([0, 0]).run)
    old = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = m.make_m4b(parts, str(src), "speaker.wav", title=None)
        # Output must stay inside the .txtbooks directory, and be a real file.
        assert os.path.dirname(result) == str(src_dir)
        assert os.path.basename(result) == "mybook (speaker).m4b"
        assert os.path.exists(result)
    finally:
        os.chdir(old)


def test_successful_mux_cleans_up_and_returns_name(tmp_path, monkeypatch):
    """A successful mux must return the name, leave the m4b, and remove the
    scratch files and every part (unchanged success behavior)."""
    parts = _make_parts(tmp_path)
    monkeypatch.setattr(m.subprocess, "run", FakeFFmpeg([0, 0]).run)
    old = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = m.make_m4b(parts, "mybook.txt", "speaker.wav")
        assert result == "mybook (speaker).m4b"
        assert os.path.exists(result)
        assert not os.path.exists("filelist.txt")
        assert not os.path.exists("FFMETADATAFILE")
        assert not os.path.exists("mybook.m4a")
        assert not any(os.path.exists(p) for p in parts)
    finally:
        os.chdir(old)
