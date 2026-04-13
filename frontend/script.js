const API_URL = "https://court-verdict-7.onrender.com/predict";

async function predict() {
    try {
        const text = document.getElementById("textInput").value;

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        document.getElementById("result").innerHTML =
            `IPC: ${data.ipc} <br>
             Verdict: ${data.verdict} <br>
             Confidence: ${data.confidence}%`;

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
            "❌ Backend connection error";
    }
}
