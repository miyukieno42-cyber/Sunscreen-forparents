document.addEventListener("DOMContentLoaded", () => {

    const questions =
        document.querySelectorAll(".question");

    const totalQuestions =
        questions.length;

    let currentQuestion = 0;


    /* =====================================================
       プログレス更新
    ===================================================== */

    function updateProgress() {

        const current =
            currentQuestion + 1;

        const currentQuestionElement =
            document.getElementById("currentQuestion");

        const totalQuestionElement =
            document.getElementById("totalQuestions");

        const progressElement =
            document.getElementById("progress");


        if (currentQuestionElement) {
            currentQuestionElement.textContent =
                current;
        }

        if (totalQuestionElement) {
            totalQuestionElement.textContent =
                totalQuestions;
        }

        if (progressElement) {

            const percentage =
                (current / totalQuestions) * 100;

            progressElement.style.width =
                percentage + "%";
        }
    }


    /* =====================================================
       質問表示
    ===================================================== */

    function showQuestion(index) {

        questions.forEach((question, i) => {

            question.classList.toggle(
                "active",
                i === index
            );

        });


        updateProgress();


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }


    /* =====================================================
       現在の質問の必須項目チェック
    ===================================================== */

    function validateCurrentQuestion() {

        const current =
            questions[currentQuestion];


        if (!current) {
            return true;
        }


        /* -------------------------------------------------
           required
        ------------------------------------------------- */

        const requiredInputs =
            current.querySelectorAll(
                "input[required]"
            );


        for (const input of requiredInputs) {

            if (!input.checkValidity()) {

                input.reportValidity();

                return false;
            }
        }


        /* -------------------------------------------------
           Q3「その他」
        ------------------------------------------------- */

        if (
            current.dataset.question === "3"
        ) {

            const other =
                document.getElementById(
                    "useTimingOther"
                );

            const otherText =
                document.getElementById(
                    "useTimingOtherText"
                );


            if (
                other &&
                other.checked &&
                otherText &&
                otherText.value.trim() === ""
            ) {

                alert(
                    "「その他」の内容を入力してください。"
                );

                otherText.focus();

                return false;
            }
        }


        /* -------------------------------------------------
           Q5「その他」
        ------------------------------------------------- */

        if (
            current.dataset.question === "5"
        ) {

            const other =
                document.getElementById(
                    "dislikeReasonOther"
                );

            const otherText =
                document.getElementById(
                    "dislikeReasonOtherText"
                );


            if (
                other &&
                other.checked &&
                otherText &&
                otherText.value.trim() === ""
            ) {

                alert(
                    "「その他」の理由を入力してください。"
                );

                otherText.focus();

                return false;
            }
        }


        return true;
    }


    /* =====================================================
       次へ
    ===================================================== */

    const nextButtons =
        document.querySelectorAll(
            ".next-button"
        );


    nextButtons.forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                if (
                    !validateCurrentQuestion()
                ) {
                    return;
                }


                if (
                    currentQuestion <
                    totalQuestions - 1
                ) {

                    currentQuestion++;

                    showQuestion(
                        currentQuestion
                    );
                }

            }
        );

    });


    /* =====================================================
       戻る
    ===================================================== */

    const backButtons =
        document.querySelectorAll(
            ".back-button"
        );


    backButtons.forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                if (
                    currentQuestion > 0
                ) {

                    currentQuestion--;

                    showQuestion(
                        currentQuestion
                    );
                }

            }
        );

    });


    /* =====================================================
       Q3「その他」
    ===================================================== */

    const useTimingOther =
        document.getElementById(
            "useTimingOther"
        );

    const useTimingOtherText =
        document.getElementById(
            "useTimingOtherText"
        );


    if (
        useTimingOther &&
        useTimingOtherText
    ) {

        useTimingOtherText.style.display =
            "none";


        useTimingOther.addEventListener(
            "change",
            function () {

                if (this.checked) {

                    useTimingOtherText.style.display =
                        "block";

                    useTimingOtherText.focus();

                } else {

                    useTimingOtherText.style.display =
                        "none";

                    useTimingOtherText.value =
                        "";
                }

            }
        );


        const timingRadios =
            document.querySelectorAll(
                'input[name="childhood_timing"]'
            );


        timingRadios.forEach((radio) => {

            radio.addEventListener(
                "change",
                function () {

                    if (
                        this.value !== "その他"
                    ) {

                        useTimingOtherText.style.display =
                            "none";

                        useTimingOtherText.value =
                            "";
                    }

                }
            );

        });

    }


    /* =====================================================
       Q5「その他」
    ===================================================== */

    const dislikeReasonOther =
        document.getElementById(
            "dislikeReasonOther"
        );

    const dislikeReasonOtherText =
        document.getElementById(
            "dislikeReasonOtherText"
        );


    if (
        dislikeReasonOther &&
        dislikeReasonOtherText
    ) {

        dislikeReasonOtherText.style.display =
            "none";


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

                    dislikeReasonOtherText.value =
                        "";
                }

            }
        );

    }


    /* =====================================================
       フォーム送信
    ===================================================== */

    const form =
        document.getElementById(
            "surveyForm"
        );


    if (form) {

        form.addEventListener(
            "submit",
            (event) => {

                if (
                    !validateCurrentQuestion()
                ) {

                    event.preventDefault();

                    return;
                }


                if (
                    !form.checkValidity()
                ) {

                    event.preventDefault();

                    form.reportValidity();

                    return;
                }


                /* -----------------------------------------
                   Q3 その他
                ----------------------------------------- */

                const timingOther =
                    document.getElementById(
                        "useTimingOther"
                    );

                const timingOtherText =
                    document.getElementById(
                        "useTimingOtherText"
                    );


                if (
                    timingOther &&
                    timingOther.checked &&
                    timingOtherText &&
                    timingOtherText.value.trim() === ""
                ) {

                    event.preventDefault();

                    alert(
                        "「その他」の内容を入力してください。"
                    );

                    timingOtherText.focus();

                    return;
                }


                /* -----------------------------------------
                   Q5 その他
                ----------------------------------------- */

                const reasonOther =
                    document.getElementById(
                        "dislikeReasonOther"
                    );

                const reasonOtherText =
                    document.getElementById(
                        "dislikeReasonOtherText"
                    );


                if (
                    reasonOther &&
                    reasonOther.checked &&
                    reasonOtherText &&
                    reasonOtherText.value.trim() === ""
                ) {

                    event.preventDefault();

                    alert(
                        "「その他」の理由を入力してください。"
                    );

                    reasonOtherText.focus();

                    return;
                }

            }
        );

    }


    /* =====================================================
       最初の質問
    ===================================================== */

    showQuestion(0);

});
