
from flask import Flask, render_template_string
import sqlite3
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).resolve().parents[2] / "IT_Inventory.db"

if not DATABASE.is_file():
    raise FileNotFoundError(f"Database niet gevonden: {DATABASE}")

@app.route("/")
def home():
    with sqlite3.connect(DATABASE) as db:
        voorraad = db.execute("""
            SELECT
                Apparaten.Merk,
                Apparaten.Soort,
                Locaties.Naam,
                Voorraad.Aantal
            FROM Apparaten
            LEFT JOIN Voorraad
                ON Apparaten.ApparaatID = Voorraad.ApparaatID
            LEFT JOIN Locaties
                ON Voorraad.LocatieID = Locaties.LocatieID
        """).fetchall()

    return render_template_string("""
        <h1>Eijerkamp IT Inventaris</h1>

        <input
            type="search"
            id="search"
            placeholder="Zoek apparaat, merk of locatie..."
        >

        <table border="1" cellpadding="10">
            <tr>
                <th>Merk</th>
                <th>Soort</th>
                <th>Locatie</th>
                <th>Aantal</th>
            </tr>

            {% for merk, soort, locatie, aantal in voorraad %}
            <tr>
                <td>{{ merk }}</td>
                <td>{{ soort }}</td>
                <td>{{ locatie }}</td>
                <td>{{ aantal }}</td>
            </tr>
            {% endfor %}
        </table>

        <script>
            document.getElementById("search").addEventListener("input", function() {
                document.querySelectorAll("table tr:not(:first-child)").forEach(row => {
                    row.style.display = row.textContent.toLowerCase().includes(
                        this.value.toLowerCase()
                    ) ? "" : "none";
                });
            });
        </script>
    """, voorraad=voorraad)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
