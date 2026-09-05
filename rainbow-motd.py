#!/usr/bin/env python3

from pathlib import Path

motd_file = Path("/home/arduino/motd.txt")

# Red, orange, yellow, green, cyan, blue, violet, magenta
colors = [196, 208, 226, 46, 51, 27, 93, 201]

if motd_file.exists():
    art = motd_file.read_text()

    for row, line in enumerate(art.splitlines()):
        # Limit and pad each line to exactly 80 characters
        line = line[:80].ljust(80)

        # Black background
        print("\033[48;5;0m", end="")

        for column, character in enumerate(line):
            if character == " ":
                print(" ", end="")
            else:
                color = colors[(column // 4 + row) % len(colors)]
                print(
                    f"\033[1;38;5;{color};48;5;0m{character}",
                    end=""
                )

        # Reset colors after each line
        print("\033[0m")

# Restore the terminal's normal colors
print("\033[0m", end="")
