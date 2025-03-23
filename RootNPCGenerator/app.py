from flask import Flask, render_template
from npc_generator import initialize_data

app = Flask(__name__)


@app.route("/")
def npc_generator():
    name_enums, species_enums, drive_enums, harm_tracks = initialize_data()
    species_options = []
    for species in species_enums:
        species_option = {
            "id": species.name,
            "display": species.name.title(),
            "value": species.name,
        }
        species_options.append(species_option)

    harm_track_options = []
    for key, value in harm_tracks.items():
        harm_track_option = {"id": key, "display": key.title(), "value": key}
        harm_track_options.append(harm_track_option)

    return render_template(
        "npc_generator.html",
        species_options=species_options,
        harm_track_options=harm_track_options,
    )


if __name__ == "__main__":
    app.run()
