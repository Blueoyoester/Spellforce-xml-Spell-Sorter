# SpellForce XML Spell Sorter

A lightweight, automated Python utility designed for **SpellForce: Platinum Edition** modders. This tool reorganizes the structure of your `[i000, t2002] Spells.xml` file into a perfectly logical and clean layout without breaking game files or deleting vital developer comments.

**Version:** 1.0.0 | **License:** Modified MIT (Non-Commercial) | **Platform:** Windows | **Language:** Python | **Maintained:** Yes

[What It Does](#what-it-does) • [Features](#features) • [How to Use](#how-to-use) • [Roadmap](#roadmap--future-plans) • [License](#license)

---

### What It Does

When working with large modification files using tools like the *SFCFF Editor*, spell IDs and spell lines can quickly become cluttered, out of order, or hard to navigate. 

This script reads your XML file and automatically sorts every spell using a **three-tier smart hierarchy**: 

1. **Alphabetically** by Spell Line (e.g., Decay ➔ FireBall ➔ FireBurst ➔ Freeze).
2. **Numerically by Spell Level** (`Level="1"` up to `Level="13"`, sending special/enemy high-level spells like `Level="101"` safely to the end of the line).
3. **Numerically by Spell ID** (as a foolproof tie-breaker).

### Features

* **Comment Preservation:** Unlike standard XML sorters, this script **preserves and links** the original game comments to their correct spell entries. 
* **Smart Math Sorting:** Avoids text-sorting glitches (e.g., it correctly places ID 83 *before* ID 250).
* **Multi-language Support:** Automatically detects your system language (supports **English** and **Polish** natively out of the box).

### How to Use

> **Note on Directory:** The script must be placed in the specific working directory where you extracted the game's `data.cff` file using the SFCFF Editor (the official developer modding tool released by the creators of the game in patch 1.61 on April 9, 2021).

1. Place the `sorter.py` script into the same folder where your game file `[i000, t2002] Spells.xml` is located.
2. Run the script using Python (or click the Play button in Visual Studio Code).
3. A brand new, beautifully sorted file named `[i000, t2002] Spells_Sorted.xml` will be generated instantly in the same directory.
4. Back up your original file, rename the new one by removing `_Sorted`, and you're good to go!

### Roadmap / Future Plans

- Create a graphical user interface (GUI) desktop application.
- Add explicit language selection settings.
- Expand functionality to support item files (Items.xml) and creature files.

### License

This project is licensed under the Modified MIT License for Non-Commercial Use - see the LICENSE file for details. Feel free to use, modify, and share it within the modding community for personal use!

