# The Cat’s Dream

A Python desktop animation of the thirteen mice puzzle, using Tkinter.

## Run

From the folder containing the program:

```sh
python3 dreaming_cat.py
```

Requires Python 3.7 or newer with Tkinter and a graphical desktop. No pip packages are needed. If your Python does not include Tkinter, install Tk support for that Python distribution.

- **Play / Pause** or **Space** controls the animation.
- **Next eaten** advances to the next mouse eaten.
- **Reset** starts over.
- The speed slider controls counting speed.

The gold ring follows the count clockwise. Eaten mice fade out and are skipped in subsequent counts. The bottom row records the eating order. Mouse 1 is counted first; mouse 8 is white.

For text output without a graphical window:

```sh
python3 dreaming_cat.py --sequence
```

Expected order: **13, 1, 3, 6, 10, 5, 2, 4, 9, 11, 12, 7, 8**.

To start playing immediately:

```sh
python3 dreaming_cat.py --autoplay
```

On this Mac, the verified graphical Python runtime is `/opt/anaconda3/bin/python3`:

```sh
/opt/anaconda3/bin/python3 dreaming_cat.py --autoplay
```
