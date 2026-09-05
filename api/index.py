from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import csv
import io
from datetime import datetime
import os


# =========================================================
# フォルダ設定
# =========================================================

# このファイルは /api/index.py にある
API_DIR = os.path.dirname(os.path.abspath(__file__))

# プロジェクトのルート
# /api の1つ上
BASE_DIR = os.path.dirname(API_DIR)

TEMPLATE_DIR = os.path.join(
    BASE_DIR,
    "templates"
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    "static"
)


# =========================================================
# Flask
# =========================================================

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)


# =========================================================
# データベース
# =========================================================

DATABASE = "/tmp/childhood_sunscreen_survey.db"


def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,

            age TEXT,

            childhood_use TEXT,
            childhood_timing TEXT,
            childhood_timing_other TEXT,

            childhood_dislike TEXT,

            dislike_reason TEXT,
            dislike_reason_other TEXT,

            current_use TEXT,
            current_problem TEXT,

            ideal_sunscreen TEXT
        )
    """)

    conn.commit()

    return conn


# =========================================================
# トップページ
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index2.html"
    )


# =========================================================
# アンケート送信
# =========================================================

@app.route("/submit", methods=["POST"])
def submit():

    # -----------------------------------------------------
    # Q1
    # -----------------------------------------------------

    age = request.form.get(
        "age",
        ""
    )


    # -----------------------------------------------------
    # Q2
    # -----------------------------------------------------

    childhood_use = request.form.get(
        "childhood_use",
        ""
    )


    # -----------------------------------------------------
    # Q3
    # -----------------------------------------------------

    childhood_timing = request.form.get(
        "childhood_timing",
        ""
    )

    childhood_timing_other = request.form.get(
        "childhood_timing_other",
        ""
    )


    if (
        childhood_timing == "その他"
        and childhood_timing_other.strip()
    ):

        childhood_timing_text = (
            "その他: "
            + childhood_timing_other.strip()
        )

    else:

        childhood_timing_text = (
            childhood_timing
        )


    # -----------------------------------------------------
    # Q4
    # -----------------------------------------------------

    childhood_dislike = request.form.get(
        "childhood_dislike",
        ""
    )


    # -----------------------------------------------------
    # Q5
    # -----------------------------------------------------

    dislike_reason = request.form.getlist(
        "dislike_reason"
    )

    dislike_reason_other = request.form.get(
        "dislike_reason_other",
        ""
    )

    dislike_reason_text = ", ".join(
        dislike_reason
    )


    if (
        "その他" in dislike_reason
        and dislike_reason_other.strip()
    ):

        if dislike_reason_text:

            dislike_reason_text += (
                ", その他: "
                + dislike_reason_other.strip()
            )

        else:

            dislike_reason_text = (
                "その他: "
                + dislike_reason_other.strip()
            )


    # -----------------------------------------------------
    # Q6
    # -----------------------------------------------------

    current_use = request.form.get(
        "current_use",
        ""
    )


    # -----------------------------------------------------
    # Q7
    # -----------------------------------------------------

    current_problem = request.form.get(
        "current_problem",
        ""
    )


    # -----------------------------------------------------
    # Q8
    # -----------------------------------------------------

    ideal_sunscreen = request.form.get(
        "ideal_sunscreen",
        ""
    )


    # -----------------------------------------------------
    # 回答日時
    # -----------------------------------------------------

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # -----------------------------------------------------
    # DB保存
    # -----------------------------------------------------

    conn = get_db()

    conn.execute(
        """
        INSERT INTO responses (
            created_at,
            age,
            childhood_use,
            childhood_timing,
            childhood_timing_other,
            childhood_dislike,
            dislike_reason,
            dislike_reason_other,
            current_use,
            current_problem,
            ideal_sunscreen
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            created_at,
            age,
            childhood_use,
            childhood_timing_text,
            childhood_timing_other,
            childhood_dislike,
            dislike_reason_text,
            dislike_reason_other,
            current_use,
            current_problem,
            ideal_sunscreen
        )
    )

    conn.commit()

    conn.close()


    return redirect(
        url_for("thanks")
    )


# =========================================================
# 完了ページ
# =========================================================

@app.route("/thanks")
def thanks():

    return render_template(
        "thanks2.html"
    )


# =========================================================
# CSVダウンロード
# =========================================================

@app.route("/download_csv")
def download_csv():

    if not os.path.exists(DATABASE):

        return (
            "まだ回答データがありません。",
            200
        )


    conn = get_db()

    cursor = conn.execute(
        """
        SELECT
            id,
            created_at,
            age,
            childhood_use,
            childhood_timing,
            childhood_timing_other,
            childhood_dislike,
            dislike_reason,
            dislike_reason_other,
            current_use,
            current_problem,
            ideal_sunscreen
        FROM responses
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    conn.close()


    output = io.StringIO(
        newline=""
    )

    writer = csv.writer(output)


    writer.writerow([
        "ID",
        "回答日時",
        "年代",
        "子どものころ日焼け止めを使っていたか",
        "子どものころ使っていたタイミング",
        "タイミング・その他",
        "子どものころ日焼け止めを塗るのが好きだったか",
        "嫌だった理由",
        "嫌だった理由・その他",
        "現在の日焼け止め使用状況",
        "現在困っていること",
        "こんな日焼け止めなら使ってみたい"
    ])


    writer.writerows(rows)


    csv_data = "\ufeff" + output.getvalue()


    response = Response(
        csv_data,
        mimetype="text/csv"
    )


    response.headers[
        "Content-Disposition"
    ] = (
        "attachment; "
        "filename=childhood_sunscreen_survey.csv"
    )


    return response


# =========================================================
# Vercel / Flask
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
