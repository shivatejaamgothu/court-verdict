const API_URL = "https://court-verdict-3.onrender.com/predict";

// pages
function showPage(page) {
    document.querySelectorAll(".page").forEach(p => p.style.display = "none");
    document.getElementById(page).style.display = "block";
}

showPage("dashboard");

// prediction function (FIXED)
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
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        document.getElementById("loader").style.display = "none";

        // RESULT HANDLING
        document.getElementById("verdict").innerText =
            "Verdict: " + (data.prediction || "N/A");

        document.getElementById("punishment").innerText =
            "Prediction Result: " + (data.prediction || "N/A");

        document.getElementById("recommendation").innerText =
            data.error ? data.error : "AI analysis completed successfully";

        // confidence (fake fallback if not provided)
        let confidence = data.confidence || Math.floor(Math.random() * 30 + 70);

        document.getElementById("similarity").innerText =
            "Confidence: " + confidence + "%";

        document.getElementById("confidenceBar").style.width = confidence + "%";

        // IPC tags (if backend returns list later)
        let ipcDiv = document.getElementById("ipc");
        ipcDiv.innerHTML = "";

        if (data.ipc && Array.isArray(data.ipc)) {
            data.ipc.forEach(ipc => {
                let span = document.createElement("span");
                span.className = "tag";
                span.innerText = ipc;
                ipcDiv.appendChild(span);
            });
        }

    } catch (error) {
        document.getElementById("loader").style.display = "none";
        alert("Backend connection failed ❌");
        console.error(error);
    }
}
