/* 漫畫閱讀模式切換：卷軸（整話直排）/ 翻頁（單頁放大，左右換頁）。
   頁面需求：#reader 內含依序的 <img>；#mode-scroll / #mode-paged 切換鈕；
   #pager 內含 #prev / #next / #page-indicator。
   翻頁操作：底部按鈕、鍵盤 ←→、點圖片左半（上一頁）右半（下一頁）。
   模式偏好記在 localStorage；未設定時寬螢幕預設翻頁、窄螢幕預設卷軸。 */
(function () {
  "use strict";
  var reader = document.getElementById("reader");
  if (!reader) return;
  var imgs = Array.prototype.slice.call(reader.querySelectorAll("img"));
  var pager = document.getElementById("pager");
  var indicator = document.getElementById("page-indicator");
  var btnScroll = document.getElementById("mode-scroll");
  var btnPaged = document.getElementById("mode-paged");
  var btnPrev = document.getElementById("prev");
  var btnNext = document.getElementById("next");
  var btnScene = document.getElementById("next-scene");
  var sceneEnd = document.getElementById("scene-end");
  // 下一場已上線時在 #reader 加 data-next-url / data-next-label，最後一頁的「下一頁」變「下一場」
  var nextUrl = reader.getAttribute("data-next-url");
  var nextLabel = reader.getAttribute("data-next-label") || "下一場";
  var cur = 0;
  var paged = false;

  function show(i, scroll) {
    cur = Math.max(0, Math.min(imgs.length - 1, i));
    var last = cur === imgs.length - 1;
    imgs.forEach(function (im, k) { im.classList.toggle("current", k === cur); });
    indicator.textContent = (cur + 1) + " ／ " + imgs.length;
    btnPrev.disabled = cur === 0;
    btnNext.disabled = last && !nextUrl;
    btnNext.textContent = last && nextUrl ? nextLabel + " →" : "下一頁 →";
    if (sceneEnd) sceneEnd.classList.toggle("show", last);
    if (imgs[cur + 1]) { (new Image()).src = imgs[cur + 1].src; } // 預載下一頁
    if (scroll) reader.scrollIntoView({ block: "start" });
  }

  function goNext() {
    if (cur === imgs.length - 1) {
      if (nextUrl) window.location.href = nextUrl;
      return;
    }
    show(cur + 1, true);
  }

  function setMode(p) {
    paged = p;
    reader.classList.toggle("paged", p);
    pager.hidden = !p;
    btnPaged.classList.toggle("active", p);
    btnScroll.classList.toggle("active", !p);
    try { localStorage.setItem("comicReaderMode", p ? "paged" : "scroll"); } catch (e) { /* 私密模式沒 storage，略過 */ }
    if (p) show(cur, false);
  }

  btnScroll.addEventListener("click", function () { setMode(false); });
  btnPaged.addEventListener("click", function () { setMode(true); });
  btnPrev.addEventListener("click", function () { show(cur - 1, true); });
  btnNext.addEventListener("click", goNext);

  if (btnScene) {
    if (nextUrl) {
      btnScene.textContent = nextLabel + " »";
      btnScene.addEventListener("click", function () { window.location.href = nextUrl; });
    } else {
      btnScene.disabled = true;
      btnScene.title = "下一場製作中";
    }
  }

  imgs.forEach(function (im) {
    im.addEventListener("click", function (e) {
      if (!paged) return;
      var rect = im.getBoundingClientRect();
      if (e.clientX - rect.left < rect.width / 2) { show(cur - 1, true); } else { goNext(); }
    });
  });

  document.addEventListener("keydown", function (e) {
    if (!paged) return;
    if (e.key === "ArrowLeft") show(cur - 1, true);
    if (e.key === "ArrowRight") goNext();
  });

  var saved = null;
  try { saved = localStorage.getItem("comicReaderMode"); } catch (e) { saved = null; }
  setMode(saved ? saved === "paged" : window.matchMedia("(min-width: 900px)").matches);
})();
