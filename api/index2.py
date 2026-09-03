from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import csv
import io
import os
from datetime import datetime

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

DATABASE = "/tmp/parent_sunscreen_survey.db"


def get_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            child_age TEXT,
            sunscreen_use TEXT,
            use_timing TEXT,
            use_timing_other TEXT,
            child_dislike TEXT,
            dislike_reason TEXT,
            dislike_reason_other TEXT,
            parent_problem TEXT,
            how_to_apply TEXT,
            want_self_apply TEXT,
            child_idea TEXT
        )
    """)

    conn.commit()

    return conn


@app.route("/")
def index():
    return render_template("index2.html")


@app.route("/submit", methods=["POST"])
def submit():

    # Q1：お子さんの年齢
    child_age = request.form.getlist("child_age")

    # Q2：日焼け止めを使っているか
    sunscreen_use = request.form.get("sunscreen_use", "")

    # Q3：いつ使うか
    use_timing = request.form.get("use_timing", "")
    use_timing_other = request.form.get("use_timing_other", "")

    # Q4：子どもが嫌がるか
    child_dislike = request.form.get("child_dislike", "")

    # Q5：嫌がる理由
    dislike_reason = request.form.getlist("dislike_reason")
    dislike_reason_other = request.form.get("dislike_reason_other", "")

    # Q6：親が困っていること
    parent_problem = request.form.get("parent_problem", "")

    # Q7：嫌がる子への塗り方
    how_to_apply = request.form.get("how_to_apply", "")

    # Q8：自分から塗りたくなる日焼け止め
    want_self_apply = request.form.get("want_self_apply", "")

    # Q9：子どもが喜びそうな工夫
    child_idea = request.form.get("child_idea", "")

    # 複数選択をカンマ区切りで保存
    child_age_text = ", ".join(child_age)
    dislike_reason_text = ", ".join(dislike_reason)

    # 「その他」の内容を回答に含める
    if use_timing == "その他" and use_timing_other:
        use_timing_text = f"その他: {use_timing_other}"
    else:
        use_timing_text = use_timing

    if "その他" in dislike_reason and dislike_reason_other:
        if dislike_reason_text:
            dislike_reason_text += f", その他: {dislike_reason_other}"
        else:
            dislike_reason_text = f"その他: {dislike_reason_other}"

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()

    conn.execute(
        """
        INSERT INTO responses (
            created_at,
            child_age,
            sunscreen_use,
            use_timing,
            use_timing_other,
            child_dislike,
            dislike_reason,
            dislike_reason_other,
            parent_problem,
            how_to_apply,
            want_self_apply,
            child_idea
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            created_at,
            child_age_text,
            sunscreen_use,
            use_timing_text,
            use_timing_other,
            child_dislike,
            dislike_reason_text,
            dislike_reason_other,
            parent_problem,
            how_to_apply,
            want_self_apply,
            child_idea
        )
    )

    conn.commit()
    conn.close()

    return redirect(url_for("thanks"))


@app.route("/thanks")
def thanks():
    return render_template("thanks2.html")


@app.route("/download_csv")
def download_csv():

    if not os.path.exists(DATABASE):
        return "まだ回答データがありません。", 200

    conn = get_db()

    cursor = conn.execute(
        """
        SELECT
            id,
            created_at,
            child_age,
            sunscreen_use,
            use_timing,
            use_timing_other,
            child_dislike,
            dislike_reason,
            dislike_reason_other,
            parent_problem,
            how_to_apply,
            want_self_apply,
            child_idea
        FROM responses
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "回答日時",
        "お子さんの年齢",
        "日焼け止めの使用状況",
        "日焼け止めを使うタイミング",
        "使うタイミング・その他",
        "子どもが嫌がること",
        "嫌がる理由",
        "嫌がる理由・その他",
        "親が困っていること",
        "嫌がる子どもへの塗り方",
        "自分から塗りたくなる日焼け止めを使ってみたいか",
        "子どもが喜びそうな工夫"
    ])

    writer.writerows(rows)

    response = Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8"
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=parent_sunscreen_survey.csv"

    return response


if __name__ == "__main__":
    app.run(debug=True)
