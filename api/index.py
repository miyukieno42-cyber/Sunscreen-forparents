from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import csv
import io
from datetime import datetime
import os


# =========================================================
# パス設定
# =========================================================

# このファイルは
# /api/index.py
# にあります。

API_DIR = os.path.dirname(os.path.abspath(__file__))

# 1つ上がプロジェクトのルート
BASE_DIR = os.path.dirname(API_DIR)

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")


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

# Vercelではローカルファイルへの保存は永続DBとして使えません。
# 今回はまずアンケートを動かすことを優先した簡易保存です。

DATABASE = "/tmp/childhood_sunscreen_survey.db"


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


# =========================================================
# トップページ
# =========================================================

@app.route("/")
def index():

    return render_template("index2.html")


# =========================================================
# アンケート送信
# =========================================================

@app.route("/submit", methods=["POST"])
def submit():

    # -----------------------------------------------------
    # Q1
    # お子さんの年齢
    # -----------------------------------------------------

    child_age = request.form.getlist(
        "child_age"
    )

    child_age_text = ", ".join(
        child_age
    )


    # -----------------------------------------------------
    # Q2
    # 日焼け止めを使っていますか？
    # -----------------------------------------------------

    sunscreen_use = request.form.get(
        "sunscreen_use",
        ""
    )


    # -----------------------------------------------------
    # Q3
    # いつ使っていますか？
    # -----------------------------------------------------

    use_timing = request.form.get(
        "use_timing",
        ""
    )

    use_timing_other = request.form.get(
        "use_timing_other",
        ""
    )


    # -----------------------------------------------------
    # Q4
    # 嫌がることがありますか？
    # -----------------------------------------------------

    child_dislike = request.form.get(
        "child_dislike",
        ""
    )


    # -----------------------------------------------------
    # Q5
    # 嫌がる理由
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
　 　# 親として困っていること
　　 # -----------------------------------------------------

　　　parent_problem = request.form.getlist(
       "parent_problem"
   )

parent_problem_other = request.form.get(
    "parent_problem_other",
    ""
)

parent_problem_text = ", ".join(
    parent_problem
)

if (
    "その他" in parent_problem
    and parent_problem_other.strip()
):

    if parent_problem_text:

        parent_problem_text += (
            ", その他: "
            + parent_problem_other.strip()
        )

    else:

        parent_problem_text = (
            "その他: "
            + parent_problem_other.strip()
        )
        
    # -----------------------------------------------------
    # Q7
    # どのように塗っていますか？
    # -----------------------------------------------------

    how_to_apply = request.form.get(
        "how_to_apply",
        ""
    )


    # -----------------------------------------------------
    # Q8
    # 自分から塗りたくなる日焼け止め
    # -----------------------------------------------------

    want_self_apply = request.form.get(
        "want_self_apply",
        ""
    )


    # -----------------------------------------------------
    # Q9
    # どんな工夫があったら喜ぶ？
    # -----------------------------------------------------

    child_idea = request.form.get(
        "child_idea",
        ""
    )


    # -----------------------------------------------------
    # 回答日時
    # -----------------------------------------------------

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # -----------------------------------------------------
    # データ保存
    # -----------------------------------------------------

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
            use_timing,
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


    # -----------------------------------------------------
    # 完了画面へ
    # -----------------------------------------------------

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


    output = io.StringIO(
        newline=""
    )

    writer = csv.writer(output)


    writer.writerow([
        "ID",
        "回答日時",
        "お子さんの年齢",
        "日焼け止めを使っていますか",
        "使用タイミング",
        "使用タイミング・その他",
        "日焼け止めを嫌がること",
        "嫌がる理由",
        "嫌がる理由・その他",
        "親として困っていること",
        "どのように塗っているか",
        "自分から塗りたくなる日焼け止め",
        "あったら嬉しい工夫"
    ])


    writer.writerows(rows)


    # Excelで文字化けしにくいようにBOMを追加
    csv_data = "\ufeff" + output.getvalue()


    response = Response(
        csv_data,
        mimetype="text/csv"
    )


    response.headers[
        "Content-Disposition"
    ] = (
        "attachment; "
        "filename=child_sunscreen_survey.csv"
    )


    return response


# =========================================================
# ローカル実行用
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
