async function fetch_data(){
    const url = "http://127.0.0.1:5500/upload";
    try{
        const response = await fetch(url);
        if (!response.ok){
            throw new Error(`HTTP Error! Status code ${response.status}`);
        }
        const data = await response.json();
        console.log(data);
    }
    catch (error){
        console.error("Failed to fetch data!")
    }

}