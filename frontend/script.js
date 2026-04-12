const API_URL = "https://court-verdict-5.onrender.com/chat"; // keep your correct Render URL

function showPage(page) {
    document.querySelectorAll(".page").forEach(p => p.style.display = "none");
    document.getElementById(page).style.display = "block";
}

showPage("dashboard");

// ==========================
// MAIN PREDICT FUNCTION
// ==========================
async function predict() {
    const text = document.getElementById("caseText").value;

    if (!text) {
        alert("Please enter case details");
        return;
    }

    document.getElementById("loader").style.display = "block";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();

        document.getElementById("loader").style.display = "none";

        if (data.error) {
            alert(data.error);
            return;
        }

        // ==========================
        // VERDICT
        // ==========================
        document.getElementById("verdict").innerText =
            "Verdict: " + (data.verdict || "N/A");

        // ==========================
        // IPC SECTIONS (MULTIPLE)
        // ==========================
        const ipcDiv = document.getElementById("ipc");
        ipcDiv.innerHTML = "";

        if (data.ipc_sections && data.ipc_sections.length > 0) {
            data.ipc_sections.forEach(ipc => {
                let span = document.createElement("span");
                span.className = "ipc-tag";
                span.innerText = ipc;
                ipcDiv.appendChild(span);
            });
        } else {
            ipcDiv.innerText = "No IPC detected";
        }

        // ==========================
        // PUNISHMENT
        // ==========================
        document.getElementById("punishment").innerText =
            "Punishment: " + (data.punishment || "Not available");

        // ==========================
        // CONFIDENCE BAR
        // ==========================
        let confidence = data.confidence || 0;
        document.getElementById("confidenceBar").style.width = confidence + "%";

        // ==========================
        // SIMILARITY / EXTRA INFO
        // ==========================
        document.getElementById("similarity").innerText =
            "Confidence: " + confidence + "%";

    } catch (error) {
        document.getElementById("loader").style.display = "none";
        console.log(error);
        alert("❌ Backend connection failed");
    }
}