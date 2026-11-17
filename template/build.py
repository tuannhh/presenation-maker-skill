#!/usr/bin/env python3
"""Đóng gói deck thành 1 file HTML tự chứa (font + ảnh + logo + video nhúng base64).
Chạy:  ~/.claude/skills/misa-html-deck/.venv/bin/python build.py
Cấu hình ở deck.json (title, output, logo, parts, videos).
"""
import base64, io, json, re, sys
from pathlib import Path
from PIL import Image
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).parent
SRC, AS, OUT = ROOT / "src", ROOT / "assets", ROOT / "dist"
OUT.mkdir(exist_ok=True)
CFG = json.loads((ROOT / "deck.json").read_text("utf-8"))

# ---------- Icon set (Lucide-style, stroke 2) ----------
ICONS = {
 "shield":'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
 "shield-check":'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 "shield-alert":'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M12 8v4M12 16h.01"/>',
 "alert-triangle":'<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4M12 17h.01"/>',
 "phone":'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "message":'<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 "link":'<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
 "smartphone":'<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>',
 "download":'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
 "banknote":'<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
 "coins":'<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/>',
 "trending-up":'<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
 "trending-down":'<path d="M22 17 13.5 8.5 8.5 13.5 2 7"/><path d="M16 17h6v-6"/>',
 "globe":'<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
 "landmark":'<path d="M3 22h18"/><path d="M6 18v-7M10 18v-7M14 18v-7M18 18v-7"/><path d="M12 2 20 7H4z"/>',
 "bank":'<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20M6 15h4"/>',
 "users":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "user":'<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
 "user-check":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/>',
 "bot":'<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/>',
 "factory":'<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1M12 18h1M7 18h1"/>',
 "crosshair":'<circle cx="12" cy="12" r="10"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/>',
 "truck":'<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 "gift":'<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>',
 "briefcase":'<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
 "heart":'<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
 "clock":'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "key":'<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
 "lock":'<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "eye":'<path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/>',
 "eye-off":'<path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.53 13.53 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="m2 2 20 20"/>',
 "help":'<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
 "hand":'<path d="M18 11V6a2 2 0 0 0-4 0v5"/><path d="M14 10V4a2 2 0 0 0-4 0v6"/><path d="M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
 "check-circle":'<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
 "x-circle":'<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/>',
 "check":'<path d="M20 6 9 17l-5-5"/>',
 "arrow-right":'<path d="M5 12h14M12 5l7 7-7 7"/>',
 "chevrons-right":'<path d="m6 17 5-5-5-5M13 17l5-5-5-5"/>',
 "play":'<path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/>',
 "zap":'<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 "brain":'<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v13"/>',
 "bell":'<path d="M10.27 21a2 2 0 0 0 3.46 0"/><path d="M3.26 15.33A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.67C19.41 13.96 18 12.5 18 8A6 6 0 0 0 6 8c0 4.5-1.41 5.96-2.74 7.33"/>',
 "megaphone":'<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
 "flag":'<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',
 "repeat":'<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
 "refresh":'<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 "home":'<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "sparkles":'<path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.13-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.13a.5.5 0 0 1 .96 0L14.06 8.5A2 2 0 0 0 15.5 9.94l6.13 1.58a.5.5 0 0 1 0 .96L15.5 14.06a2 2 0 0 0-1.44 1.44l-1.58 6.13a.5.5 0 0 1-.96 0z"/>',
 "ban":'<circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/>',
 "ticket":'<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2M13 17v2M13 11v2"/>',
 "receipt":'<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8M12 17.5v-11"/>',
 "trophy":'<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
 "grad":'<path d="M21.42 10.92a1 1 0 0 0-.02-1.84L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.83l8.57 3.91a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
 "flame":'<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
 "qr":'<rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3M21 21v.01M12 7v3a2 2 0 0 1-2 2H7M3 12h.01M12 3h.01M12 16v.01M16 12h1M21 12v.01M12 21v-1"/>',
 "search":'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 "scan-face":'<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01M15 9h.01"/>',
 "mic":'<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/>',
 "file-text":'<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M10 9H8M16 13H8M16 17H8"/>',
 "image":'<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
 "git-branch":'<path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
 "target":'<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 "hook":'<path d="M15 3v10a5 5 0 0 1-10 0v-2l3 3"/><circle cx="15" cy="3" r="1.2"/>',
 "toggle":'<rect width="20" height="12" x="2" y="6" rx="6"/><circle cx="16" cy="12" r="2.5"/>',
 "building":'<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2M10 6h4M10 10h4M10 14h4M10 18h4"/>',
 "wallet":'<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
 "percent":'<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
 "hourglass":'<path d="M5 22h14M5 2h14M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"/>',
 "life-buoy":'<circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/><circle cx="12" cy="12" r="4"/>',
 "share":'<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.59 13.51 6.83 3.98M15.41 6.51l-6.82 3.98"/>',
 "info":'<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
 "lightbulb":'<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4"/>',
 "cast":'<path d="M2 8V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-6"/><path d="M2 12a9 9 0 0 1 8 8M2 16a5 5 0 0 1 4 4M2 20h.01"/>',
 "layers":'<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
 "map-pin":'<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 "wrench":'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 "id-card":'<path d="M16 10h2M16 14h2"/><path d="M6.17 15a3 3 0 0 1 5.66 0"/><circle cx="9" cy="11" r="2"/><rect x="2" y="5" width="20" height="14" rx="2"/>',
 "activity":'<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
 "sliders":'<path d="M21 4h-7M10 4H3M21 12h-9M8 12H3M21 20h-5M12 20H3M14 2v4M8 10v4M16 18v4"/>',
 "handshake":'<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3M3 4h8"/>',
}

def icon_svg(name):
    if name not in ICONS:
        sys.exit(f"Thiếu icon: {name}")
    return f'<svg class="i" aria-hidden="true"><use href="#i-{name}"/></svg>'

def b64(data, mime):
    return f"data:{mime};base64," + base64.b64encode(data).decode()

def webp(path, max_side, q=80):
    im = Image.open(path)
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=q, method=6)
    return buf.getvalue()

# ---------- Compose ----------
slides = (SRC / "slides.html").read_text("utf-8")
css = (SRC / "style.css").read_text("utf-8")
js = (SRC / "app.js").read_text("utf-8")
# mô-đun ảnh chèn thêm: ghép vào trước "window.deck" (cùng phạm vi với app.js)
_img = (SRC / "img.js").read_text("utf-8")
assert "window.deck = {" in js
js = js.replace("window.deck = {", _img + "\nwindow.deck = {", 1)
notes = json.loads((SRC / "notes.json").read_text("utf-8")) if (SRC / "notes.json").exists() else []
SECS = re.findall(r'<section class="slide([^"]*)"([^>]*)>', slides)
n_slides = len(SECS)
if len(notes) != n_slides:
    print(f"  (ghi chú: {len(notes)} mục / {n_slides} trang — tự bù/cắt cho khớp)")
notes = (notes + [""] * n_slides)[:n_slides]
# số trang đánh số = mọi trang trừ trang kết (.closing); các phần lấy theo data-p
TOTAL_NUMBERED = sum(1 for cls, _ in SECS if "closing" not in cls)
parts = [None]
for k, p in enumerate(CFG.get("parts", []), 1):
    idx = [i + 1 for i, (cls, attrs) in enumerate(SECS) if f'data-p="{k}"' in attrs and "cover" not in cls]
    parts.append({"n": p["name"], "c": p.get("color", "#4D8BFF"), "from": min(idx) if idx else 0, "to": max(idx) if idx else 0})

used_icons = sorted(set(re.findall(r"\[\[([a-z0-9-]+)\]\]", slides)))
slides = re.sub(r"\[\[([a-z0-9-]+)\]\]", lambda m: icon_svg(m.group(1)), slides)
sprite = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(
    f'<symbol id="i-{n}" viewBox="0 0 24 24">{ICONS[n]}</symbol>' for n in used_icons) + "</defs></svg>"

# Ảnh minh hoạ (dùng lại qua CSS, không lặp base64)
used_imgs = sorted(set(re.findall(r'data-im="([a-z_]+)"', slides)))
img_css, total_img = [], 0
for name in used_imgs:
    p = next((AS / "img" / f"{name}.{e}" for e in ("png", "jpg", "jpeg", "webp") if (AS / "img" / f"{name}.{e}").exists()), None)
    if not p: print(f"  ! thiếu ảnh assets/img/{name}.png — thẻ ảnh sẽ trống"); continue
    W_, H_ = Image.open(p).size
    data = webp(p, 900, 82)
    total_img += len(data)
    img_css.append(f'.im[data-im="{name}"]{{--r:{W_/H_:.4f}}}.im[data-im="{name}"] .imt{{background-image:url({b64(data, "image/webp")})}}')
slides = re.sub(r'(<div class="im[^"]*" data-im="[a-z_]+"[^>]*>)(</div>)', r'\1<i class="imt"></i>\2', slides)
logo = webp(ROOT / CFG.get("logo", "assets/logo-misa.png"), 1300, 90)

js = js.replace("{{NOTES_JSON}}", json.dumps(notes, ensure_ascii=False)).replace("{{TOTAL_NUMBERED}}", str(TOTAL_NUMBERED)).replace("{{PARTS_JSON}}", json.dumps(parts, ensure_ascii=False))


# ---------- Nền security: lưới lục giác + khiên chìm + hạt sáng ----------
import math, random
def hex_tile():
    W,H=52,90; R=W/math.sqrt(3); r=R-1.05
    def hx(cx,cy): return "M"+" L".join(f"{cx+r*math.cos(math.radians(a)):.2f} {cy+r*math.sin(math.radians(a)):.2f}" for a in range(-90,270,60))+" Z"
    d=" ".join(hx(x,y) for x,y in [(0,0),(W,0),(W/2,H/2),(0,H),(W,H)])
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><path d="{d}" fill="rgb(6,13,33)" fill-opacity=".8"/></svg>'
    return "data:image/svg+xml;base64,"+base64.b64encode(svg.encode()).decode()

def circuit_svg():
    rg=random.Random(11); W,H=1920,1080; base=[]; pulses=[]; pads=[]
    def route(x,y,dx,dy,n):
        pts=[(x,y)]
        for k in range(n):
            if k%2==0:
                L=rg.choice([70,110,150,200,260]); x,y=x+dx*L,y+dy*L
            else:
                d=rg.choice([30,50,70])*rg.choice([-1,1])
                if dx: x,y=x+dx*abs(d),y+d
                else: x,y=x+d,y+dy*abs(d)
            pts.append((x,y))
        return pts
    starts=[]
    for i in range(9): starts.append((0,rg.uniform(60,1020),1,0))
    for i in range(9): starts.append((W,rg.uniform(60,1020),-1,0))
    for i in range(5): starts.append((rg.uniform(80,1840),0,0,1))
    for i in range(5): starts.append((rg.uniform(80,1840),H,0,-1))
    for idx,(x,y,dx,dy) in enumerate(starts):
        pts=route(x,y,dx,dy,rg.choice([3,4,5]))
        d="M"+" L".join(f"{a:.0f} {b:.0f}" for a,b in pts)
        base.append(f'<path d="{d}"/>')
        ex,ey=pts[-1]; pads.append(f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="5"/>')
        if rg.random()<.3:
            mx,my=pts[len(pts)//2]; pads.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="3.5"/>')
        if idx in (0,4,9,13,18,23):
            dur=rg.uniform(16,24); dl=-rg.uniform(0,20)
            pulses.append(f'<path pathLength="1000" d="{d}" style="animation-duration:{dur:.1f}s;animation-delay:{dl:.1f}s"/>')
    # vài chip IC nhỏ
    chips=[]  # bỏ các ô vuông IC theo góp ý
    return (f'<svg class="circ" viewBox="0 0 {W} {H}" preserveAspectRatio="none">'
            f'<g class="cb">{"".join(base)}</g><g class="cp">{"".join(pads)}{"".join(chips)}</g>'
            f'<g class="cg">{"".join(pulses)}</g><g class="cl">{"".join(pulses)}</g></svg>')

SH='M410 60 L720 170 V430 C720 640 590 790 410 870 C230 790 100 640 100 430 V170 Z'
SH2='M410 110 L672 203 V430 C672 610 562 738 410 808 C258 738 148 610 148 430 V203 Z'
rnd=random.Random(7)
ptc="".join(f'<i style="left:{rnd.uniform(0,1920):.0f}px;animation-duration:{rnd.uniform(30,45):.1f}s;animation-delay:{-rnd.uniform(0,40):.1f}s;{"width:2px;height:2px;" if rnd.random()<.5 else ""}"></i>' for _ in range(10))
BG=(f'<div id="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="glow"></div>'
    f'{circuit_svg()}<div class="scan"></div>'
    f'<svg class="bshield" viewBox="0 0 820 920"><circle class="ring" cx="410" cy="450" r="400"/><circle class="ring r2" cx="410" cy="450" r="440"/>'
    f'<path class="o" d="{SH}"/><path class="o" d="{SH2}" style="opacity:.6"/><path class="flow" pathLength="1000" d="{SH}" style="stroke-dasharray:70 930"/>'
    f'<path d="M300 450 L385 535 L540 360" class="o" style="stroke-width:6;opacity:.7"/></svg>'
    f'<div class="ptc">{ptc}</div><div class="vig"></div></div>')

title = CFG["title"]
html_body = f"""<div id="stage" data-p="1">
{BG}
<div id="logo"><img src="{{{{LOGO}}}}" alt="MISA"></div>
{slides}
<div id="foot"><div class="parts"></div><div class="pg"></div></div>
</div>
<div id="ov"></div><div id="jump"></div>
<div id="help"><kbd>→</kbd><kbd>Space</kbd> tiếp · <kbd>←</kbd> lùi · <kbd>F</kbd> toàn màn hình · <kbd>N</kbd> ghi chú · <kbd>G</kbd> mục lục · <kbd>E</kbd> sửa nội dung · gõ số + <kbd>Enter</kbd> nhảy trang</div>
<div id="ebar"><span class="dot"></span><b>Chế độ chỉnh sửa</b><span>Bấm chữ để sửa · kéo-thả hoặc Ctrl+V ảnh vào trang để chèn · bấm khung video để chèn video · <kbd>←</kbd><kbd>→</kbd> đổi trang</span><span class="st">Có thay đổi chưa lưu</span><button class="ad">🖼 Chèn ảnh</button><button class="sv">Lưu file (Ctrl+S)</button><button class="ex">Thoát (E)</button></div>
<div id="fmt" class="off"><div class="g"><button data-f="fs-" title="Chữ nhỏ hơn">A−</button><span class="fsv" title="Cỡ chữ">–</span><button data-f="fs+" title="Chữ to hơn">A+</button></div><div class="g"><button data-f="lh-" title="Giảm dãn dòng">↕−</button><span class="lhv" title="Dãn dòng">–</span><button data-f="lh+" title="Tăng dãn dòng">↕+</button></div><div class="g"><button data-f="br" title="Xuống dòng (Enter)">↵ Xuống dòng</button></div><div class="g"><button data-f="bold" title="In đậm (Ctrl+B)"><b>B</b></button><button data-f="italic" title="In nghiêng (Ctrl+I)"><i>I</i></button><button data-f="underline" title="Gạch chân (Ctrl+U)"><u>U</u></button></div><div class="g cl"><button data-f="c" data-v="#1557F0" title="Xanh dương" style="--sw:#1557F0"></button><button data-f="c" data-v="#E3263A" title="Đỏ" style="--sw:#E3263A"></button><button data-f="c" data-v="#0B9A62" title="Xanh lá" style="--sw:#0B9A62"></button><button data-f="c" data-v="#DE8A00" title="Cam" style="--sw:#DE8A00"></button><button data-f="c" data-v="#5A3FE6" title="Tím" style="--sw:#5A3FE6"></button><button data-f="c" data-v="#0B1A4A" title="Xanh đen (mặc định)" style="--sw:#0B1A4A"></button><button data-f="hl" title="Tô nền vàng nhấn mạnh" class="hlb">▇</button></div><div class="g"><button data-f="al" data-v="left" title="Căn trái"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 10h12M3 14h18M3 18h12"/></svg></button><button data-f="al" data-v="center" title="Căn giữa"><svg viewBox="0 0 24 24"><path d="M3 6h18M6 10h12M3 14h18M6 18h12"/></svg></button><button data-f="al" data-v="right" title="Căn phải"><svg viewBox="0 0 24 24"><path d="M3 6h18M9 10h12M3 14h18M9 18h12"/></svg></button><button data-f="al" data-v="justify" title="Căn đều 2 bên"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 10h18M3 14h18M3 18h18"/></svg></button></div><div class="g"><button data-f="up" title="VIẾT HOA">AA</button><button data-f="low" title="viết thường">aa</button><button data-f="none" title="Giữ nguyên như khi gõ">Aa</button></div><div class="g"><button data-f="undo" title="Hoàn tác (Ctrl+Z)">↶</button><button data-f="redo" title="Làm lại">↷</button><button data-f="clear" title="Xoá định dạng">⌫ Định dạng</button></div><span class="tip">Bấm vào một đoạn chữ để định dạng</span></div><div id="ipan"><div class="g"><span class="l">Sáng / tối</span><input type="range" data-k="b" min="30" max="170" step="1"><span class="v" data-v="b"></span></div><div class="g"><span class="l">Bo góc</span><input type="range" data-k="rad" min="0" max="50" step="1"><span class="v" data-v="rad"></span></div><div class="g"><span class="l">Viền</span><input type="range" data-k="bw" min="0" max="24" step="1"><span class="v" data-v="bw"></span><button data-bc="#ffffff" title="Trắng" style="--sw:#ffffff"></button><button data-bc="#0B1A4A" title="Xanh đen" style="--sw:#0B1A4A"></button><button data-bc="#1557F0" title="Xanh dương" style="--sw:#1557F0"></button><button data-bc="#E3263A" title="Đỏ" style="--sw:#E3263A"></button><button data-bc="#DE8A00" title="Cam" style="--sw:#DE8A00"></button><label class="cp" title="Chọn màu viền khác"><input type="color" data-k="bc"></label></div><div class="g"><span class="l">Đổ bóng</span><input type="range" data-k="sh" min="0" max="100" step="1"><span class="v" data-v="sh"></span></div><div class="g"><span class="l">Xoay</span><input type="range" data-k="r" min="-180" max="180" step="1"><span class="v" data-v="r"></span></div><div class="g"><button data-ia="front" title="Đưa ảnh lên trên cùng">Lên trên</button><button data-ia="back" title="Đưa ảnh ra sau chữ">Ra sau chữ</button><button data-ia="reset" title="Bỏ xoay, sáng tối, viền… về mặc định">Đặt lại</button><button data-ia="del" class="del" title="Xoá ảnh (Delete)">Xoá</button></div></div><div id="toast"></div>
"""

# ---------- Font subset theo đúng ký tự dùng ----------
text_for_glyphs = re.sub(r"<[^>]+>", " ", html_body) + js + css + "".join(notes) + title
text_for_glyphs = __import__("html").unescape(text_for_glyphs)
chars = set(text_for_glyphs) | set("0123456789.,:;!?%+-–—…“”‘’\"'()/·→←▶◀ ") | set("абвгдеёжзийклмнопрстуфхцчшщъыьэюяіАВЕКМНОРСТХ")
chars |= set(chr(c) for c in range(0x20, 0x7F))
unicodes = sorted(ord(c) for c in chars if ord(c) >= 0x20)

def subset_font(path, out_name, keep_axes=None):
    f = TTFont(path, lazy=False)
    if keep_axes and "fvar" in f:
        f = instancer.instantiateVariableFont(f, keep_axes); f = TTFont(io.BytesIO((lambda b: (f.save(b), b.getvalue())[1])(io.BytesIO())), lazy=False)
    cmap = f.getBestCmap()
    missing = [chr(u) for u in unicodes if u not in cmap and u > 0x7F]
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
    sub = subset.Subsetter(opts); sub.populate(unicodes=unicodes); sub.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    print(f"  {out_name}: {len(buf.getvalue())//1024} KB" + (f"  (thiếu {len(missing)} ký tự: {''.join(missing[:30])})" if missing else ""))
    return buf.getvalue()

F = AS / "fonts"
print("Font:")
fonts = {
    "F_GS400": subset_font(F / "GoogleSans-Regular.otf", "Google Sans 400"),
    "F_GS500": subset_font(F / "GoogleSans-Medium.otf", "Google Sans 500"),
    "F_GS700": subset_font(F / "GoogleSans-Bold.ttf", "Google Sans 700"),
    "F_GS900": subset_font(F / "GoogleSans-Black.ttf", "Google Sans 900"),
    "F_INTER": subset_font(F / "Inter-VariableFont_opsz,wght.ttf", "Inter var", {"wght": (300, 800), "opsz": (14, 32)}),
}
for k, v in fonts.items():
    css = css.replace("{{" + k + "}}", b64(v, "font/woff2"))

# Video nhúng sẵn: số trang -> file đã nén
VMAP = {int(k): v for k, v in CFG.get("videos", {}).items()}
VIDS = "".join(f'<script type="application/octet-stream" id="dv-{n}">{base64.b64encode((AS/"video"/f).read_bytes()).decode()}</script>\n' for n, f in VMAP.items() if (AS/"video"/f).exists())
print("Video nhúng:", {n: f"{(AS/'video'/f).stat().st_size/1048576:.1f} MB" for n, f in VMAP.items() if (AS/'video'/f).exists()})
html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{css}
{''.join(img_css)}</style>
</head><body>
{sprite}
{html_body}
<div id="vfs"></div>
<script id="deck-edits" type="application/json">{{}}</script>
{VIDS}
<script>{js}</script>
</body></html>"""
html = html.replace("{{LOGO}}", b64(logo, "image/webp")).replace("{{HEX}}", hex_tile())
left = re.findall(r"\{\{[A-Z_]+\}\}", html)
assert not left, left

out = OUT / CFG.get("output", "deck.html")
out.write_text(html, "utf-8")
print(f"Trang: {n_slides} ({TOTAL_NUMBERED} đánh số) · Ảnh: {len(used_imgs)} ảnh, {total_img//1024} KB · Logo {len(logo)//1024} KB · Icon: {len(used_icons)}")
print(f"=> {out}  ({out.stat().st_size/1024/1024:.2f} MB)")
