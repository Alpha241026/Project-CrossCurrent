const proInput = document.querySelector("#pro-input");
const proButton = document.querySelector("#pro-button");
const proList = document.querySelector("#project-list");

const methodSelect = document.querySelector("#method");
const urlInput = document.querySelector("#url");
const bodyInput = document.querySelector("#request-body");

const sendButton = document.querySelector("#send-btn");

const statusOutput = document.querySelector("#status-output");
const responseOutput = document.querySelector("#response-output");

proButton.addEventListener("click", createProject); //create a project when the button is clicked
sendButton.addEventListener("click", sendRequest);  //send the configured HTTP request

//sends a new project to the backend
function createProject() {
    const name = proInput.value;

    //prevent empty project names
    if (name.trim() == "") {
        alert("Name can't be empty!");
        return;
    }

    fetch("http://127.0.0.1:5000/projects", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name })
    }).then(() => {
        proInput.value = ""; //clear the input and refresh the project list
        loadProjects();
    });
}

//fetches and displays all projects
function loadProjects() {
    fetch("http://127.0.0.1:5000/projects", {
        method: "GET"
    }).then((response) => {
        return response.json();
    }).then((data) => {

        proList.innerHTML = ""; //rebuild the sidebar from the latest backend data

        for (const project of data) {
            const projectItem = document.createElement("li");
            projectItem.textContent = project.name;
            proList.appendChild(projectItem);
        }
    });
}

//sends an HTTP request from the request builder
function sendRequest() {

    //read the request inputs
    const method = methodSelect.value;
    const url = urlInput.value;
    const body = bodyInput.value;

    //prevent empty URLs
    if (url.trim() === "") {
        alert("URL can't be empty!");
        return;
    }

    //build the original request configuration
    const options = {
        method
    };

    //only attach a body for non-GET requests
    if (method !== "GET") {
        options.headers = {
            "Content-Type": "application/json"
        };

        options.body = body;
    }

    //send the request details to the backend for execution
    fetch("http://127.0.0.1:5000/execute", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            method: method,
            url: url,
            body: method === "GET" ? null : JSON.parse(body)
        })

    })
    .then((response) => { //read the backend response

        return response.json();

    })
    .then((data) => { //update the status and response panels

        statusOutput.textContent = data.status;
        responseOutput.textContent = JSON.stringify(data.body, null, 2);

    })
    .catch((error) => { //display request errors

        statusOutput.textContent = "Request Failed";
        responseOutput.textContent = error.message;

    });
}

loadProjects();