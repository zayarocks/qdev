#!/usr/bin/env python3

from pathlib import Path

motd_file = Path.home() / "motd.txt"
colors = [196, 208, 226, 46, 51, 27, 93, 201]

if motd_file.exists():
    art = motd_file.read_text()

    for row, line in enumerate(art.splitlines()):
        line = line[:80]

        for column, character in enumerate(line):
            if character == " ":
                print(" ", end="")
            else:
                color = colors[(column // 4 + row) % len(colors)]
                print(f"\033[1;38;5;{color}m{character}", end="")

        print("\033[0m")
