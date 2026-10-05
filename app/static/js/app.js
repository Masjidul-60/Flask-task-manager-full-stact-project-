const list = document.getElementById("task-list");
const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const empty = document.getElementById("empty");

async function api(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return res.status === 204 ? null : res.json();
}

function render(tasks) {
  list.innerHTML = "";
  empty.hidden = tasks.length > 0;
  for (const t of tasks) {
    const li = document.createElement("li");
    if (t.done) li.className = "done";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = t.done;
    cb.onchange = async () => {
      await api(`/api/tasks/${t.id}`, { method: "PATCH", body: JSON.stringify({ done: cb.checked }) });
      load();
    };

    const span = document.createElement("span");
    span.textContent = t.title;

    const del = document.createElement("button");
    del.className = "del";
    del.textContent = "✕";
    del.onclick = async () => {
      await api(`/api/tasks/${t.id}`, { method: "DELETE" });
      load();
    };

    li.append(cb, span, del);
    list.append(li);
  }
}

async function load() {
  render(await api("/api/tasks"));
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  await api("/api/tasks", { method: "POST", body: JSON.stringify({ title }) });
  input.value = "";
  load();
});

load();
