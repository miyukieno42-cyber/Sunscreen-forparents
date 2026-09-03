const questions = document.querySelectorAll(".question");

let currentQuestion = 0;

const totalQuestions = questions.length;


/* =========================
   進捗表示
========================= */

function updateProgress() {

    const current = currentQuestion + 1;

    document.getElementById("currentQuestion").textContent = current;

    document.getElementById("totalQuestions").textContent = totalQuestions;

    const progress = (current / totalQuestions) * 100;

    document.getElementById("progress").style.width =
        progress + "%";
}


/* =========================
   質問表示
========================= */

function showQuestion(number) {

    questions.forEach((question, index) => {

        question.classList.remove("active");

        if (index === number) {
            question.classList.add("active");
        }

    });

    updateProgress();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


/* =========================
   次へボタン
========================= */

const nextButtons =
    document.querySelectorAll(".next-button");

nextButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const current =
            questions[currentQuestion];

        /*
         * 現在の質問にある
         * required の入力をチェック
         */
        const requiredInputs =
            current.querySelectorAll("input[required]");

        for (const input of requiredInputs) {

            if (!input.checkValidity()) {

                input.reportValidity();

                return;
            }
        }


        /*
         * Q1はチェックボックスなので
         * 1つ以上選ばれているか確認
         */
        if (current.dataset.question === "1") {

            const ageCheckboxes =
                current.querySelectorAll(
                    'input[name="child_age"]'
                );

            const ageChecked =
                Array.from(ageCheckboxes)
                    .some((checkbox) => checkbox.checked);

            if (!ageChecked) {

                alert("お子さんの年齢を1つ以上選んでください。");

                return;
            }
        }


        /*
         * Q3「その他」の入力チェック
         */
        if (current.dataset.question === "3") {

            const other =
                document.getElementById("useTimingOther");

            const otherText =
                document.getElementById("useTimingOtherText");

            if (
                other &&
                other.checked &&
                otherText.value.trim() === ""
            ) {

                alert("「その他」の内容を入力してください。");

                otherText.focus();

                return;
            }
        }


        /*
         * 次の質問へ
         */
        if (currentQuestion < totalQuestions - 1) {

            currentQuestion++;

            showQuestion(currentQuestion);
        }

    });

});


/* =========================
   戻るボタン
========================= */

const backButtons =
    document.querySelectorAll(".back-button");

backButtons.forEach((button) => {

    button.addEventListener("click", () => {

        if (currentQuestion > 0) {

            currentQuestion--;

            showQuestion(currentQuestion);
        }

    });

});


/* =========================
   フォーム送信
========================= */

const form =
    document.getElementById("surveyForm");

form.addEventListener("submit", (event) => {

    /*
     * Q9まで来て送信するときに
     * required項目を最終確認
     */
    if (!form.checkValidity()) {

        event.preventDefault();

        form.reportValidity();

        return;
    }


    /*
     * Q1の年齢を確認
     */
    const ageCheckboxes =
        document.querySelectorAll(
            'input[name="child_age"]'
        );

    const ageChecked =
        Array.from(ageCheckboxes)
            .some((checkbox) => checkbox.checked);

    if (!ageChecked) {

        event.preventDefault();

        alert("お子さんの年齢を1つ以上選んでください。");

        return;
    }


    /*
     * Q3のその他
     */
    const timingOther =
        document.getElementById("useTimingOther");

    const timingOtherText =
        document.getElementById("useTimingOtherText");

    if (
        timingOther &&
        timingOther.checked &&
        timingOtherText.value.trim() === ""
    ) {

        event.preventDefault();

        alert("「その他」の内容を入力してください。");

        timingOtherText.focus();

        return;
    }


    /*
     * Q5のその他
     */
    const reasonOther =
        document.getElementById("dislikeReasonOther");

    const reasonOtherText =
        document.getElementById("dislikeReasonOtherText");

    if (
        reasonOther &&
        reasonOther.checked &&
        reasonOtherText.value.trim() === ""
    ) {

        event.preventDefault();

        alert("「その他」の理由を入力してください。");

        reasonOtherText.focus();

        return;
    }

});


/* =========================
   Q3「その他」
========================= */

const useTimingOther =
    document.getElementById("useTimingOther");

const useTimingOtherText =
    document.getElementById("useTimingOtherText");

if (useTimingOther && useTimingOtherText) {

    useTimingOther.addEventListener("change", function () {

        if (this.checked) {

            useTimingOtherText.style.display = "block";

            useTimingOtherText.focus();

        } else {

            useTimingOtherText.style.display = "none";

            useTimingOtherText.value = "";
        }

    });


    /*
     * Q3の他のラジオボタンを選んだら
     * その他欄を隠す
     */
    const timingRadios =
        document.querySelectorAll(
            'input[name="use_timing"]'
        );

    timingRadios.forEach((radio) => {

        radio.addEventListener("change", function () {

            if (this.value !== "その他") {

                useTimingOtherText.style.display =
                    "none";

                useTimingOtherText.value = "";
            }

        });

    });

}


/* =========================
   Q5「その他」
========================= */

const dislikeReasonOther =
    document.getElementById("dislikeReasonOther");

const dislikeReasonOtherText =
    document.getElementById("dislikeReasonOtherText");

if (
    dislikeReasonOther &&
    dislikeReasonOtherText
) {

    dislikeReasonOther.addEventListener(
        "change",
        function () {

            if (this.checked) {

                dislikeReasonOtherText.style.display =
                    "block";

                dislikeReasonOtherText.focus();

            } else {

                dislikeReasonOtherText.style.display =
                    "none";

                dislikeReasonOtherText.value = "";
            }

        }
    );

}


/* =========================
   最初の質問を表示
========================= */

showQuestion(0);
