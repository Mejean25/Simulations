#!/usr/bin/env python3
"""Animate the thirteen mice puzzle. Run with --sequence for text only."""

import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class CountEvent:
    mouse: int
    count: int
    eaten: bool


def counting_events(total=13, interval=13):
    """Count from mouse 1, resuming at the next survivor after each meal."""
    if total < 1 or interval < 1:
        raise ValueError("total and interval must be positive")
    remaining = list(range(1, total + 1))
    position = 0
    while remaining:
        for count in range(1, interval + 1):
            yield CountEvent(remaining[position], count, count == interval)
            if count == interval:
                remaining.pop(position)
                if remaining:
                    position %= len(remaining)
            else:
                position = (position + 1) % len(remaining)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sequence", action="store_true", help="print the order without opening a window")
    parser.add_argument("--autoplay", action="store_true", help="start the animation automatically")
    args = parser.parse_args()
    events = list(counting_events())
    order = [event.mouse for event in events if event.eaten]
    if args.sequence:
        print("Eating order: " + " → ".join(map(str, order)))
        print("Mouse 8 is white and is eaten last.")
        return

    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        parser.exit(1, "This animation needs Python with Tkinter support.\nYou can still run it with --sequence.\n")

    class MouseDream:
        BG = "#101725"
        PANEL = "#192337"
        TEXT = "#eef2fa"
        MUTED = "#93a4bf"
        GOLD = "#f4bf63"
        GREEN = "#74dfc0"

        def __init__(self, root):
            self.root = root
            self.index = 0
            self.eaten = []
            self.current = None
            self.running = False
            self.timer = None
            root.title("The Cat's Dream · Thirteen Mice")
            root.geometry("1060x860")
            root.minsize(850, 780)
            root.configure(bg=self.BG)
            style = ttk.Style(root)
            style.theme_use("clam")
            style.configure("TButton", font=("Helvetica", 12), padding=(15, 9))
            style.configure("Horizontal.TScale", background=self.BG)

            tk.Label(root, text="THE CAT’S DREAM", font=("Helvetica", 25, "bold"),
                     fg=self.TEXT, bg=self.BG).pack(pady=(22, 5))
            tk.Label(root, text="12 grey mice · 1 white mouse · every 13th mouse is eaten",
                     font=("Helvetica", 12), fg=self.MUTED, bg=self.BG).pack()
            controls = tk.Frame(root, bg=self.BG)
            controls.pack(pady=15)
            self.play_button = ttk.Button(controls, text="Play", command=self.toggle)
            self.play_button.pack(side="left", padx=5)
            ttk.Button(controls, text="Next eaten", command=self.next_eaten).pack(side="left", padx=5)
            ttk.Button(controls, text="Reset", command=self.reset).pack(side="left", padx=5)
            tk.Label(controls, text="   Slow", fg=self.MUTED, bg=self.BG).pack(side="left")
            self.speed = tk.DoubleVar(value=6)
            ttk.Scale(controls, from_=1, to=10, variable=self.speed, length=130).pack(side="left", padx=7)
            tk.Label(controls, text="Fast", fg=self.MUTED, bg=self.BG).pack(side="left")
            self.canvas = tk.Canvas(root, bg=self.BG, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True, padx=18)
            self.status = tk.StringVar(value="Start at mouse 1. Count clockwise; the white mouse is number 8.")
            tk.Label(root, textvariable=self.status, font=("Helvetica", 12),
                     fg=self.TEXT, bg=self.BG, wraplength=810).pack(pady=(8, 10))
            tk.Label(root, text="Gold ring = counting now     •     Faded position = already eaten     •     Space = play / pause",
                     font=("Helvetica", 10), fg=self.MUTED, bg=self.BG).pack(pady=(0, 16))
            self.canvas.bind("<Configure>", lambda event: self.draw())
            root.bind("<space>", lambda event: self.toggle())
            root.protocol("WM_DELETE_WINDOW", self.close)

        def pause(self):
            self.running = False
            self.play_button.configure(text="Play")
            if self.timer is not None:
                self.root.after_cancel(self.timer)
                self.timer = None

        def close(self):
            self.pause()
            self.root.destroy()

        def toggle(self):
            if self.running:
                self.pause()
            else:
                if self.index == len(events):
                    self.reset()
                self.running = True
                self.play_button.configure(text="Pause")
                self.tick()

        def advance(self):
            if self.index >= len(events):
                return False
            self.current = events[self.index]
            self.index += 1
            event = self.current
            if event.eaten:
                self.eaten.append(event.mouse)
                self.status.set(f"Meal {len(self.eaten)} of 13: mouse {event.mouse} is eaten. Resume at the next remaining mouse.")
            else:
                self.status.set(f"Count {event.count} of 13 — mouse {event.mouse}. Only the remaining mice count.")
            if self.index == len(events):
                self.status.set("The dream is complete: all 12 grey mice were eaten first, and white mouse 8 was eaten last.")
            self.draw()
            return True

        def tick(self):
            self.timer = None
            if not self.running:
                return
            self.advance()
            if self.index == len(events):
                self.pause()
                self.play_button.configure(text="Replay")
                return
            delay = int(650 - self.speed.get() * 58)
            if self.current.eaten:
                delay = max(450, delay * 2)
            self.timer = self.root.after(delay, self.tick)

        def next_eaten(self):
            self.pause()
            while self.advance():
                if self.current.eaten:
                    break
            if self.index == len(events):
                self.play_button.configure(text="Replay")

        def reset(self):
            self.pause()
            self.index = 0
            self.eaten = []
            self.current = None
            self.status.set("Start at mouse 1. Count clockwise; the white mouse is number 8.")
            self.draw()

        def mouse(self, x, y, number, active=False):
            c = self.canvas
            gone = number in self.eaten
            body = "#f7f5ec" if number == 8 else "#a2acbc"
            outline = "#d4deeb" if number == 8 else "#bdc6d3"
            if gone:
                body, outline = "#263147", "#36435a"
            if active:
                c.create_oval(x-34, y-34, x+34, y+34, outline=self.GOLD, width=3)
            c.create_line(x+19, y+11, x+34, y+17, x+38, y+5,
                          fill=outline, width=2, smooth=True)
            c.create_oval(x-21, y-21, x-3, y-3, fill=body, outline=outline)
            c.create_oval(x+3, y-21, x+21, y-3, fill=body, outline=outline)
            c.create_oval(x-16, y-17, x-7, y-8, fill="#6a5868" if gone else "#e4b4b9", outline="")
            c.create_oval(x+7, y-17, x+16, y-8, fill="#6a5868" if gone else "#e4b4b9", outline="")
            c.create_oval(x-20, y-11, x+20, y+22, fill=body, outline=outline, width=2)
            for dx in (-7, 7):
                c.create_oval(x+dx-2, y+1, x+dx+2, y+5, fill=self.BG, outline="")
            c.create_oval(x-3, y+10, x+3, y+14, fill="#776071" if gone else "#c77d91", outline="")
            for sign in (-1, 1):
                for dy in (-3, 4):
                    c.create_line(x+sign*7, y+13, x+sign*26, y+13+dy, fill=outline)
            label = f"{number} · WHITE" if number == 8 else str(number)
            c.create_text(x, y+45, text=label, fill=self.MUTED if gone else self.TEXT,
                          font=("Helvetica", 10, "bold"))

        def draw(self):
            c = self.canvas
            c.delete("all")
            width, height = c.winfo_width(), c.winfo_height()
            cx, cy = width/2, (height-115)/2
            radius = min(width/2-85, (height-115)/2-55)
            if radius < 40:
                return
            c.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                          outline="#2b3952", width=2, dash=(3, 7))
            c.create_text(cx+radius+44, cy, text="↓\nCLOCKWISE", fill=self.MUTED,
                          font=("Helvetica", 9), justify="center")
            for number in range(1, 14):
                angle = -math.pi/2 + (number-1)*2*math.pi/13
                self.mouse(cx+radius*math.cos(angle), cy+radius*math.sin(angle), number,
                           self.current is not None and self.current.mouse == number)

            # A sleeping cat at the center of the dream.
            cat_y = cy-42
            c.create_polygon(cx-47, cat_y-8, cx-43, cat_y-49, cx-15, cat_y-27,
                             fill=self.GOLD, outline="")
            c.create_polygon(cx+47, cat_y-8, cx+43, cat_y-49, cx+15, cat_y-27,
                             fill=self.GOLD, outline="")
            c.create_oval(cx-49, cat_y-31, cx+49, cat_y+36, fill=self.GOLD, outline="")
            for dx in (-20, 20):
                c.create_line(cx+dx-9, cat_y+1, cx+dx, cat_y+6, cx+dx+9, cat_y+1,
                              fill="#624629", width=3, smooth=True)
            c.create_polygon(cx-5, cat_y+14, cx+5, cat_y+14, cx, cat_y+20, fill="#94614e")
            c.create_text(cx+67, cat_y-34, text="z Z", font=("Helvetica", 17), fill=self.MUTED)
            finished = len(self.eaten) == 13
            title = "White mouse last!" if finished else "Ready to dream" if self.current is None else f"{self.current.count} / 13"
            c.create_text(cx, cy+30, text=title, font=("Helvetica", 20, "bold"),
                          fill=self.GREEN if finished else self.TEXT)
            c.create_text(cx, cy+61, text=f"{len(self.eaten)} eaten  ·  {13-len(self.eaten)} remaining",
                          font=("Helvetica", 11), fill=self.MUTED)
            c.create_text(22, height-83, text="EATING ORDER", anchor="w",
                          font=("Helvetica", 10, "bold"), fill=self.MUTED)
            slot = (width-40)/13
            for i in range(13):
                x = 20+(i+0.5)*slot
                mouse = self.eaten[i] if i < len(self.eaten) else None
                fill = self.GREEN if mouse == 8 else self.PANEL
                c.create_rectangle(x-slot/2+3, height-59, x+slot/2-3, height-18,
                                   fill=fill, outline="#344059")
                c.create_text(x, height-39, text=str(mouse) if mouse else "·",
                              font=("Helvetica", 15, "bold"), fill=self.BG if mouse == 8 else self.TEXT)
                c.create_text(x, height-7, text=str(i+1), font=("Helvetica", 8), fill=self.MUTED)

    try:
        root = tk.Tk()
    except tk.TclError as exc:
        parser.exit(1, f"Cannot open a graphical window: {exc}\nRun with --sequence for text output.\n")
    app = MouseDream(root)
    if args.autoplay:
        root.after(700, app.toggle)
    root.mainloop()


if __name__ == "__main__":
    main()
