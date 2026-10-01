/* quiz.js — 共享的小测组件
 *
 * 用法：
 * <div class="quiz">
 *   <p class="q"><span class="num">Q1</span> 题干…</p>
 *   <button class="quiz-option">选项 A</button>
 *   <button class="quiz-option" data-correct="true">选项 B（正确）</button>
 *   <p class="feedback" data-ok="答对了！解释…" data-no="再想想：解释…"></p>
 * </div>
 *
 * 组件会打乱选项顺序，因此"正确项"的位置不会泄露答案。
 */
(function () {
  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function initQuiz(quiz) {
    var options = Array.prototype.slice.call(quiz.querySelectorAll(".quiz-option"));
    var feedback = quiz.querySelector(".feedback");
    if (!options.length) return;

    // 打乱顺序
    shuffle(options).forEach(function (o) { quiz.appendChild(o); });

    var answered = false;
    options.forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (answered) return;
        answered = true;
        var correct = btn.getAttribute("data-correct") === "true";
        options.forEach(function (o) { o.disabled = true; });
        btn.classList.add(correct ? "correct" : "wrong");
        if (!correct) {
          options.forEach(function (o) {
            if (o.getAttribute("data-correct") === "true") o.classList.add("correct");
          });
        }
        if (feedback) {
          feedback.textContent = correct
            ? (feedback.getAttribute("data-ok") || "答对了。")
            : (feedback.getAttribute("data-no") || "不对。看看绿色高亮的正确答案。");
          feedback.classList.add("show", correct ? "ok" : "no");
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll(".quiz"), initQuiz);
  });
})();
