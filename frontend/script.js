const API_URL = "https://court-verdict-7.onrender.com/predict";

/* =========================
   PUNISHMENT ENGINE
========================= */
function getPunishment(ipcList) {
    const map = {
        "IPC 302": "Life Imprisonment / Death Penalty",
        "IPC 379": "Up to 3 years imprisonment + fine",
        "IPC 420": "Up to 7 years imprisonment + fine",
        "IPC 323": "Up to 1 year imprisonment or fine",
        "IPC 506": "Up to 7 years imprisonment",
        "IPC 211": "Up to 2 years imprisonment + fine",
        "IPC 120B": "Criminal conspiracy punishment applicable",
        "IPC 34": "Common intention clause applied"
    };

    if (!ipcList) return "Not defined";

    let list = Array.isArray(ipcList) ? ipcList : ipcList.split(",");

    return list.map(i => {
        let clean = i.trim().toUpperCase();
        return map[clean] || "Not defined";
    }).join(" | ");
}

/* =========================
   HISTORY STORAGE
========================= */
let history = JSON.parse(localStorage.getItem("history")) || [];

/* =========================
   MAIN PREDICT FUNCTION
========================= */
async function predict() {
    try {
        const text = document.getElementById("textInput").value;

        if (!text || text.trim() === "") {
            document.getElementById("result").innerHTML =
                "❌ Enter text first";
            return;
        }

        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        if (!res.ok) throw new Error("Backend error");

        const data = await res.json();

        /* =========================
           SHOW RESULT
        ========================= */
        document.getElementById("result").innerHTML =
            `IPC: ${data.ipc} <br>
             Verdict: ${data.verdict} <br>
             Punishment: ${getPunishment(data.ipc)}`;

        /* =========================
           SAVE HISTORY
        ========================= */
        history.push({
            text: text,
            ipc: data.ipc,
            verdict: data.verdict,
            time: new Date().toLocaleString()
        });

        localStorage.setItem("history", JSON.stringify(history));

        /* =========================
           UPDATE CHART
        ========================= */
        updateChart();

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
            "❌ Backend connection error";
    }
}

/* =========================
   LOAD HISTORY PAGE
========================= */
function loadHistory() {
    let list = document.getElementById("historyList");
    list.innerHTML = "";

    history.forEach(item => {
        let li = document.createElement("li");
        li.innerHTML = `
            <b>${item.verdict}</b><br>
            IPC: ${item.ipc}<br>
            <small>${item.time}</small>
        `;
        list.appendChild(li);
    });
}

/* =========================
   PAGE NAVIGATION
========================= */
function showPage(page) {
    document.querySelectorAll(".page").forEach(p => p.style.display = "none");
    document.getElementById(page).style.display = "block";

    if (page === "history") {
        loadHistory();
    }

    if (page === "analytics") {
        updateChart();
    }
}

/* =========================
   ANALYTICS CHART
========================= */
function updateChart() {
    let ctx = document.getElementById("chart").getContext("2d");

    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: history.map(h => h.verdict),
            datasets: [{
                label: "Cases",
                data: history.map(() => 1)
            }]
        }
    });
}
