const API_URL = "https://court-verdict-7.onrender.com/predict";
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

    let list = Array.isArray(ipcList)
        ? ipcList
        : ipcList.split(",");

    return list.map(i => {
        let clean = i.trim().toUpperCase();
        return map[clean] || "Not defined";
    }).join(" | ");
}

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
    `  IPC: ${data.ipc} <br>
      Verdict: ${data.verdict} <br>
      Punishment: ${getPunishment(data.ipc)}`;


    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
            "❌ Backend connection error";
    }
}
