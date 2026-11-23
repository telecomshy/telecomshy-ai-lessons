/* theme-b.js — 为 B · 三块屏生成左侧状态轨
 *
 * 只在 body[data-track] 的课程页运行；不改正文、不改 md。
 * 生成结构：.wrap.lesson → aside.lesson-rail + header.lesson-head + div.sheet
 * 没有脚本时，页面保持 base.css 的单栏样式。
 */
(function () {
  "use strict";

  var TRACKS = {
    llm: { name: "LLM 底层" },
    agent: { name: "Agent 篇" },
    rag: { name: "RAG" },
    index: { name: "课程目录" },
    ref: { name: "速查 / Reference" }
  };

  function boot() {
    var body = document.body;
    var track = body.getAttribute("data-track");
    if (!TRACKS[track]) return;

    var wrap = document.querySelector(".wrap");
    if (!wrap || wrap.classList.contains("lesson")) return;

    var meta = wrap.querySelector(".lesson-meta");
    var h1 = wrap.querySelector("h1");
    if (!h1) return;
    if (!meta) {
      meta = document.createElement("div");
      meta.className = "lesson-meta";
      meta.textContent = TRACKS[track].name;
      wrap.insertBefore(meta, h1);
    }

    /* 1. 页眉：meta + h1 + subtitle（deep 页才有） */
    var subtitle = null;
    var next = h1.nextElementSibling;
    if (next && next.classList.contains("subtitle")) subtitle = next;

    var head = document.createElement("header");
    head.className = "lesson-head";
    wrap.insertBefore(head, wrap.firstElementChild);
    head.appendChild(meta);
    head.appendChild(h1);
    if (subtitle) head.appendChild(subtitle);

    /* 2. 正文：其余元素整体装进 sheet，顺序不变 */
    var sheet = document.createElement("div");
    sheet.className = "sheet";
    wrap.appendChild(sheet);
    Array.prototype.slice.call(wrap.children).forEach(function (el) {
      if (el === head || el === sheet) return;
      sheet.appendChild(el);
    });

    /* 宽表在小屏上横向滚动，不把列名切成两半 */
    Array.prototype.forEach.call(sheet.querySelectorAll("table"), function (table) {
      if (table.parentNode.classList.contains("table-wrap")) return;
      var tableWrap = document.createElement("div");
      tableWrap.className = "table-wrap";
      table.parentNode.insertBefore(tableWrap, table);
      tableWrap.appendChild(table);
    });

    /* 3. 左轨：从 meta 与 h2 生成，不复制正文 */
    var parts = meta.textContent.split("·").map(function (s) { return s.trim(); }).filter(Boolean);
    var kicker = parts[0] || TRACKS[track].name;
    var title = parts.slice(1).join(" · ");
    if (track === "index") { kicker = "课程目录"; title = "四条轨道 + 速查"; }
    if (track === "ref" && !title) { title = "速查卡"; }

    var rail = document.createElement("aside");
    rail.className = "lesson-rail";
    rail.setAttribute("aria-label", track === "index" || track === "ref" ? "页面小节" : "本课小节");

    var railInner = document.createElement("div");
    railInner.className = "lesson-rail-inner";
    rail.appendChild(railInner);

    var kickerEl = document.createElement("div");
    kickerEl.className = "rail-kicker";
    kickerEl.textContent = kicker;
    railInner.appendChild(kickerEl);

    if (title) {
      var titleEl = document.createElement("div");
      titleEl.className = "rail-title";
      titleEl.textContent = title;
      railInner.appendChild(titleEl);
    }

    var headings = Array.prototype.slice.call(sheet.querySelectorAll("h2"));
    if (!headings.length) body.classList.add("no-rail");
    var nav = document.createElement("nav");
    nav.className = "rail-nav";
    nav.setAttribute("aria-label", track === "index" || track === "ref" ? "页面小节目录" : "本课小节目录");

    var circled = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫";
    headings.forEach(function (h2, i) {
      if (!h2.id) h2.id = "sec-" + (i + 1);
      var text = h2.textContent.replace(/\s+/g, " ").trim();
      var m = text.match(/^(?:Q\s*(\d+)|(\d+))\s*[.、:：．·]?\s*(.*)$/);
      var no = m ? (m[1] ? "Q" + m[1] : String(Number(m[2])).padStart(2, "0")) : String(i + 1).padStart(2, "0");
      var label = m && m[3] ? m[3] : text;

      /* 速查页的 ① ② ③：数字放进左列，标题不再带圈号 */
      var cm = text.match(/^([①②③④⑤⑥⑦⑧⑨⑩⑪⑫])\s*(.*)$/);
      if (cm) {
        no = String(circled.indexOf(cm[1]) + 1).padStart(2, "0");
        label = cm[2];
      }

      var a = document.createElement("a");
      a.href = "#" + h2.id;
      var span = document.createElement("span");
      span.textContent = no;
      a.appendChild(span);
      a.appendChild(document.createTextNode(label));
      nav.appendChild(a);
    });
    railInner.appendChild(nav);

    var quizCount = sheet.querySelectorAll(".quiz").length;
    var stats = document.createElement("dl");
    stats.className = "rail-stats";

    var secRow = document.createElement("div");
    var secDt = document.createElement("dt");
    secDt.textContent = "小节";
    var secDd = document.createElement("dd");
    secDd.textContent = String(headings.length);
    secRow.appendChild(secDt);
    secRow.appendChild(secDd);
    stats.appendChild(secRow);

    if (quizCount) {
      var quizRow = document.createElement("div");
      var quizDt = document.createElement("dt");
      quizDt.textContent = "小测";
      var quizDd = document.createElement("dd");
      quizDd.textContent = quizCount + " 题";
      quizRow.appendChild(quizDt);
      quizRow.appendChild(quizDd);
      stats.appendChild(quizRow);

      var scoreRow = document.createElement("div");
      var scoreDt = document.createElement("dt");
      scoreDt.textContent = "自检";
      var scoreDd = document.createElement("dd");
      scoreDd.setAttribute("data-quiz-score", "");
      scoreDd.textContent = "0 / " + quizCount;
      scoreRow.appendChild(scoreDt);
      scoreRow.appendChild(scoreDd);
      stats.appendChild(scoreRow);
    }
    railInner.appendChild(stats);

    wrap.insertBefore(rail, head);
    wrap.classList.add("lesson");

    /* 4. 自检计数：quiz.js 先判分，这里在冒泡阶段记一次 */
    var answered = 0;
    var scoreEl = rail.querySelector("[data-quiz-score]");
    sheet.querySelectorAll(".quiz").forEach(function (quiz) {
      quiz.addEventListener("click", function (e) {
        if (!e.target.closest(".quiz-option")) return;
        if (quiz.getAttribute("data-counted") === "1") return;
        var feedback = quiz.querySelector(".feedback");
        if (!feedback || !feedback.classList.contains("show")) return;
        quiz.setAttribute("data-counted", "1");
        answered += 1;
        if (scoreEl) scoreEl.textContent = answered + " / " + quizCount;
      });
    });

    /* 5. 目录联动：点亮当前小节。按滚动位置算，点击锚点后也能立刻对上 */
    var links = Array.prototype.slice.call(nav.children);
    var activeIndex = -1;

    function setActive(index) {
      if (index === activeIndex) return;
      activeIndex = index;
      links.forEach(function (link, i) {
        link.classList.toggle("active", i === index);
      });
    }

    function syncActive() {
      if (!links.length) return;
      var index = 0;
      var line = window.innerHeight * 0.25;
      headings.forEach(function (h2, i) {
        if (h2.getBoundingClientRect().top <= line) index = i;
      });
      /* 滚到底时最后一节的标题到不了这条线，直接点亮它 */
      if (document.documentElement.scrollHeight > window.innerHeight + 8 &&
          window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4) {
        index = links.length - 1;
      }
      setActive(index);
    }

    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        ticking = false;
        syncActive();
      });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    window.addEventListener("load", syncActive);
    nav.addEventListener("click", function (e) {
      var link = e.target.closest("a");
      var i = link ? links.indexOf(link) : -1;
      if (i >= 0) setActive(i);
    });

    /* 6. 最后才开主题，脚本失败时页面仍停在 base.css 单栏 */
    body.classList.add("theme-b");
    syncActive();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
