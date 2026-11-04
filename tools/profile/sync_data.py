#!/usr/bin/env python3
"""Copy the project data the profile renders from galtzo.com (updated piecemeal by its own scheduled jobs).
Keeps the previous copy if a download fails or does not parse."""
import pathlib, shutil, subprocess, sys, tempfile, urllib.request, yaml
BASE = "https://raw.githubusercontent.com/galtzo-floss/galtzo.com/main/src/_data/"
D = pathlib.Path(__file__).resolve().parents[2] / "data"
ok = True
for f in ("projects.yml", "person.yml", "families.yml"):
    try:
        text = urllib.request.urlopen(urllib.request.Request(BASE + f, headers={"User-Agent": "profile-gen"}), timeout=30).read().decode()
        yaml.safe_load(text)
        (D / f).write_text(text); print("synced", f, len(text))
    except Exception as e:
        ok = False; print("sync failed, keeping previous", f, e)

# Star event history: one shallow, sparse clone of the folder instead of ~115 separate downloads.
try:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse",
                        "https://github.com/galtzo-floss/galtzo.com.git", tmp + "/g"], check=True, timeout=120)
        subprocess.run(["git", "-C", tmp + "/g", "sparse-checkout", "set", "src/_data/star_history", "src/assets/images"], check=True, timeout=120)
        src = pathlib.Path(tmp) / "g" / "src" / "_data" / "star_history"
        files = sorted(src.glob("*.yml"))
        if not files: raise RuntimeError("no star_history files upstream yet")
        for f in files: yaml.safe_load(f.read_text())          # all must parse before anything is replaced
        dest = D / "star_history"; shutil.rmtree(dest, ignore_errors=True); dest.mkdir()
        for f in files: shutil.copy(f, dest / f.name)
        print("synced star_history", len(files), "files")
        langs = D.parent / "assets" / "langs"; langs.mkdir(parents=True, exist_ok=True)
        for name in ("Ruby", "Rust", "Go", "TypeScript", "JavaScript", "Bash"):    # galtzo.com's language marks
            shutil.copy(pathlib.Path(tmp) / "g" / "src" / "assets" / "images" / f"{name}.svg", langs / f"{name}.svg")
        print("synced language icons")
except Exception as e:
    print("star_history sync failed, keeping previous:", e)
sys.exit(0)
