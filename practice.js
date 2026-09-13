const dir = document.getElementById("direct");

dir.addEventListener("click", () => {
    fetch("https://jsonplaceholder.typicode.com/users/1")
        .then((response) => {
            if (!response.ok){
                throw new Error("Network response was not OK");
            }
            return response.json();
        })
        .then((userData) => {
            console.log(`Name: ${userData.name}`);
            console.log(`Email Address: ${userData.email}`)
        })
        .catch((error) => {
            console.error("Something went wrong", error.message)
        })
})

    





