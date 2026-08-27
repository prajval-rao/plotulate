document.querySelector("form").addEventListener("submit", async (e) => {e.preventDefault();
    const filedata = document.getElementById("data");
    const file = filedata.files[0];
    if (!file){
        alert("Select an Excel File first!!");
        return;
    }
    const formdata = new FormData();
    formdata.append("file", file);
    try{
        const response = await fetch("http://127.0.0.1:8000/submit", {
            method: "POST",
            body: formdata
        });
        if (!response.ok) throw new Error("Server error parsing Excel File!!!");
        const cleandata = await response.json();
        console.log("Cleaned data: ", cleandata.filename);
        const rows = cleandata.content;
        rows.forEach(row => {
            console.log(row);
        })
    }
    catch(error){
        console.error("Upload failed", error);
        alert("Failed")
    }
})