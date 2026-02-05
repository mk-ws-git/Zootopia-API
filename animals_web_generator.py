import json


def get_nested_value(obj, keys):
    """Return nested dict value or None."""
    current = obj
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def serialize_field(label, value):
    """Return one <li> field line or '' if missing."""
    if value is None:
        return ""
    if isinstance(value, str) and value.strip() == "":
        return ""
    return (
        '      <li class="card__list-item">'
        "<strong>" + label + ":</strong> "
        + str(value)
        + "</li>\n"
    )


def serialize_animal(animal_obj):
    """Return one animal card as HTML."""
    output = ""

    name = animal_obj.get("name")
    scientific_name = get_nested_value(animal_obj, ["taxonomy", "scientific_name"])
    characteristics = animal_obj.get("characteristics", {})
    locations = animal_obj.get("locations", [])

    output += '<li class="cards__item">\n'

    if name:
        output += '  <div class="card__title">' + name + "</div>\n"

    if scientific_name:
        output += '  <div class="card__subtitle"><em>' + scientific_name + "</em></div>\n"

    output += '  <div class="card__text">\n'
    output += '    <ul class="card__list">\n'

    output += serialize_field("Diet", characteristics.get("diet"))

    if isinstance(locations, list) and len(locations) > 0:
        output += serialize_field("Locations", ", ".join(locations))

    output += serialize_field("Type", characteristics.get("type"))
    output += serialize_field("Group", characteristics.get("group"))
    output += serialize_field("Habitat", characteristics.get("habitat"))
    output += serialize_field("Lifespan", characteristics.get("lifespan"))
    output += serialize_field("Top speed", characteristics.get("top_speed"))
    output += serialize_field("Distinctive feature", characteristics.get("distinctive_feature"))
    output += serialize_field("Temperament", characteristics.get("temperament"))
    output += serialize_field("Skin type", characteristics.get("skin_type"))

    output += "    </ul>\n"
    output += "  </div>\n"
    output += "</li>\n"

    return output


def build_animals_output(animals):
    """Return HTML for all animal cards."""
    output = ""
    sorted_animals = sorted(animals, key=lambda a: a.get("name", "").lower())

    for animal_obj in sorted_animals:
        output += serialize_animal(animal_obj)
        output += "\n"

    return output


def read_file(filepath):
    """Read text file content."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filepath, content):
    """Write text file content."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def get_skin_types(animals):
    """Return a sorted list of unique skin_type values."""
    skin_types_set = set()

    for animal in animals:
        if "characteristics" in animal and "skin_type" in animal["characteristics"]:
            skin_type = animal["characteristics"]["skin_type"]
            if isinstance(skin_type, str) and skin_type.strip() != "":
                skin_types_set.add(skin_type.strip())

    return sorted(list(skin_types_set))


def filter_by_skin_type(animals, selected_skin_type):
    """Return only animals that match the selected skin_type."""
    filtered = []

    for animal in animals:
        if "characteristics" in animal and "skin_type" in animal["characteristics"]:
            skin_type = animal["characteristics"]["skin_type"]
            # compare trimmed values so minor whitespace differences don't prevent a match
            if isinstance(skin_type, str) and isinstance(selected_skin_type, str) and \
               skin_type.strip() == selected_skin_type:
                filtered.append(animal)

    return filtered


def main():
    """Prompt for skin_type, then generate animals.html."""
    animals = json.loads(read_file("animals_data.json"))
    html_template = read_file("animals_template.html")

    # 1) Show available skin types
    skin_types = get_skin_types(animals)

    print("Available skin_type values:")
    for skin_type in skin_types:
        print("-", skin_type)

    # Animals missing skin_type will NOT be included in filtered results.
    print("\nNote: animals with missing skin_type will be excluded.\n")

    # 2) Gather user input
    selected = input("Enter a skin_type from the list above: ").strip()

    # Validate user input
    while selected not in skin_types:
        print("\nThat skin_type is not in the list.")
        selected = input("Enter a skin_type from the list above: ").strip()

    # 3) Filter animals
    filtered_animals = filter_by_skin_type(animals, selected)

    # 4) Build HTML
    animals_output = build_animals_output(filtered_animals)

    # Optional: show which filter was used by replacing a placeholder if you have one
    # Make this defensive: ensure new_html is always defined even if placeholder missing
    if "__REPLACE_ANIMALS_INFO__" in html_template:
        new_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_output)
    else:
        # try to insert before the first closing </ul> (the cards list)
        if "</ul>" in html_template:
            new_html = html_template.replace("</ul>", animals_output + "\n</ul>", 1)
        else:
            # fallback: append the animals output to the end of the template
            new_html = html_template + "\n" + animals_output

    # 5) Write output file (wrapped for clearer error message on failure)
    try:
        write_file("animals.html", new_html)
    except Exception as e:
        print("Failed to write animals.html:", e)
        raise

    print("\nanimals.html has been created.")
    print("Filter used: skin_type =", selected)
    print("Animals shown:", len(filtered_animals))


if __name__ == '__main__':
    main()
