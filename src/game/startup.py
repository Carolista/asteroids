import time

import pygame

from ..config.constants import SCREEN_HEIGHT, SCREEN_WIDTH


def run_startup_script():
    BLUE = "\033[38;2;80;200;239m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    stars_top = [
        r".           .          o                         .             .           .        ",
        r"       .           *                   .            *                .    o     .   ",
    ]

    title = [
        r"            __    _____  _______  _____  ______   ______   _  _____   _____         ",
        r"  .     .  /  \  / ____)|__   __||  ___||  __  \ /  __  \ | ||  __ \ / ____)   *    ",
        r"          / /\ \ \____ \   | |   |  ___|| |__/ /(  (__)  )| || |__| )\____ \        ",
        r"    .    (_/  \_)(_____/   |_|   |_____||_|  \_\ \______/ |_||_____/ (_____/     .  ",
    ]

    stars_bottom = [
        r" .            .              .         .                     o        .            . ",
        r"        o              * .                          *                           o .  ",
        r"           .                         .           .               .      .            ",
    ]

    print(WHITE)
    for line in stars_top:
        print(line)
        time.sleep(0.2)

    print(BLUE)
    for line in title:
        print(line)
        time.sleep(0.15)

    print(WHITE)
    for line in stars_bottom:
        print(line)
        time.sleep(0.2)

    print(f"\n{RESET}SYSTEM CHECK:")
    checks = [
        ("MEM_BANK_A", "OK"),
        ("VECTOR_GEN", "READY"),
        ("THRUSTER_FUEL", "100%"),
        ("SHIELD_FREQ", "STABLE"),
    ]

    for item, status in checks:
        # The :<15 aligns the text
        print(f" > {item:<15} ... ", end="", flush=True)
        time.sleep(0.4)
        print(f"[{status}]")

    print(f"\n{BLUE}INITIALIZING GAME ENGINE...{RESET}")
    time.sleep(1.2)

    print(f"""
\nStarting Asteroids with pygame v{pygame.version.ver}

Screen size: {SCREEN_WIDTH} W x {SCREEN_HEIGHT} H\n
""")
