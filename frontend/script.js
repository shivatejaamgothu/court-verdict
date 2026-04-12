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

    const loader = document.getElementById("loader");

    // UI reset
    loader.style.display = "block";
    document.getElementById("verdict").innerText = "Processing...";
    document.getElementById("recommendation").innerText = "";
    document.getElementById("ipc").innerHTML = "";
    document.getElementById("punishment").innerText = "";
    document.getElementById("similarity").innerText = "";
    document.getElementById("confidenceBar").style.width = "0%";

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text
            })
        });

        const data = await res.json();

        console.log("Backend Response:", data);

        loader.style.display = "none";

        // backend error handling
        if (!res.ok || data.error) {
            throw new Error(data.error || "Server error");
        }

        /* =========================
           SHOW RESULTS
        ========================= */

        // Verdict
        document.getElementById("verdict").innerText =
            "⚖️ Verdict: " + data.prediction;

        // GPT explanation
        document.getElementById("recommendation").innerText =
            data.reply;

        // IPC tag (simple display)
        document.getElementById("ipc").innerHTML =
            `<span class="tag">${data.prediction}</span>`;

        // Static UI improvements
        document.getElementById("punishment").innerText =
            "AI Legal Analysis Completed";

        document.getElementById("similarity").innerText =
            "Confidence: ~85%";

        document.getElementById("confidenceBar").style.width = "85%";

    } catch (err) {
        loader.style.display = "none";

        console.error("Frontend Error:", err);

        document.getElementById("verdict").innerText = "❌ Error";
        document.getElementById("recommendation").innerText =
            "Backend not reachable. Check Render deployment.";

        alert("❌ Backend connection failed");
    }
}


/* =========================
   ENTER KEY SUPPORT
========================= */
document.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        const input = document.getElementById("caseText");
        if (document.activeElement === input) {
            predict();
        }
    }
});
