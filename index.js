import { createGrid, ModuleRegistry, AllCommunityModule } from 'https://cdn.jsdelivr.net/npm/ag-grid-community@latest/+esm';
let gridApi = null;
ModuleRegistry.registerModules([AllCommunityModule]);
let filedata = null;
let file = null;
let data_for_query = null;

document.getElementById("uploadfile").addEventListener("submit", async (e) => {e.preventDefault();
    /* change to track: const filedata and file now not const as query should access these */
    filedata = document.getElementById("data");
    file = filedata.files[0];
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
        data_for_query = cleandata.content;
        const rows = cleandata.content;
        rows.forEach(row => {
            console.log(row);
        })

        const generatedColDefs = Object.keys(rows[0]).map(key => {
        return {
            field: key,
            headerName: key.charAt(0).toUpperCase() + key.slice(1)
        };
        });

        const gridOptions = {
        columnDefs: generatedColDefs,
        rowData: rows,
        
        defaultColDef: {
            sortable: true,
            filter: true,
            editable: true,
            flex: 1
        }
        };

        let gridDiv = document.getElementById("myGrid");
        if (gridApi){
            gridApi.setGridOption("columnDefs", generatedColDefs);
            gridApi.setGridOption("rowData", rows);
            gridApi.sizeColumnsToFit();
        }
        else{
            gridDiv.innerHTML = "";
            gridApi = createGrid(gridDiv, gridOptions);
            gridApi.sizeColumnsToFit();
        }
    }
    catch(error){
        console.error("Error!", error);
        alert("Failed");
    }
})

const openBtn = document.getElementById('openBtn');
const closeBtn = document.getElementById('closeBtn');
const overlay = document.getElementById('popupOverlay');
let opened = false;

overlay.style.display = 'none';

openBtn.addEventListener('click', () => {
    if (opened){
        overlay.style.display = 'none';
        opened = false;
    }
    else{
        overlay.style.display = 'flex';
        opened = true;
    }
});

// Hide the popup
closeBtn.addEventListener('click', () => {
  overlay.style.display = 'none';
});

// Optional: Close if user clicks anywhere outside the box
window.addEventListener('click', (e) => {
  if (e.target === overlay) {
    overlay.style.display = 'none';
  }
});

const prompt_button = document.getElementById("promptcall");
let generated_response = document.getElementById("llm_response");

document.getElementById("query_form").addEventListener("submit", async (e) => {e.preventDefault();
    if (!userprompt.value){
        generated_response.textContent = "You have not typed a prompt, which is necessary for a response. "
    }
    else if (!data_for_query){
        generated_response.textContent = "No document provided!";
    }
    else{
        try{
            const response = await fetch("http://127.0.0.1:8000/query/generate_response", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: userprompt.value,
                    session_id: "session1",
                    file_content: data_for_query
                })
            })
            if (!response.ok) throw new Error("Server error returning LLM response!!!");
            const clean_response = await response.json();
            generated_response.textContent = clean_response.output;
        }
        catch(error){
            console.error("Error!", error)
            alert("LLM response failed to fetch")
        }
    }
})