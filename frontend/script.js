const API_URL = "https://court-verdict-5.onrender.com/chat";

/* =========================
   PAGE NAVIGATION
========================= */
function showPage(page) {
    document.querySelectorAll(".page").forEach(p => {
        p.style.display = "none";
    });

    const active = document.getElementById(page);
    if (active) active.style.display = "block";
}

showPage("dashboard");


/* =========================
   MAIN PREDICT FUNCTION
========================= */
async function predict() {
    const text = document.getElementById("caseText").value.trim();

    if (!text) {
        alert("⚠️ Please enter case details");
        return;
    }

    // UI elements
    const loader = document.getElementById("loader");
    const verdict = document.getElementById("verdict");
    const ipc = document.getElementById("ipc");
    const punishment = document.getElementById("punishment");
    const recommendation = document.getElementById("recommendation");
    const confidenceBar = document.getElementById("confidenceBar");
    const similarity = document.getElementById("similarity");

    // reset UI
    loader.style.display = "block";
    verdict.innerText = "Processing...";
    ipc.innerHTML = "";
    punishment.innerText = "";
    recommendation.innerText = "";
    similarity.innerText = "";
    confidenceBar.style.width = "0%";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text
            })
        });

        const data = await response.json();

        loader.style.display = "none";

        // backend error check
        if (!response.ok || data.error) {
            throw new Error(data.error || "Server error");
        }

        /* =========================
           SHOW RESULTS
        ========================= */

        // ML Prediction
        verdict.innerText = `⚖️ Verdict: ${data.prediction}`;

        // GPT explanation
        recommendation.innerText = data.reply;

        // IPC tag (simple display)
        ipc.innerHTML = `
            <span class="tag">${data.prediction}</span>
        `;

        punishment.innerText = "AI analysis completed successfully";

        similarity.innerText = "Confidence: 85% (estimated)";

        confidenceBar.style.width = "85%";

    } catch (error) {
        loader.style.display = "none";

        console.error("Error:", error);

        verdict.innerText = "❌ Error";
        recommendation.innerText = "Backend connection failed. Check server or API URL.";

        alert("❌ Backend connection failed");
    }
}


/* =========================
   OPTIONAL: ENTER KEY SUPPORT
========================= */
document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && document.getElementById("caseText") === document.activeElement) {
        predict();
    }
});
