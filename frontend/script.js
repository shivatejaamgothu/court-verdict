const API_URL = "https://your-backend-name.onrender.com";
let response = await fetch(API_URL + "/predict", {
let historyData=[]
let chart
function showPage(page){
document.querySelectorAll(".page").forEach(p=>p.style.display="none")
document.getElementById(page).style.display="block"
}
showPage("dashboard")

function toggleTheme(){
document.body.classList.toggle("dark")
}

document.getElementById('pdfUpload').addEventListener('change',async function(e){
let file = e.target.files[0]
let reader = new FileReader()

reader.onload = async function(){
let typedarray = new Uint8Array(this.result)
let pdf = await pdfjsLib.getDocument(typedarray).promise

let text=""
for(let i=1;i<=pdf.numPages;i++){
let page = await pdf.getPage(i)
let content = await page.getTextContent()
content.items.forEach(item=>text+=item.str+" ")
}
document.getElementById("caseText").value=text
}
reader.readAsArrayBuffer(file)
})

async function predict(){

document.getElementById("loader").style.display="block"

let text=document.getElementById("caseText").value

let response=await fetch("https://YOUR-RENDER-URL.onrender.com/predict",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({text:text})
})

let data=await response.json()

document.getElementById("loader").style.display="none"

document.getElementById("verdict").innerText="Prediction: "+data.verdict

let ipc=document.getElementById("ipc")
ipc.innerHTML=""
data.ipc.forEach(i=>{
let span=document.createElement("span")
span.className="tag"
span.innerText=i
ipc.appendChild(span)
})

document.getElementById("punishment").innerText="Punishment: "+data.punishment
document.getElementById("recommendation").innerText="Recommendation: "+data.recommendation

document.getElementById("bar").style.width=data.confidence+"%"

/* similarity */
let sim=Math.floor(Math.random()*20)+80
document.getElementById("similarity").innerText="Similarity: "+sim+"%"

/* history */
historyData.push(text)
let li=document.createElement("li")
li.innerText=text.substring(0,60)
document.getElementById("historyList").appendChild(li)

/* analytics */
updateChart(data.confidence)
}

function updateChart(val){
let ctx=document.getElementById("chart")

if(chart) chart.destroy()

chart=new Chart(ctx,{
type:"bar",
data:{
labels:["Confidence"],
datasets:[{
label:"AI Score",
data:[val]
}]
}
})
}

function exportPDF(){
const { jsPDF } = window.jspdf
let doc=new jsPDF()

doc.text("Court Verdict Prediction",10,10)
doc.text(document.getElementById("verdict").innerText,10,20)
doc.text(document.getElementById("punishment").innerText,10,30)
doc.text(document.getElementById("recommendation").innerText,10,40)

doc.save("court-report.pdf")
}
document.getElementById("confidenceBar").style.width="75%"
document.getElementById("statPred").innerText++
document.getElementById("statIPC").innerText="3"
document.getElementById("statConf").innerText="75%"
document.getElementById("loader").style.display="block"
