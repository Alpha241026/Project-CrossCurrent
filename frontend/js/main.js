const proInput = document.querySelector("#pro-input")
const proButton = document.querySelector("#pro-button");
const proList = document.querySelector("#project-list");

proButton.addEventListener("click", createProject); //create a project when the button is clicked

//sends a new project to the backend
function createProject() {
    const name = proInput.value;

    //prevent empty project names
    if (name.trim()=="") {
            alert("Name can't be empty!")
            return
    }
    
    fetch("http://127.0.0.1:5000/projects", {method: "POST", headers: {"Content-Type":"application/json"}, body:JSON.stringify({ name })
    }).then(()=>{
        proInput.value=""; //clear the input and refresh the project list
        loadProjects();
    });

}

//fetches and displays all projects
function loadProjects() {
    fetch("http://127.0.0.1:5000/projects", {
    method: "GET"
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        proList.innerHTML = ""; //rebuild the sidebar from the latest backend data
        for(const project of data) {
            const projectItem = document.createElement("li");
            projectItem.textContent = project.name;
            proList.appendChild(projectItem);
        }
    })
}

loadProjects(); //load existing projects when the page opens