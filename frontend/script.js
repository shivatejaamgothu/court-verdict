const API_URL = "https://court-verdict-7.onrender.com/chat";

console.log("SCRIPT LOADED SUCCESSFULLY");

// ==========================
// PAGE NAVIGATION
// ==========================
function showPage(page) {
    document.querySelectorAll(".page").forEach(p => {
        p.style.display = "none";
    });

    const activePage = document.getElementById(page);
    if (activePage) {
        activePage.style.display = "block";
    } else {
        console.error("Page not found:", page);
    }
}

// Default page
window.onload = () => {
    showPage("dashboard");
};

// ==========================
// MAIN PREDICT FUNCTION
// ==========================
async function predict() {
    const text = document.getElementById("caseText").value;

    if (!text || text.trim() === "") {
        alert("Please enter case details");
        return;
    }

    console.log("Sending request:", text);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        console.log("Response status:", response.status);

        const data = await response.json();
        console.log("Response data:", data);

        if (!response.ok) {
            throw new Error(data.error || "Backend error");
        }

        // ==========================
        // VERDICT
        // ==========================
        document.getElementById("verdict").innerText =
            "Verdict: " + (data.verdict || "N/A");

        // ==========================
        // IPC SECTIONS
        // ==========================
        const ipcDiv = document.getElementById("ipc");
        ipcDiv.innerHTML = "";

        if (data.ipc_sections && data.ipc_sections.length > 0) {
            data.ipc_sections.forEach(ipc => {
                const span = document.createElement("span");
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
        const confidence = data.confidence || 0;
        const bar = document.getElementById("confidenceBar");

        if (bar) {
            bar.style.width = confidence + "%";
        }

    } catch (error) {
        console.error("Frontend Error:", error);
        alert("Backend connection failed: " + error.message);
    }
}
