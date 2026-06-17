// Ensure API requests target the Flask backend. When developing with a
// static server (eg. Live Server on :5500) requests to `/api` will hit
// the static server and return 405 for POST. Point to the Flask server
// instead (default: http://localhost:5000).
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

function renderResult(scanData) {
  const container = document.getElementById("scan-result");
  const details = scanData.reasons.map((reason) => `<li>${reason}</li>`).join("");
  const statusColor = scanData.status === "DANGEROUS" ? "#ff4d4d" : scanData.status === "SUSPICIOUS" ? "#ffcc00" : "#00ff88";

  container.innerHTML = `
    <h3>Status: <span style="color:${statusColor}">${scanData.status}</span></h3>
    <p><strong>Risk score:</strong> ${scanData.riskScore}</p>
    <p><strong>URL:</strong> ${scanData.url}</p>
    <h4>Reasons:</h4>
    <ul>${details || "<li>No suspicious indicators detected</li>"}</ul>
  `;
}

async function scanUrl(event) {
  // Prevent default form submit or other default actions if an event is provided
  if (event && typeof event.preventDefault === "function") {
    event.preventDefault();
  }

  const input = document.getElementById("scan-url");
  const url = input.value.trim();
  if (!url) {
    showToast("Please enter a URL to scan.", "error");
    return;
  }

  showLoader();
  try {
    const response = await callAPI(`${apiBase}/phishing/scan`, "POST", { url });
    renderResult(response);
    try {
      // Persist last scan so a brief page reload doesn't lose it
      localStorage.setItem("cyberguard_last_scan", JSON.stringify(response));
    } catch (e) {
      // ignore storage errors
    }
    showToast("URL scanned successfully.");
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    hideLoader();
  }
}

const scanButton = document.getElementById("scan-button");
if (scanButton) {
  scanButton.addEventListener("click", scanUrl);
}

// Only trigger scan with Enter when the URL input is focused to avoid
// global Enter handling causing unintended page reloads or actions.
window.addEventListener("keydown", (event) => {
  if (
    event.key === "Enter" &&
    document.activeElement &&
    document.activeElement.id === "scan-url"
  ) {
    event.preventDefault();
    scanUrl();
  }
});

// On load, re-render last scan result if available so short reloads don't
// cause the result to vanish.
window.addEventListener("load", () => {
  try {
    const raw = localStorage.getItem("cyberguard_last_scan");
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && parsed.url) {
        renderResult(parsed);
      }
    }
  } catch (e) {
    // ignore parse errors
  }
});
