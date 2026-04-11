const form = document.getElementById("uploadForm");
const loading = document.getElementById("loading");

if(form){
    form.addEventListener("submit", function(){
        loading.style.display = "block";
    });
}