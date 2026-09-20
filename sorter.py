import re
import os
import locale
import ctypes

# Slownik jezykow (Wykrywanie wersji jezykowej systemu)
LOCALES = {
    "pl": {
        "loading": "Wczytywanie pliku XML...",
        "err_not_found": "Blad: Nie znaleziono pliku w sciezce:\n{}",
        "err_structure": "Blad: Plik nie posiada prawidlowej struktury ze znacznikami <Spells> i </Spells>.",
        "err_no_spells": "Blad: Nie znaleziono czarow dopasowanych do wzorca.",
        "sorting": "Znaleziono {} czarow. Analizowanie poziomow i sortowanie...",
        "success": "\nSUKCES!",
        "desc": "Czary zostaly ulozone wedlug Nazwy -> Poziomu (Level) -> ID.",
        "saved": "Plik wynikowy: '{}'"
    },
    "en": {
        "loading": "Loading XML file...",
        "err_not_found": "Error: File not found in path:\n{}",
        "err_structure": "Error: The file does not have a valid structure with <Spells> and </Spells> tags.",
        "err_no_spells": "Error: No spells matching the pattern were found.",
        "sorting": "Found {} spells. Analyzing levels and sorting...",
        "success": "\nSUCCESS!",
        "desc": "Spells have been sorted by Name -> Level -> ID.",
        "saved": "Output file: '{}'"
    }
}

def get_text(key, *args):
    # Zaawansowane wykrywanie jezyka interfejsu Windowsa (dziala tez w VS Code)
    try:
        windll = ctypes.windll.kernel32
        user_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        lang = "pl" if "pl" in user_lang.lower() else "en"
    except:
        # Metoda awaryjna w razie bledu lub innego systemu niz Windows
        sys_lang = locale.getlocale()
        lang = "pl" if sys_lang and "Polish" in sys_lang else "en"
        
    text = LOCALES[lang].get(key, LOCALES["en"][key])
    return text.format(*args) if args else text

def sort_spellforce_xml():
    # Pobiera folder, w ktorym znajduje sie plik sorter.py
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Laczy folder z poprawna nazwa pliku XML
    input_file = os.path.join(current_folder, "[i000, t2002] Spells.xml")
    output_file = os.path.join(current_folder, "[i000, t2002] Spells_Sorted.xml")

    if not os.path.exists(input_file):
        print(get_text("err_not_found", input_file))
        return

    print(get_text("loading"))
    with open(input_file, "r", encoding="utf-8") as f:
        xml_data = f.read()

    if "<Spells>" not in xml_data or "</Spells>" not in xml_data:
        print(get_text("err_structure"))
        return
        
    header_part = xml_data.split("<Spells>")[0] + "<Spells>"
    footer_part = "</Spells>" + xml_data.split("</Spells>")[-1]

    # Wyrazenie pobiera: caly blok (0), nazwe czaru (1), ID czaru (2)
    pattern = re.compile(r"(\s*<!--SpellLine:\s*([^\s-]+)-->\s*<Spell\s+ID=\"(\d+)\".*?</Spell>)", re.DOTALL)
    matches = pattern.findall(xml_data)

    if not matches:
        print(get_text("err_no_spells"))
        return

    print(get_text("sorting", len(matches)))

    # Przygotowujemy liste do zaawansowanego sortowania po strukturze wewnetrznej
    enriched_matches = []
    for match in matches:
        full_text = match[0]
        spell_line_name = match[1].lower()
        spell_id = int(match[2])
        
        # Wyciągamy wartosc Level="..." z sekcji RequiredAbilities danego czaru
        level_search = re.search(r'Level="(\d+)"', full_text)
        spell_level = int(level_search.group(1)) if level_search else 0
        
        enriched_matches.append((full_text, spell_line_name, spell_level, spell_id))

    # SORTOWANIE TRZYETAPOWE: Nazwa -> Poziom (Level) -> ID
    sorted_enriched = sorted(enriched_matches, key=lambda x: (x[1], x[2], x[3]))
    
    # Wyciagamy z powrotem sam czysty tekst XML
    sorted_spells_text = "".join([item[0] for item in sorted_enriched])
    final_xml = header_part + sorted_spells_text + "\n\t" + footer_part

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_xml)

    print(get_text("success"))
    print(get_text("desc"))
    print(get_text("saved", output_file))

if __name__ == "__main__":
    sort_spellforce_xml()
