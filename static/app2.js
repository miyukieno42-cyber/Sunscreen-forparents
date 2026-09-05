document.addEventListener("DOMContentLoaded", function () {

    const questions = Array.from(
        document.querySelectorAll(".question")
    );

    const totalQuestions = questions.length;

    let currentIndex = 0;


    const currentQuestion = document.getElementById(
        "currentQuestion"
    );

    const totalQuestion = document.getElementById(
        "totalQuestions"
    );

    const progress = document.getElementById(
        "progress"
    );


    if (totalQuestion) {
        totalQuestion.textContent = totalQuestions;
    }


    // =====================================================
    // 質問表示
    // =====================================================

    function showQuestion(index) {

        questions.forEach(function (question, i) {

            question.classList.toggle(
                "active",
                i === index
            );

        });


        if (currentQuestion) {

            currentQuestion.textContent =
                index + 1;

        }


        if (progress) {

            const percentage =
                ((index + 1) / totalQuestions) * 100;

            progress.style.width =
                percentage + "%";

        }


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }


    // =====================================================
    // 必須チェック
    // =====================================================

    function validateQuestion(question) {

        const requiredInputs =
            question.querySelectorAll(
                "input[required], textarea[required], select[required]"
            );


        if (requiredInputs.length === 0) {

            return true;

        }


        for (const input of requiredInputs) {

            if (
                input.type === "radio" ||
                input.type === "checkbox"
            ) {

                const name =
                    input.name;

                const checked =
                    question.querySelector(
                        `input[name="${name}"]:checked`
                    );

                if (!checked) {

                    alert(
                        "回答を選択してください。"
                    );

                    return false;

                }

            } else {

                if (!input.value.trim()) {

                    alert(
                        "回答を入力してください。"
                    );

                    input.focus();

                    return false;

                }

            }

        }


        return true;

    }


    // =====================================================
    // 次へ
    // =====================================================

    document.querySelectorAll(
        ".next-button"
    ).forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const currentQuestionElement =
                    questions[currentIndex];


                if (
                    !validateQuestion(
                        currentQuestionElement
                    )
                ) {

                    return;

                }


                if (
                    currentIndex <
                    questions.length - 1
                ) {

                    currentIndex++;

                    showQuestion(
                        currentIndex
                    );

                }

            }
        );

    });


    // =====================================================
    // 戻る
    // =====================================================

    document.querySelectorAll(
        ".back-button"
    ).forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                if (currentIndex > 0) {

                    currentIndex--;

                    showQuestion(
                        currentIndex
                    );

                }

            }
        );

    });


    // =====================================================
    // Q3「その他」
    // =====================================================

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

        document
            .querySelectorAll(
                'input[name="use_timing"]'
            )
            .forEach(function (input) {

                input.addEventListener(
                    "change",
                    function () {

                        if (
                            useTimingOther.checked
                        ) {

                            useTimingOtherText.style.display =
                                "block";

                        } else {

                            useTimingOtherText.style.display =
                                "none";

                            useTimingOtherText.value =
                                "";

                        }

                    }
                );

            });

    }


    // =====================================================
    // Q5「その他」
    // =====================================================

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

        dislikeReasonOther.addEventListener(
            "change",
            function () {

                if (
                    dislikeReasonOther.checked
                ) {

                    dislikeReasonOtherText.style.display =
                        "block";

                } else {

                    dislikeReasonOtherText.style.display =
                        "none";

                    dislikeReasonOtherText.value =
                        "";

                }

            }
        );

    }


    // =====================================================
    // 初期表示
    // =====================================================

    showQuestion(
        currentIndex
    );

});
// Q6「その他」の表示・非表示
const parentProblemOther = document.getElementById("parentProblemOther");
const parentProblemOtherText = document.getElementById("parentProblemOtherText");

if (parentProblemOther && parentProblemOtherText) {
    parentProblemOther.addEventListener("change", function () {

        if (this.checked) {
            parentProblemOtherText.style.display = "block";
        } else {
            parentProblemOtherText.style.display = "none";
            parentProblemOtherText.value = "";
        }

    });
}
