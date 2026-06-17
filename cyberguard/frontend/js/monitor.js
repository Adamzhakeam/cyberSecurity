// Point API calls to Flask backend. Change if your backend runs elsewhere.
// Uses `window.API_BASE` when available so deployments can override the
// backend URL (set this via an inline script or replace at build time).
const apiBase = (window && window.API_BASE) ? window.API_BASE : "/api";
const toastElement = document.getElementById("toast");
const loaderElement = document.getElementById("page-loader");

function showLoader() {
  loaderElement.classList.remove("hidden");
}

function hideLoader() {
  loaderElement.classList.add("hidden");
}

function showToast(message, type = "success") {
  toastElement.textContent = message;
  toastElement.className = `toast show ${type === "error" ? "error" : ""}`;
  window.setTimeout(() => {
    toastElement.classList.remove("show");
  }, 3200);
}

async function callAPI(url, method = "GET", payload = null) {
  const options = { method, headers: { "Content-Type": "application/json" } };
  if (payload) options.body = JSON.stringify(payload);

  const response = await fetch(url, options);
  const body = await response.json();
  if (response.ok && body.responseCode === "000") {
    return body.responseData;
  }
  throw new Error(body.responseMessage || "API error");
}

function renderProcessTable(processes) {
  const tbody = document.getElementById("process-table-body");
  tbody.innerHTML = "";

  processes.forEach((process) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${process.pid}</td>
      <td>${process.name}</td>
      <td>${process.cpu}%</td>
      <td>${process.memory}%</td>
      <td>${process.path}</td>
    `;
    tbody.appendChild(row);
  });
}

async function loadProcesses() {
  showLoader();
  try {
    const result = await callAPI(`${apiBase}/processes`, "GET");
    renderProcessTable(result);
    showToast("Process list updated.");
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    hideLoader();
  }
}

const refreshButton = document.getElementById("refresh-processes");
if (refreshButton) {
  refreshButton.addEventListener("click", loadProcesses);
}

window.addEventListener("load", loadProcesses);
