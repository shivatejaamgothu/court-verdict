const API_URL = "https://court-verdict-7.onrender.com/predict";

async function predict() {
    try {
        const text = document.getElementById("textInput").value;

        if (!text) {
            document.getElementById("result").innerHTML = "❌ Enter text first";
            return;
        }

        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        if (!res.ok) {
            throw new Error("Backend error");
        }

        const data = await res.json();

        document.getElementById("result").innerHTML =
            `IPC: ${data.ipc} <br> Verdict: ${data.verdict}`;

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
            "❌ Backend connection error";
    }
}
