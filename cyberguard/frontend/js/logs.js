// Point API calls to Flask backend. Change if your backend runs elsewhere.
const apiBase = "http://localhost:5000/api";
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

function renderLogsTable(events) {
  const tbody = document.getElementById("logs-table-body");
  tbody.innerHTML = "";

  if (events.length === 0) {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="4">No security events found</td>`;
    tbody.appendChild(row);
    return;
  }

  events.forEach((event) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${event.eventId}</td>
      <td>${event.eventType}</td>
      <td>${event.description}</td>
      <td>${event.timestamp}</td>
    `;
    tbody.appendChild(row);
  });
}

async function loadLogs() {
  showLoader();
  try {
    const events = await callAPI(`${apiBase}/logs`, "GET");
    window.allLogs = events;
    renderLogsTable(events);
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    hideLoader();
  }
}

function filterLogs(searchTerm) {
  const filtered = (window.allLogs || []).filter((event) => {
    const lower = searchTerm.toLowerCase();
    return (
      event.eventId.toLowerCase().includes(lower) ||
      event.eventType.toLowerCase().includes(lower) ||
      event.description.toLowerCase().includes(lower) ||
      event.timestamp.toLowerCase().includes(lower)
    );
  });
  renderLogsTable(filtered);
}

window.addEventListener("load", loadLogs);
const searchInput = document.getElementById("search-logs");
if (searchInput) {
  searchInput.addEventListener("input", (event) => {
    filterLogs(event.target.value.trim());
  });
}
