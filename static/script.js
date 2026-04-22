const form = document.getElementById("uploadForm");
const loading = document.getElementById("loading");

if(form){
    form.addEventListener("submit", function(){
        loading.style.display = "block";
    });
}

let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");

if(recordBtn){

recordBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.start();
    recordBtn.disabled = true;
    stopBtn.disabled = false;

    mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
    };
};

stopBtn.onclick = () => {
    mediaRecorder.stop();
    recordBtn.disabled = false;
    stopBtn.disabled = true;

    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: "audio/wav" });
        audioChunks = [];

        const formData = new FormData();
        formData.append("audio", blob, "recording.wav");

        document.getElementById("loading").style.display = "block";

        fetch("/analyze", {
            method: "POST",
            body: formData
        })
        .then(res => res.text())
        .then(html => {
            document.open();
            document.write(html);
            document.close();
        });
    };
};

}