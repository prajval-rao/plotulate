import { createGrid, ModuleRegistry, AllCommunityModule } from 'https://cdn.jsdelivr.net/npm/ag-grid-community@latest/+esm';
let gridApi = null;
ModuleRegistry.registerModules([AllCommunityModule]);
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