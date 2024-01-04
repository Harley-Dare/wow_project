from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

class_colors = {
    "Warrior": "#C79C6E",
    "Paladin": "#F58CBA",
    "Hunter": "#ABD473",
    "Rogue": "#FFF569",
    "Priest": "#FFFFFF",
    "Death Knight": "#C41F3B",
    "Shaman": "#0070DE",
    "Mage": "#69CCF0",
    "Warlock": "#9482C9",
    "Monk": "#00FF96",
    "Druid": "#FF7D0A",
    "Demon Hunter": "#A330C9",
    "Evoker": "#33937F"
}

def get_sorted_characters(sort_by, sort_order):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM data ORDER BY {sort_by} {sort_order}"
    cursor.execute(query)
    sorted_rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return sorted_rows



@app.route('/')
def index():
    # Default sort column and order
    sort_by = request.args.get('sort', 'item_level')
    sort_order = request.args.get('order', 'DESC')

    # Check what was the previous sort column and order
    prev_sort_by = request.args.get('prev_sort')
    prev_sort_order = request.args.get('prev_order', 'ASC')

    # Toggle the sort order if the same sort column is clicked
    if prev_sort_by == sort_by:
        sort_order = 'DESC' if prev_sort_order == 'ASC' else 'ASC'

    characters = get_sorted_characters(sort_by, sort_order)
    return render_template('index.html', characters=characters,
                           sort_by=sort_by, sort_order=sort_order,
                           prev_sort=sort_by, prev_order=sort_order,
                           class_colors=class_colors)
    




if __name__ == '__main__':
    app.run(debug=True)
