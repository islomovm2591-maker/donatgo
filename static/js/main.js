// DonatGo — kichik yordamchi skriptlar
document.addEventListener("DOMContentLoaded", () => {
  // Nusxalash tugmalari
  document.querySelectorAll(".copy[data-copy]").forEach((btn) => {
    const label = btn.textContent;
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy.replace(/^[^:]*:\s*/, "").replace(/\s*\(.*\)\s*$/, "") || btn.dataset.copy;
      const value = btn.closest(".cards") ? text : btn.dataset.copy;
      try { await navigator.clipboard.writeText(value); }
      catch { const ta = document.createElement("textarea"); ta.value = value; document.body.append(ta); ta.select(); document.execCommand("copy"); ta.remove(); }
      btn.textContent = btn.dataset.done; btn.classList.add("done");
      setTimeout(() => { btn.textContent = label; btn.classList.remove("done"); }, 1800);
    });
  });

  // Paket tanlanganda summa
  const payText = document.querySelector(".pay-text");
  const total = document.querySelector(".total");
  const update = () => {
    const sel = document.querySelector(".packs input:checked");
    if (!sel || !payText) return;
    total.textContent = sel.dataset.price;
    payText.innerHTML = "";
    const [a, b] = payText.dataset.tpl.split("%AMOUNT%");
    const strong = document.createElement("b"); strong.textContent = sel.dataset.price;
    payText.append(a, strong, b);
  };
  document.querySelectorAll(".packs input").forEach((i) => i.addEventListener("change", update));
  update();

  // Chek rasmi ko'rinishi
  const file = document.querySelector('.upload input[type="file"]');
  if (file) file.addEventListener("change", () => {
    const f = file.files[0];
    const img = document.querySelector(".upload .preview");
    document.querySelector(".upload-name").textContent = f ? f.name : "";
    if (f && f.type.startsWith("image/")) { img.src = URL.createObjectURL(f); img.hidden = false; } else { img.hidden = true; }
  });

  // Tugmani ikki marta bosishdan himoya
  const form = document.querySelector(".order-form");
  if (form) form.addEventListener("submit", () => { const b = form.querySelector('button[type="submit"]'); b.disabled = true; b.style.opacity = .6; });

  // Buyurtma holatini avtomatik yangilash
  const view = document.querySelector(".order-view[data-status='pending']");
  if (view) setInterval(async () => {
    try {
      const r = await fetch(`/api/order/${encodeURIComponent(view.dataset.code)}`);
      const d = await r.json();
      if (d.status && d.status !== "pending") location.reload();
    } catch {}
  }, 15000);

  // Admin: yangi buyurtma kelsa sahifani yangilash
  const stats = document.querySelector("[data-poll-pending]");
  if (stats) setInterval(async () => {
    try {
      const r = await fetch("/admin/api/pending");
      const d = await r.json();
      if (d.pending !== Number(stats.dataset.pollPending)) location.reload();
    } catch {}
  }, 30000);
});
