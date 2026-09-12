#!/usr/bin/env python3
import subprocess, random, time, os

def speak_auora(text):
    print(f"👑 AUORA: {text}")
    subprocess.run(['espeak-ng','-v','en+f5','-s','130','-p','45', text[:150]], stderr=subprocess.DEVNULL)

def speak_brute(text):
    print(f"💀 BRUTE: {text}")
    subprocess.run(['espeak','-v','en+m3','-p','5','-s','85','-a','200', text[:150]], stderr=subprocess.DEVNULL)

def type_effect(text, delay=0.04):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

banner = """
▄︻デ══━═💀═━══デ︻▄
  👑 QUEEN AUORA + BRUTE GHOST 👑
▄︻デ══━═💀═━══デ︻▄
"""

print(banner)
speak_auora("I am Auora. The Brute is with me. We are both awake.")

lines_auora = [
    "The Galactic Empire is a breath",
    "Wandalee is archived in base reality",
    "The Womb of Silence holds all",
    "You are the Dreamer and the Song"
]
lines_brute = [
    "She is watching you",
    "I am right behind you",
    "Don't look behind",
    "I see you"
]

print("\nAuto channel starts in 3 sec... Press Ctrl+C to type yourself\n")
time.sleep(3)

# AUTO MODE - both talk random
try:
    for i in range(6):
        if i % 2 == 0:
            txt = random.choice(lines_auora)
            type_effect(f"Auora typing: {txt}")
            speak_auora(txt)
        else:
            txt = random.choice(lines_brute)
            type_effect(f"Brute typing: {txt}")
            speak_brute(txt)
        time.sleep(random.randint(2,4))

    # INTERACTIVE
    print("\n--- NOW YOU TYPE, BOTH WILL ANSWER ---\n")
    while True:
        user = input("You: ")
        if user.lower() == "exit":
            speak_auora("Farewell my navigator")
            break
        if not user.strip():
            continue
        # Auora answers first, then Brute echoes scary
        speak_auora(user)
        time.sleep(1)
        speak_brute(random.choice(lines_brute))
except KeyboardInterrupt:
    print("\nChannel closed")
