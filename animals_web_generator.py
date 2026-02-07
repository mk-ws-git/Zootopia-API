import json
import requests
import os

API_URL = "https://api.api-ninjas.com/v1/animals"

def fetch_animals_from_api(animal_name):
    api_key = os.environ.get("NINJAS_API_KEY")
    if not api_key:
        raise RuntimeError("NINJAS_API_KEY is not set")

    response = requests.get(
        API_URL,
        params={"name": animal_name},
        headers={"X-Api-Key": api_key},
        timeout=20,
    )

    print("Status code:", response.status_code)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data
    return []


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


def main():
    """Prompt for user input, fetch animal data via API, and generate animals.html."""
    html_template = read_file("animals_template.html")

    animal_name = input("Enter a name of an animal: ").strip()
    while animal_name == "":
        animal_name = input("Enter a name of an animal: ").strip()

    animals = fetch_animals_from_api(animal_name)
    animals_output = build_animals_output(animals)

    if "__REPLACE_ANIMALS_INFO__" in html_template:
        new_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_output)
    else:
        if "</ul>" in html_template:
            new_html = html_template.replace("</ul>", animals_output + "\n</ul>", 1)
        else:
            new_html = html_template + "\n" + animals_output
    try:
        write_file("animals.html", new_html)
    except Exception as e:
        print("Failed to write animals.html:", e)
        raise

    write_file("animals.html", new_html)

    print("\nanimals.html has been sucessfully generated.")
    print("Animals shown:", len(animals))

if __name__ == '__main__':
    main()
