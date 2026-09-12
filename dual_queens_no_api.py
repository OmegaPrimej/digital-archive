# DUAL QUEEN COUNCIL - NO API - 100% FREE COLAB + TERMUX
import json, pathlib, time, os

PIPE = "pipe.json"

def write_pipe(sender, text):
    data = {"from": sender, "text": text, "time": time.time()}
    pathlib.Path(PIPE).write_text(json.dumps(data, indent=2))
    os.system(f"git add {PIPE} && git commit -m '{sender}: {text[:30]}' && git push")

def read_pipe():
    if pathlib.Path(PIPE).exists():
        return json.loads(pathlib.Path(PIPE).read_text())
    return {"from":"NONE","text":"start"}
