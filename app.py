from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

is_updating = False

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
      
def get_last_updated_time():
    try:
        modification_time = os.path.getmtime('data.db')
        last_updated = datetime.fromtimestamp(modification_time)
        return last_updated.strftime('%Y-%m-%d %H:%M')
    except OSError:
        return "Database file not found."

def check_database():
    database_exists = os.path.exists('data.db')
    if not database_exists:
        print("Database not found. Running wow_project.py to create the database...")
        try:
            subprocess.run(["python", "wow_project.py"], check=True)
        except subprocess.CalledProcessError as e:
            print("An error occurred while creating the database:", e)

def get_sorted_characters(sort_by, sort_order):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM data ORDER BY {sort_by} {sort_order}"
    cursor.execute(query)
    sorted_rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return sorted_rows

def fetch_latest_data():
    print("Fetching latest data...")
    try:
        subprocess.run(["python", "wow_project.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while fetching data:", e)

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    global is_updating
    if is_updating:
        print("Update already in progress.")
        return redirect(url_for('index'))
    
    is_updating = True
    print("Updating data...")
    try:
        subprocess.run(["python", "wow_project.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while updating data:", e)
    finally:
        is_updating = False

    return redirect(url_for('index'))


@app.route('/')
def index():
    last_updated = get_last_updated_time()
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
                           class_colors=class_colors, last_updated=last_updated)
    

if __name__ == '__main__':
    check_database()
    app.run(debug=True)
