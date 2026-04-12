const API_URL = "https://court-verdict-7.onrender.com/chat";
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

    console.log("Sending to backend:", text);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        console.log("Raw response:", response);

        const data = await response.json();
        console.log("Backend data:", data);

        if (!response.ok) {
            throw new Error("HTTP Error: " + response.status);
        }

        document.getElementById("verdict").innerText =
            "Verdict: " + data.verdict;

        document.getElementById("punishment").innerText =
            "Punishment: " + data.punishment;

        const ipcDiv = document.getElementById("ipc");
        ipcDiv.innerHTML = "";

        (data.ipc_sections || []).forEach(ipc => {
            let span = document.createElement("span");
            span.innerText = ipc;
            span.className = "ipc-tag";
            ipcDiv.appendChild(span);
        });

        document.getElementById("confidenceBar").style.width =
            data.confidence + "%";

    } catch (err) {
        console.log("ERROR:", err);
        alert("Backend connection failed: " + err.message);
    }
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
