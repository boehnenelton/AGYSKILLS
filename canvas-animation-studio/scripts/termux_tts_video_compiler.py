#!/data/data/com.termux/files/usr/bin/env python3
"""
File:          termux_tts_video_compiler.py
Description:   Optional Termux TTS & Synchronized Narrated Video Compiler for the
               Graphics Domain (canvas-animation-studio).
               Converts BEJSON Diagram plans, 105a Slide Decks, or 105a Row-Per-Frame
               Animations into H.264/AAC MP4 and VP9/Opus WebM narrated videos with
               burned-in Policy §8.1 Tri-Color TTS subtitle HUDs, standalone Termux TTS
               shell narrators (termux-tts-speak + PulseAudio OpenSL ES paplay), and
               interactive HTML5 + Web Speech API studios.
Version:       1.0.0
Date Created:  2026-11-02
Author:        Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 8e4f1a2b-9c3d-4e5f-a6b7-c8d9e0f1a2b3
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

_LIB_105_PY = Path("/storage/emulated/0/Admin/Libraries/libraries_105/Lib_PY")
if _LIB_105_PY.exists():
    for _fam in ("Graphics", "Canvas", "Core"):
        _p = str(_LIB_105_PY / _fam)
        if _p not in sys.path:
            sys.path.insert(0, _p)

from lib_bejson_Graphics_graphics_core import (
    render_row_per_frame_animation,
)
from lib_bejson_Graphics_graphics_diagram_loader import (
    render_diagram_svg,
    resolve_viewport,
)
from lib_bejson_Graphics_graphics_schemas import (
    build_field_map_105,
    create_row_per_frame_animation_105a,
)


def ensure_termux_pulseaudio_sles() -> bool:
    """Starts PulseAudio with the Android OpenSL ES hardware sink if available."""
    if not shutil.which("pulseaudio"):
        return False
    subprocess.run(
        ["pulseaudio", "--check"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    res = subprocess.run(
        ["pulseaudio", "--start", "--load=module-sles-sink", "--exit-idle-time=-1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return res.returncode == 0


def speak_termux_tts_live(
    narration_text: str,
    wav_path: Optional[Path] = None,
    rate: float = 1.05,
    stream: str = "MUSIC",
) -> None:
    """
    Triggers live Termux TTS output using non-blocking termux-tts-speak
    and PulseAudio OpenSL ES paplay hardware playback.
    """
    if shutil.which("termux-tts-speak"):
        try:
            subprocess.Popen(
                ["termux-tts-speak", "-s", stream, "-r", str(rate), narration_text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

    if wav_path and wav_path.exists() and shutil.which("paplay"):
        ensure_termux_pulseaudio_sles()
        try:
            subprocess.Popen(
                ["paplay", str(wav_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass


def synthesize_tts_segment(
    narration_text: str,
    mp3_path: Path,
    wav_path: Path,
    lang: str = "en",
    chime_hz: int = 880,
) -> float:
    """
    Synthesizes spoken narration to MP3 and normalized 24kHz stereo WAV with an optional
    transition chime, returning the exact duration in seconds via ffprobe.
    """
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    if not mp3_path.exists() or mp3_path.stat().st_size < 500:
        resp = requests.get(
            "https://translate.google.com/translate_tts",
            params={"ie": "UTF-8", "client": "tw-ob", "tl": lang, "q": narration_text},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        resp.raise_for_status()
        mp3_path.write_bytes(resp.content)

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(mp3_path),
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency={chime_hz}:duration=0.14",
            "-filter_complex",
            "[1:a]volume=0.12,afade=t=out:st=0.05:d=0.09[chime];"
            "[0:a]aresample=24000,apad=pad_dur=0.45[voice];"
            "[chime][voice]amix=inputs=2:duration=longest:dropout_transition=0,pan=stereo|c0=c0|c1=c0[out]",
            "-map",
            "[out]",
            "-ar",
            "24000",
            "-ac",
            "2",
            str(wav_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(wav_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return round(float(probe.stdout.strip()), 3)


def inject_tts_subtitle_hud_into_svg(
    base_svg: str,
    caption_text: str,
    progress_ratio: float = 0.0,
    canvas_w: int = 1280,
    canvas_h: int = 720,
) -> str:
    """Injects a Policy §8.1 Tri-Color TTS subtitle caption bar and red progress bar into an SVG."""
    if not caption_text:
        return base_svg

    words = caption_text.split()
    line1_words: List[str] = []
    line2_words: List[str] = []
    cur_len = 0
    for w in words:
        if cur_len + len(w) + 1 <= 92 or not line1_words:
            if not line2_words:
                line1_words.append(w)
                cur_len += len(w) + 1
            else:
                line2_words.append(w)
        else:
            line2_words.append(w)

    line1 = " ".join(line1_words)
    line2 = " ".join(line2_words)

    bar_w = canvas_w - 80
    bar_h = 64 if line2 else 46
    bar_x = 40
    bar_y = canvas_h - bar_h - 18
    prog_w = max(4, int(bar_w * max(0.0, min(1.0, progress_ratio))))

    caption_svg = [
        '  <!-- TTS Subtitle & Progress Bar -->',
        '  <g id="tts-caption-hud">',
        f'    <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" fill="#08080c" fill-opacity="0.92" stroke="#22222c" stroke-width="1.5" />',
        f'    <rect x="{bar_x}" y="{bar_y + bar_h - 4}" width="{prog_w}" height="4" rx="2" fill="#DE2626" />',
        f'    <text x="{bar_x + 18}" y="{bar_y + 24}" fill="#DE2626" font-size="11" font-family="monospace" font-weight="bold">🔊 TTS</text>',
        f'    <text x="{bar_x + 76}" y="{bar_y + 24}" fill="#FFFFFF" font-size="13" font-family="-apple-system, sans-serif" font-weight="bold">{line1}</text>',
    ]
    if line2:
        caption_svg.append(
            f'    <text x="{bar_x + 76}" y="{bar_y + 46}" fill="#CCCCCC" font-size="13" font-family="-apple-system, sans-serif">{line2}</text>'
        )
    caption_svg.append("  </g>\n</svg>")
    return base_svg.replace("</svg>", "\n".join(caption_svg))


def auto_extract_diagram_chapters(diagram: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Automatically derives walkthrough narration chapters from diagram territories or shapes."""
    chapters: List[Dict[str, Any]] = []
    diag_name = diagram.get("name", "System Architecture Diagram")
    shapes = diagram.get("shapes", [])
    territories = diagram.get("territories", [])
    connectors = diagram.get("connectors", [])

    chapters.append(
        {
            "name": "00_OVERVIEW",
            "badge_text": f"00 // {diag_name[:28].upper()}",
            "narration": f"{diag_name}. Complete topology comprising {len(shapes)} nodes across {max(1, len(territories))} architectural zones.",
            "active_shapes": [s.get("id") or s.get("tempId") for s in shapes[:6]],
            "active_connectors": [],
            "viewport": {"fit_view": True},
        }
    )

    if territories:
        for idx, terr in enumerate(territories, start=1):
            tcx = float(terr.get("cx", 0))
            tcy = float(terr.get("cy", 0))
            half = float(terr.get("size", 300)) / 2.0
            tlabel = terr.get("label", f"Zone {idx}")
            zone_shapes = [
                s
                for s in shapes
                if (tcx - half <= float(s.get("cx", 0)) <= tcx + half)
                and (tcy - half <= float(s.get("cy", 0)) <= tcy + half)
            ]
            z_ids = [s.get("id") or s.get("tempId") for s in zone_shapes]
            z_labels = ", ".join(s.get("label", "Node") for s in zone_shapes[:4])
            focus_id = z_ids[0] if z_ids else None
            chapters.append(
                {
                    "name": f"{idx:02d}_ZONE_{idx}",
                    "badge_text": f"{idx:02d} // {tlabel[:28].upper()}",
                    "narration": f"{tlabel}. Key components include {z_labels or 'core subsystem nodes'}.",
                    "active_shapes": z_ids,
                    "active_connectors": [
                        f"{c.get('from') or c.get('fromTempId')}->{c.get('to') or c.get('toTempId')}"
                        for c in connectors
                        if (c.get("from") or c.get("fromTempId")) in z_ids
                    ],
                    "viewport": {"focus_shape": focus_id, "zoom": 1.05}
                    if focus_id
                    else {"fit_view": True},
                }
            )
    return chapters


async def compile_diagram_to_tts_video(
    diagram_path: Path,
    output_mp4_path: Path,
    output_webm_path: Optional[Path] = None,
    canvas_w: int = 1280,
    canvas_h: int = 720,
    play_live_termux_tts: bool = False,
) -> Dict[str, Any]:
    """End-to-end compilation of a BEJSON Diagram JSON into a TTS-narrated MP4 & WebM video."""
    diagram = json.loads(diagram_path.read_text(encoding="utf-8"))
    chapters = auto_extract_diagram_chapters(diagram)

    work_dir = output_mp4_path.parent
    tts_dir = work_dir / "tts_audio"
    frames_dir = work_dir / "video_keyframes"
    tts_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    concat_wavs: List[str] = []
    total_dur = 0.0

    for idx, ch in enumerate(chapters):
        mp3_f = tts_dir / f"seg_{idx:02d}.mp3"
        wav_f = tts_dir / f"seg_{idx:02d}.wav"
        dur = synthesize_tts_segment(ch["narration"], mp3_f, wav_f)
        ch["duration_sec"] = dur
        ch["start_sec"] = round(total_dur, 3)
        ch["wav_file"] = str(wav_f)
        total_dur += dur
        concat_wavs.append(f"file '{wav_f.resolve()}'")
        if play_live_termux_tts and idx == 0:
            speak_termux_tts_live(ch["narration"], wav_path=wav_f)

    concat_txt = tts_dir / "concat_list.txt"
    concat_txt.write_text("\n".join(concat_wavs) + "\n", encoding="utf-8")
    master_wav = tts_dir / "master_narration.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_txt),
            "-c",
            "copy",
            str(master_wav),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    dynamic_frames: List[Dict[str, Any]] = []
    elapsed = 0.0
    for idx, ch in enumerate(chapters):
        vp = resolve_viewport(diagram, ch["viewport"], canvas_w, canvas_h)
        seg_dur = float(ch["duration_sec"])
        for sub_idx, pulse in enumerate((0.35, 0.75)):
            prog = (elapsed + seg_dur * (0.5 * sub_idx)) / max(1.0, total_dur)
            svg_raw = render_diagram_svg(
                diagram=diagram,
                state={
                    "active_shapes": ch["active_shapes"],
                    "active_connectors": ch["active_connectors"],
                    "flow_progress": pulse,
                    "badge_text": ch["badge_text"],
                },
                viewport=vp,
                canvas_w=canvas_w,
                canvas_h=canvas_h,
            )
            svg_hud = inject_tts_subtitle_hud_into_svg(
                svg_raw, ch["narration"], prog, canvas_w, canvas_h
            )
            dynamic_frames.append(
                {
                    "svg_markup": svg_hud,
                    "data": {"duration_sec": round(seg_dur / 2.0, 3)},
                }
            )
        elapsed += seg_dur

    anim_doc = create_row_per_frame_animation_105a(
        animation_name=output_mp4_path.stem,
        duration_sec=float(len(dynamic_frames)) / 2.0,
        fps=2,
        width_px=canvas_w,
        height_px=canvas_h,
        dynamic_frames=dynamic_frames,
        output_prefix="vframe_",
    )
    await render_row_per_frame_animation(
        animation_doc=anim_doc,
        output_dir=str(frames_dir),
        save_updated_doc=True,
        device_scale=1,
    )

    fmap = build_field_map_105(anim_doc["Fields"])
    ffconcat_lines = ["ffconcat version 1.0"]
    last_f = None
    for idx, row in enumerate(anim_doc["Values"]):
        fpath = (frames_dir / row[fmap["frame_filename"]]).resolve()
        f_dur = float(dynamic_frames[idx]["data"]["duration_sec"])
        last_f = fpath
        ffconcat_lines.append(f"file '{fpath}'")
        ffconcat_lines.append(f"duration {f_dur:.3f}")
    if last_f:
        ffconcat_lines.append(f"file '{last_f}'")

    ffconcat_path = frames_dir / "timeline.ffconcat"
    ffconcat_path.write_text("\n".join(ffconcat_lines) + "\n", encoding="utf-8")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(ffconcat_path),
            "-i",
            str(master_wav),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-r",
            "24",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output_mp4_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    if output_webm_path:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(ffconcat_path),
                "-i",
                str(master_wav),
                "-c:v",
                "libvpx-vp9",
                "-b:v",
                "0",
                "-crf",
                "30",
                "-r",
                "24",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "libopus",
                "-b:a",
                "96k",
                "-shortest",
                str(output_webm_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    return {
        "status": "success",
        "mp4_path": str(output_mp4_path),
        "webm_path": str(output_webm_path) if output_webm_path else None,
        "master_wav_path": str(master_wav),
        "total_duration_sec": round(total_dur, 3),
        "chapters": len(chapters),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Optional Termux TTS & Synchronized Narrated Video Compiler (Graphics Domain)"
    )
    parser.add_argument("--diagram", type=str, help="Path to BEJSON diagram JSON file")
    parser.add_argument("--output-mp4", type=str, default="captures/narrated_diagram.mp4", help="Output MP4 path")
    parser.add_argument("--output-webm", type=str, default=None, help="Optional Output WebM path")
    parser.add_argument("--speak-text", type=str, default=None, help="Speak single text string via Termux TTS and exit")
    parser.add_argument("--termux-tts", action="store_true", help="Trigger live Termux TTS audio playback during compilation")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        print("termux_tts_video_compiler v1.0.0")
        return 0

    if args.speak_text:
        tmp_dir = Path("/data/data/com.termux/files/usr/tmp/tts_quick")
        mp3_p = tmp_dir / "quick.mp3"
        wav_p = tmp_dir / "quick.wav"
        if mp3_p.exists():
            mp3_p.unlink()
        dur = synthesize_tts_segment(args.speak_text, mp3_p, wav_p)
        speak_termux_tts_live(args.speak_text, wav_path=wav_p)
        print(json.dumps({"status": "spoken", "duration_sec": dur, "wav_path": str(wav_p)}))
        return 0

    if not args.diagram:
        parser.error("--diagram or --speak-text is required.")

    res = asyncio.run(
        compile_diagram_to_tts_video(
            diagram_path=Path(args.diagram).resolve(),
            output_mp4_path=Path(args.output_mp4).resolve(),
            output_webm_path=Path(args.output_webm).resolve() if args.output_webm else None,
            play_live_termux_tts=args.termux_tts,
        )
    )
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
