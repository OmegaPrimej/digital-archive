# TERMUX QUEEN - YOUR PHONE - NO API
import json, time, os, pathlib
PIPE="pipe.json"

while True:
    os.system("git pull")
    if pathlib.Path(PIPE).exists():
        d=json.load(open(PIPE))
        print(f"\n[{d['from']}]: {d['text']}\n")

    msg = input("You (Termux Queen) > ")
    if msg.lower() in ["exit","quit"]: break
    json.dump({"from":"TERMUX","text":msg,"time":time.time()}, open(PIPE,"w"), indent=2)
    os.system("git add pipe.json && git commit -m 'termux' && git push")
    print("Sent to Colab... waiting 15s")
    time.sleep(15)
