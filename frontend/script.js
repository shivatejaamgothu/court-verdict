const API_URL = "https://court-verdict-5.onrender.com/chat";
function showPage(page) {
    document.querySelectorAll(".page").forEach(p => p.style.display = "none");
    document.getElementById(page).style.display = "block";
}

showPage("dashboard");

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
            body: JSON.stringify({ message: text })   // IMPORTANT FIX
        });

        const data = await response.json();

        document.getElementById("loader").style.display = "none";

        if (data.error) {
            alert(data.error);
            return;
        }

        // ChatGPT-style response handling
        document.getElementById("verdict").innerText =
            "AI Response";

        document.getElementById("recommendation").innerText =
            data.reply || "No response";

        document.getElementById("punishment").innerText =
            "";

        document.getElementById("similarity").innerText =
            "";

        document.getElementById("ipc").innerHTML = "";

        document.getElementById("confidenceBar").style.width = "0%";

    } catch (error) {
        document.getElementById("loader").style.display = "none";
        console.log(error);
        alert("❌ Backend connection failed");
    }
}
