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

  try {
    const response = await fetch(url, options);
    const result = await response.json();
    if (response.ok && result.responseCode === "000") {
      return result.responseData;
    }
    throw new Error(result.responseMessage || "API request failed");
  } catch (error) {
    throw error;
  }
}

function drawPieChart(canvas, values, colors) {
  const ctx = canvas.getContext("2d");
  const total = values.reduce((sum, item) => sum + item.value, 0);
  let startAngle = -0.5 * Math.PI;
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = Math.min(centerX, centerY) - 10;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  values.forEach((segment, index) => {
    const sliceAngle = total ? (segment.value / total) * Math.PI * 2 : 0;
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
    ctx.closePath();
    ctx.fillStyle = colors[index];
    ctx.fill();
    startAngle += sliceAngle;
  });
}

function drawBarChart(canvas, value, color) {
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const width = canvas.width - 40;
  const height = canvas.height - 60;
  const barHeight = 20;
  const x = 20;
  const y = 40;
  const barWidth = (value / 100) * width;

  ctx.fillStyle = "rgba(255,255,255,0.08)";
  ctx.fillRect(x, y, width, barHeight);
  ctx.fillStyle = color;
  ctx.fillRect(x, y, barWidth, barHeight);
  ctx.font = "14px Inter, sans-serif";
  ctx.fillStyle = "rgba(255,255,255,0.82)";
  ctx.fillText(`${value}% events flagged`, x, y - 12);
}

async function loadDashboard() {
  showLoader();
  try {
    const data = await callAPI(`${apiBase}/dashboard`, "GET");
    document.getElementById("card-total-scans").textContent = data.totalScans;
    document.getElementById("card-safe").textContent = data.safe;
    document.getElementById("card-suspicious").textContent = data.suspicious;
    document.getElementById("card-dangerous").textContent = data.dangerous;
    document.getElementById("card-events").textContent = data.events;

    const riskChart = document.getElementById("riskChart");
    const eventsChart = document.getElementById("eventsChart");

    riskChart.width = riskChart.clientWidth * 2;
    riskChart.height = 240;
    eventsChart.width = eventsChart.clientWidth * 2;
    eventsChart.height = 240;

    drawPieChart(
      riskChart,
      [
        { value: data.safe, label: "Safe" },
        { value: data.suspicious, label: "Suspicious" },
        { value: data.dangerous, label: "Dangerous" },
      ],
      ["#00ff88", "#ffcc00", "#ff4d4d"]
    );

    const eventPercent = data.totalScans ? Math.round((data.events / data.totalScans) * 100) : 0;
    drawBarChart(eventsChart, eventPercent, "#00ff88");
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    hideLoader();
  }
}

window.addEventListener("load", loadDashboard);
const refreshButton = document.getElementById("refresh-dashboard");
if (refreshButton) {
  refreshButton.addEventListener("click", loadDashboard);
}
