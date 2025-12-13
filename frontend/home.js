// -------------------- SECTION NAVIGATION --------------------
function showSection(sectionId) {
  document.querySelectorAll("main section").forEach(sec => sec.classList.remove("active"));
  document.getElementById(sectionId).classList.add("active");
}

// -------------------- API BASES --------------------
const DATA_API = "http://127.0.0.1:8000/data";
const PREPROCESS_API = "http://127.0.0.1:8000/preprocess";
const BIAS_API = "http://127.0.0.1:8000/bias";
const PRIVACY_API = "http://127.0.0.1:8000/privacy";
const SIM_API = "http://127.0.0.1:8000/sim";
const DASH_API = "http://127.0.0.1:8000/dashboard";

// -------------------- DATA INGESTION --------------------
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput?.files[0];
  if (!file) return alert("Select a CSV file first!");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${DATA_API}/upload`, { method: "POST", body: formData });
    const data = await res.json();
    alert(data.message);
    loadDatasets();
  } catch (err) {
    alert("Upload failed: " + err);
  }
}

async function loadDatasets() {
  const res = await fetch(`${DATA_API}/files`);
  const data = await res.json();

  const tableBody = document.querySelector("#datasetTable tbody");
  if (!tableBody) return;

  tableBody.innerHTML = "";
  data.files.forEach(filename => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${filename}</td>
      <td>—</td>
      <td>—</td>
      <td><button onclick="previewDataset('${filename}')">Preview</button></td>
    `;
    tableBody.appendChild(tr);
  });
}

async function previewDataset(filename) {
  const res = await fetch(`${DATA_API}/preview/${filename}`);
  const data = await res.json();

  const previewDiv = document.getElementById("previewDiv");
  previewDiv.innerHTML = "";

  const table = document.createElement("table");
  table.classList.add("preview-table");

  const headers = Object.keys(data.preview[0] || {});
  const thead = document.createElement("thead");
  thead.innerHTML = "<tr>" + headers.map(h => `<th>${h}</th>`).join("") + "</tr>";
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  data.preview.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = headers.map(h => `<td>${row[h]}</td>`).join("");
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  previewDiv.appendChild(table);
}

loadDatasets();

// -------------------- PREPROCESSING --------------------
async function loadPreprocessFiles() {
  const res = await fetch(`${DATA_API}/files`);
  const data = await res.json();
  const select = document.getElementById("preprocessFileSelect");
  select.innerHTML = data.files.map(f => `<option value="${f}">${f}</option>`).join("");
}

async function previewPreprocess() {
  const filename = document.getElementById("preprocessFileSelect").value;
  const res = await fetch(`${PREPROCESS_API}/preview/${filename}`);
  const data = await res.json();

  let html = `<h4>Preview of ${data.filename}</h4>`;
  html += `<p>Rows: ${data.rows}, Columns: ${data.columns.length}</p>`;
  const headers = data.columns;
  html += "<table border='1'><tr>" + headers.map(h => `<th>${h}</th>`).join("") + "</tr>";
  data.sample_data.forEach(row => {
    html += "<tr>" + headers.map(h => `<td>${row[h]}</td>`).join("") + "</tr>";
  });
  html += "</table>";
  document.getElementById("preprocessPreview").innerHTML = html;
}

async function summaryPreprocess() {
  const filename = document.getElementById("preprocessFileSelect").value;
  const res = await fetch(`${PREPROCESS_API}/summary/${filename}`);
  const data = await res.json();

  let html = `<h4>Summary of ${filename}</h4>`;
  html += `<p>Rows: ${data.rows}, Columns: ${data.columns}</p>`;
  html += "<h5>Missing Values:</h5><ul>";
  for (const col in data.missing_values) html += `<li>${col}: ${data.missing_values[col]}</li>`;
  html += "</ul><h5>Column Types:</h5><ul>";
  for (const col in data.column_types) html += `<li>${col}: ${data.column_types[col]}</li>`;
  html += "</ul>";

  document.getElementById("preprocessSummary").innerHTML = html;
}

async function cleanPreprocess() {
  const filename = document.getElementById("preprocessFileSelect").value;
  const res = await fetch(`${PREPROCESS_API}/clean/${filename}`, { method: "POST" });
  const data = await res.json();

  document.getElementById("preprocessResult").innerHTML = `
    <p>${data.message}</p>
    <p>Saved as: ${data.saved_as}</p>
    <p>Rows before: ${data.rows_before}, Rows after: ${data.rows_after}</p>
  `;
}

async function convertPreprocess() {
  const filename = document.getElementById("preprocessFileSelect").value;
  const res = await fetch(`${PREPROCESS_API}/convert/csv/${filename}`, { method: "POST" });
  const data = await res.json();
  alert(`${data.message}. Saved as: ${data.saved_as}`);
}

loadPreprocessFiles();

// -------------------- BIAS DETECTION --------------------
let imbalanceChart, missingChart, numericChart;

async function loadBiasFiles() {
  const res = await fetch(`${DATA_API}/files`);
  const data = await res.json();
  const select = document.getElementById("biasFileSelect");
  select.innerHTML = data.files.map(f => `<option value="${f}">${f}</option>`).join("");
}

async function loadBiasOverview() {
  const filename = document.getElementById("biasFileSelect").value;
  const res = await fetch(`${BIAS_API}/overview/${filename}`);
  const data = await res.json();
  document.getElementById("biasOverview").innerHTML = `
    <p>Bias Score: ${data.bias_score}</p>
    <p>Missing Value Rate: ${data.missing_value_rate}</p>
    <p>Average Skewness: ${data.avg_skewness}</p>
  `;
}

async function loadClassImbalance() {
  const filename = document.getElementById("biasFileSelect").value;
  const target = document.getElementById("targetColumn").value;
  const res = await fetch(`${BIAS_API}/imbalance/${filename}?target=${target}`);
  const data = await res.json();

  const ctx = document.getElementById("imbalanceChart").getContext("2d");
  if (imbalanceChart) imbalanceChart.destroy();
  imbalanceChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: Object.keys(data.distribution_percent),
      datasets: [{ data: Object.values(data.distribution_percent), backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF'] }]
    },
    options: { responsive: true }
  });
}

async function loadMissingBias() {
  const filename = document.getElementById("biasFileSelect").value;
  const res = await fetch(`${BIAS_API}/missing/${filename}`);
  const data = await res.json();

  let html = "<h4>Columns with Missing Values</h4><ul>";
  data.columns_with_missing.forEach(col => {
    html += `<li>${col}: ${data.missing_by_column[col]}</li>`;
  });
  html += "</ul>";
  document.getElementById("missingBias").innerHTML = html;

  const ctx = document.getElementById("missingChart").getContext("2d");
  if (missingChart) missingChart.destroy();
  missingChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: data.columns_with_missing,
      datasets: [{ data: data.columns_with_missing.map(col => data.missing_by_column[col]), backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'] }]
    },
    options: { responsive: true }
  });
}

async function loadNumericBias() {
  const filename = document.getElementById("biasFileSelect").value;
  const res = await fetch(`${BIAS_API}/numeric/${filename}`);
  const data = await res.json();

  let html = "<h4>Numeric Columns Bias</h4><ul>";
  data.numeric_columns.forEach(col => {
    html += `<li>${col} - Skewness: ${data.skewness[col]}, Outliers: ${data.outliers_per_column[col]}</li>`;
  });
  html += "</ul>";
  document.getElementById("numericBias").innerHTML = html;

  const ctx = document.getElementById("numericChart").getContext("2d");
  if (numericChart) numericChart.destroy();
  numericChart = new Chart(ctx, {
    type: 'bar',
    data: { labels: data.numeric_columns, datasets: [{ label: 'Skewness', data: data.numeric_columns.map(col => data.skewness[col]), backgroundColor: '#36A2EB' }] },
    options: { responsive: true, scales: { y: { beginAtZero: true } } }
  });
}

loadBiasFiles();

// -------------------- PRIVACY AUDIT --------------------
let privacyChart = null;
async function runPrivacyAudit() {
  const fileInput = document.getElementById("privacyFileInput");
  const file = fileInput?.files[0];
  if (!file) return alert("Select a CSV file first!");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${PRIVACY_API}/audit`, { method: "POST", body: formData });
  const data = await res.json();

  const totalCells = data.total_cells || 100;
  const exposed = data.total_hits || 0;
  const notExposed = totalCells - exposed;

  const ctx = document.getElementById("privacyChart").getContext("2d");
  if (privacyChart) privacyChart.destroy();
  privacyChart = new Chart(ctx, {
    type: 'pie',
    data: { labels: ['Exposed', 'Safe'], datasets: [{ data: [exposed, notExposed], backgroundColor: ['#FF6384','#36A2EB'] }] },
    options: { responsive: true }
  });

  // PII Details
  let detailsHtml = "<h4>Detected PII</h4>";
  for (const col in data.pii_detected) detailsHtml += `<p><strong>${col}</strong>: ${JSON.stringify(data.pii_detected[col])}</p>`;
  document.getElementById("privacyDetails").innerHTML = detailsHtml;

  // Recommendations
  let recHtml = "<h4>Recommendations</h4><ul>";
  data.recommendations.forEach(r => recHtml += `<li>${r}</li>`);
  recHtml += "</ul>";
  document.getElementById("privacyRecommendations").innerHTML = recHtml;
}

// -------------------- SIMULATION --------------------
async function runSimulation() {
  const payload = {
    vehicle_speed: parseFloat(document.getElementById("vehicleSpeed").value),
    vru_distance: parseFloat(document.getElementById("vruDistance").value),
    vru_type: document.getElementById("vruType").value,
    weather: document.getElementById("weather").value,
    lighting: document.getElementById("lighting").value
  };

  const res = await fetch(`${SIM_API}/run`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
  const data = await res.json();

  let html = `<h4>Simulation Results</h4>
    <p>Reaction Distance: ${data.reaction_distance} m</p>
    <p>Braking Distance: ${data.braking_distance} m</p>
    <p>Total Stopping Distance: ${data.total_stopping_distance} m</p>
    <p>Risk Score: ${data.risk_score}</p>
    <p>Risk Level: <strong>${data.risk_level}</strong></p>
    <p>Collision Likely: ${data.collision_likely ? "Yes" : "No"}</p>`;
  document.getElementById("simulationResult").innerHTML = html;
}

// -------------------- DASHBOARD --------------------
let vehicleChart, collisionChart, environmentChart;

async function loadDashboardFiles() {
  const res = await fetch(`${DATA_API}/files`);
  const data = await res.json();
  const select = document.getElementById("dashboardFileSelect");
  select.innerHTML = data.files.map(f => `<option value="${f}">${f}</option>`).join("");
}

async function loadDashboardSummary() {
  const filename = document.getElementById("dashboardFileSelect").value;

  // Summary
  const summaryRes = await fetch(`${DASH_API}/summary/${filename}`);
  const summary = await summaryRes.json();
  document.getElementById("dashboardSummary").innerHTML = `
    <p>Total Records: ${summary.total_records}</p>
    <p>Columns: ${summary.columns.join(", ")}</p>
    <p>Missing Values: ${JSON.stringify(summary.missing_values)}</p>
    <p>Column Types: ${JSON.stringify(summary.dtypes)}</p>
  `;

  // Vehicle Distribution
  const vehicleRes = await fetch(`${DASH_API}/vehicle-distribution/${filename}`);
  const vehicleData = await vehicleRes.json();
  const ctxVehicle = document.getElementById("vehicleChart").getContext("2d");
  if (vehicleChart) vehicleChart.destroy();
  vehicleChart = new Chart(ctxVehicle, {
    type: 'pie',
    data: { labels: Object.keys(vehicleData.vehicle_distribution), datasets: [{ data: Object.values(vehicleData.vehicle_distribution), backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF'] }] },
    options: { responsive: true }
  });

  // Collision Risk
  const collisionRes = await fetch(`${DASH_API}/collision-risk/${filename}`);
  const collisionData = await collisionRes.json();
  const ctxCollision = document.getElementById("collisionChart").getContext("2d");
  if (collisionChart) collisionChart.destroy();
  collisionChart = new Chart(ctxCollision, {
    type: 'pie',
    data: { labels: Object.keys(collisionData.collision_risk_distribution), datasets: [{ data: Object.values(collisionData.collision_risk_distribution), backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF'] }] },
    options: { responsive: true }
  });

  // Environment
  const envRes = await fetch(`${DASH_API}/environment/${filename}`);
  const envData = await envRes.json();
  const ctxEnv = document.getElementById("environmentChart").getContext("2d");
  if (environmentChart) environmentChart.destroy();
  const labelsEnv = envData.weather ? Object.keys(envData.weather) : Object.keys(envData.light_condition);
  const valuesEnv = envData.weather ? Object.values(envData.weather) : Object.values(envData.light_condition);
  environmentChart = new Chart(ctxEnv, {
    type: 'pie',
    data: { labels: labelsEnv, datasets: [{ data: valuesEnv, backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF'] }] },
    options: { responsive: true }
  });
  // Speed & VRU Stats
  const speedRes = await fetch(`${DASH_API}/speed-stats/${filename}`);
  const speed = await speedRes.json();
  document.getElementById("speedStats").innerHTML = `<p>Min: ${speed.min_speed}, Max: ${speed.max_speed}, Avg: ${speed.avg_speed}, Median: ${speed.median_speed}, Std: ${speed.std_speed}</p>`;

  const vruRes = await fetch(`${DASH_API}/vru-distance/${filename}`);
  const vru = await vruRes.json();
  document.getElementById("vruStats").innerHTML = `<p>Avg: ${vru.average_distance}, Min: ${vru.min_distance}, Max: ${vru.max_distance}</p>`;
}
loadDashboardFiles();
