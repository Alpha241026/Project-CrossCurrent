const proInput = document.querySelector("#pro-input");
const proDescriptionInput = document.querySelector("#pro-description-input");
const proButton = document.querySelector("#pro-button");
const proList = document.querySelector("#project-list");

const methodSelect = document.querySelector("#method");
const urlInput = document.querySelector("#url");
const paramsContainer = document.querySelector("#params-container");
const addParamButton = document.querySelector("#add-param-btn");
const headersContainer = document.querySelector("#headers-container");
const addHeadersButton = document.querySelector("#add-headers-btn");
const bodyInput = document.querySelector("#request-body");
const endpointNameInput = document.querySelector("#endpoint-name");
const endpointDescriptionInput = document.querySelector("#endpoint-description");

const saveEndpointButton = document.querySelector("#save-endpoint-btn");
const sendButton = document.querySelector("#send-btn");

const statusOutput = document.querySelector("#status-output");
const responseOutput = document.querySelector("#response-output");

const historyList = document.getElementById("history-list");
const refreshHistoryBtn = document.getElementById("refresh-history-btn");

let selectedProjectID = null; //store ID of currently selected project, none project selected on initial page load
let selectedEndpoint = null; //store the currently selected endpoint and its request configuration
let editingEndpointID = null; //store the ID of the endpoint currently being edited


proButton.addEventListener("click", createProject); //create a project when the button is clicked


addParamButton.addEventListener("click", () => { //create a params row when the button is clicked
    paramsContainer.appendChild(createParamRow());
});


addHeadersButton.addEventListener("click", () => { //create a headers row when the button is clicked
    headersContainer.appendChild(createHeadersRow());
});


saveEndpointButton.addEventListener("click", saveEndpoint); //save the endpoint in the menu when the button is clicked
sendButton.addEventListener("click", sendRequest); //send the configured HTTP request



//sends a new project to the backend
function createProject() {
    const name = proInput.value;
    const description = proDescriptionInput.value;

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
        body: JSON.stringify({
            name: name,
            description: description
        })
    }).then(() => {
        proInput.value = "";
        proDescriptionInput.value = "";

        //clear the input fields and refresh the project list
        loadProjects();
    });
}



//fetches and displays all projects
function loadProjects(expandProjectID = null) {
    fetch("http://127.0.0.1:5000/projects", {
        method: "GET"
    }).then((response) => {
        return response.json();
    }).then((data) => {

        proList.innerHTML = ""; //rebuild the sidebar from the latest backend project data

        for (const project of data) {
            const projectItem = document.createElement("li");

            //attach the backend project ID to the project list item
            projectItem.dataset.projectId = project.id;

            //display the project name separately so action buttons can sit beside it
            const projectName = document.createElement("span");
            projectName.className = "project-name";
            projectName.textContent = project.name;

            //display the project description when one exists
            const projectDescription = document.createElement("div");
            projectDescription.className = "project-description";
            projectDescription.textContent = project.description || "";

            //create project update button
            const editButton = document.createElement("button");
            editButton.textContent = "Edit";

            //create project delete button
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";

            //handle project selection
            projectItem.addEventListener("click", () => {

                //store the selected project's ID for later endpoint operations
                selectedProjectID = Number(projectItem.dataset.projectId);

                //a new project selection means no endpoint is currently selected
                selectedEndpoint = null;

                loadEndpoints(selectedProjectID, projectItem);
                console.log(selectedProjectID);
            });

            //handle project update without triggering project selection
            editButton.addEventListener("click", (event) => {
                event.stopPropagation();
                updateProject(project.id, projectItem, project.description);
            });

            //handle project deletion without triggering project selection
            deleteButton.addEventListener("click", (event) => {
                event.stopPropagation();
                deleteProject(project.id);
            });

            projectItem.appendChild(projectName);
            projectItem.appendChild(editButton);
            projectItem.appendChild(deleteButton);

            //only display the description when the project has one
            if (project.description) {
                projectItem.appendChild(projectDescription);
            }

            proList.appendChild(projectItem);

            //restore the endpoint list after refreshing an updated project
            if (expandProjectID === project.id) {
                loadEndpoints(project.id, projectItem);
            }
        }
    });
}



//updates the name and description of an existing project
function updateProject(projectID, projectItem, currentDescription) {

    //find the currently displayed project name
    const projectName = projectItem.querySelector(".project-name");

    //prevent multiple edit inputs on the same project
    if (projectItem.querySelector(".project-edit-input")) {
        return;
    }

    //replace the displayed name with an editable input
    const editInput = document.createElement("input");
    editInput.className = "project-edit-input";
    editInput.value = projectName.textContent;

    //create an editable project description field
    const descriptionInput = document.createElement("textarea");
    descriptionInput.className = "project-edit-description";
    descriptionInput.placeholder = "Description";
    descriptionInput.value = currentDescription || "";

    //create a button to confirm the new name and description
    const saveButton = document.createElement("button");
    saveButton.textContent = "Save";

    //replace the project name with the edit controls
    projectName.replaceWith(editInput);
    editInput.after(descriptionInput);
    descriptionInput.after(saveButton);

    //save the updated project name and description
    saveButton.addEventListener("click", (event) => {
        event.stopPropagation();

        const name = editInput.value;
        const description = descriptionInput.value;

        //prevent empty project names
        if (name.trim() === "") {
            alert("Project name can't be empty!");
            return;
        }

        fetch(`http://127.0.0.1:5000/projects/${projectID}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                description: description
            })
        })
        .then((response) => {
            return response.json();
        })
        .then(() => {

            //refresh the project list after a successful update
            loadProjects(projectID);
        })
        .catch((error) => {
            alert("Failed to update project: " + error.message);
        });
    });
}



//deletes an existing project
function deleteProject(projectID) {

    //confirm before permanently deleting the project and its endpoints
    if (!confirm("Delete this project and all its endpoints?")) {
        return;
    }

    fetch(`http://127.0.0.1:5000/projects/${projectID}`, {
        method: "DELETE"
    })
    .then((response) => {
        return response.json();
    })
    .then(() => {

        //clear selection if the deleted project was currently selected
        if (selectedProjectID === projectID) {
            selectedProjectID = null;
            selectedEndpoint = null;
        }

        //refresh the project list after deletion
        loadProjects();
    })
    .catch((error) => {

        //display a basic error if deleting the project fails
        alert("Failed to delete project: " + error.message);
    });
}



//fetches and displays all endpoints
function loadEndpoints(projectID, projectItem) {
    fetch(`http://127.0.0.1:5000/projects/${projectID}/endpoints`, {
        method: "GET"
    }).then((response) => {
        return response.json();
    }).then((data) => {

        //remove endpoint lists from previously selected projects
        document.querySelectorAll(".endpoint-list").forEach((list) => list.remove());

        //create a new endpoint list inside the selected project
        const endpointList = document.createElement("ul");
        endpointList.className = "endpoint-list";

        for (const ep of data) {
            const endpointItem = document.createElement("li");

            //attach the backend endpoint ID to the endpoint list item
            endpointItem.dataset.endpointId = ep.id;

            //create endpoint name display
            const endpointName = document.createElement("span");
            endpointName.className = "endpoint-name";
            endpointName.textContent = ep.name;

            //create endpoint Edit button
            const editButton = document.createElement("button");
            editButton.textContent = "Edit";

            //create endpoint Delete button
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";

            //handle endpoint selection
            endpointItem.addEventListener("click", (event) => {
                event.stopPropagation();

                //store the complete endpoint object for use by the request builder
                selectedEndpoint = ep;
                loadEndpointIntoBuilder(ep);
                console.log(selectedEndpoint);
            });

            //handle endpoint editing
            editButton.addEventListener("click", (event) => {
                event.stopPropagation();

                //store which endpoint is being edited
                editingEndpointID = ep.id;

                //load the endpoint's existing configuration into the request builder
                selectedEndpoint = ep;
                loadEndpointIntoBuilder(ep);

                //change Save button into Update button
                saveEndpointButton.textContent = "Update";
            });

            //handle endpoint deletion
            deleteButton.addEventListener("click", (event) => {
                event.stopPropagation();

                deleteEndpoint(projectID, ep.id);
            });

            endpointItem.appendChild(endpointName);
            endpointItem.appendChild(editButton);
            endpointItem.appendChild(deleteButton);

            endpointList.appendChild(endpointItem);
        }

        //attach this project's endpoints underneath its project item
        projectItem.appendChild(endpointList);
    });
}



//populates the request builder after an endpoint is selected
function loadEndpointIntoBuilder(endpoint) {
    methodSelect.value = endpoint.method;
    urlInput.value = endpoint.url;
    endpointNameInput.value = endpoint.name;
    endpointDescriptionInput.value = endpoint.description || "";

    //clear existing parameter rows before loading the endpoint's params
    paramsContainer.innerHTML = "";

    //recreate a row for every saved parameter
    for (const [key, value] of Object.entries(endpoint.params || {})) {
        const row = createParamRow();

        row.children[0].value = key;
        row.children[1].value = value;

        paramsContainer.appendChild(row);
    }

    //clear existing header rows before loading the endpoint's headers
    headersContainer.innerHTML = "";

    //recreate a row for every saved header
    for (const [key, value] of Object.entries(endpoint.headers || {})) {
        const row = createHeadersRow();

        row.children[0].value = key;
        row.children[1].value = value;

        headersContainer.appendChild(row);
    }

    //load the saved request body
    if (endpoint.body === null) {
        bodyInput.value = "";
    } else {
        bodyInput.value = JSON.stringify(endpoint.body, null, 2);
    }

    //load saved execution history for the selected endpoint
    loadExecutionHistory();
}



//creates params row
function createParamRow() {
    //creating parent div
    const row = document.createElement("div");
    row.className = "param-row";

    //creating the three child elements below
    const keyInput = document.createElement("input");
    keyInput.placeholder = "Key";

    const valueInput = document.createElement("input");
    valueInput.placeholder = "Value";

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";

    //make the button remove its own row
    deleteButton.addEventListener("click", () => {
        row.remove();
    });

    //attaching children to the row
    row.appendChild(keyInput);
    row.appendChild(valueInput);
    row.appendChild(deleteButton);

    return row; //returning the finished row
}



//creates headers row
function createHeadersRow() {
    //creating parent div
    const row = document.createElement("div");
    row.className = "header-row";

    //creating the three child elements below
    const keyInput = document.createElement("input");
    keyInput.placeholder = "Key";

    const valueInput = document.createElement("input");
    valueInput.placeholder = "Value";

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";

    //make the button remove its own row
    deleteButton.addEventListener("click", () => {
        row.remove();
    });

    //attaching children to the row
    row.appendChild(keyInput);
    row.appendChild(valueInput);
    row.appendChild(deleteButton);

    return row; //returning the finished row
}



//collects all parameter rows from the Params editor
function collectParams() {
    const params = {};

    const rows = paramsContainer.querySelectorAll(".param-row");

    for (const row of rows) {
        const key = row.children[0].value.trim();
        const value = row.children[1].value;

        //ignore completely empty rows
        if (key !== "") {
            params[key] = value;
        }
    }

    return params;
}



//collects all header rows from the Headers editor
function collectHeaders() {
    const headers = {};

    const rows = headersContainer.querySelectorAll(".header-row");

    for (const row of rows) {
        const key = row.children[0].value.trim();
        const value = row.children[1].value;

        //ignore completely empty rows
        if (key !== "") {
            headers[key] = value;
        }
    }

    return headers;
}



//saves a new endpoint or updates an existing endpoint
function saveEndpoint() {

    //a project must be selected before an endpoint can be saved
    if (selectedProjectID === null) {
        alert("Select a project first!");
        return;
    }

    //read the endpoint details from the request builder
    const name = endpointNameInput.value;
    const description = endpointDescriptionInput.value;
    const method = methodSelect.value;
    const url = urlInput.value;
    const body = bodyInput.value;
    const params = collectParams();
    const headers = collectHeaders();

    //prevent an empty endpoint name
    if (name.trim() === "") {
        alert("Endpoint name can't be empty!");
        return;
    }

    //prevent an empty URL
    if (url.trim() === "") {
        alert("URL can't be empty!");
        return;
    }

    //parse the request body only when one is provided
    let parsedBody = null;

    if (body.trim() !== "") {
        try {
            parsedBody = JSON.parse(body);
        } catch {
            alert("Body must contain valid JSON!");
            return;
        }
    }

    //choose PATCH when editing, otherwise POST when creating
    const isEditing = editingEndpointID !== null;

    const urlPath = isEditing
        ? `http://127.0.0.1:5000/endpoints/${editingEndpointID}`
        : `http://127.0.0.1:5000/projects/${selectedProjectID}/endpoints`;

    const methodType = isEditing ? "PATCH" : "POST";

    fetch(urlPath, {
        method: methodType,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            method: method,
            url: url,
            description: description,
            params: params,
            headers: headers,
            body: parsedBody
        })
    })
    .then((response) => {
        return response.json();
    })
    .then(() => {

        //reset endpoint editing state after a successful save/update
        editingEndpointID = null;
        selectedEndpoint = null;

        //restore the button to normal Save mode
        saveEndpointButton.textContent = "Save";

        //clear the endpoint name and description fields
        endpointNameInput.value = "";
        endpointDescriptionInput.value = "";

        //refresh the endpoint list for the currently selected project
        const selectedProjectItem =
            document.querySelector(`[data-project-id="${selectedProjectID}"]`);

        loadEndpoints(selectedProjectID, selectedProjectItem);
    })
    .catch((error) => {

        //display a basic error if saving/updating the endpoint fails
        alert("Failed to save endpoint: " + error.message);
    });
}



//deletes an existing endpoint
function deleteEndpoint(projectID, endpointID) {

    //confirm before permanently deleting the endpoint
    if (!confirm("Delete this endpoint?")) {
        return;
    }

    fetch(`http://127.0.0.1:5000/endpoints/${endpointID}`, {
        method: "DELETE"
    })
    .then((response) => {
        return response.json();
    })
    .then(() => {

        //clear selection if the deleted endpoint was currently selected
        if (selectedEndpoint && selectedEndpoint.id === endpointID) {
            selectedEndpoint = null;
            editingEndpointID = null;
        }

        //restore the Save button in case we were editing this endpoint
        saveEndpointButton.textContent = "Save";

        //refresh the endpoint list for the selected project
        const selectedProjectItem =
            document.querySelector(`[data-project-id="${projectID}"]`);

        loadEndpoints(projectID, selectedProjectItem);
    })
    .catch((error) => {

        //display a basic error if endpoint deletion fails
        alert("Failed to delete endpoint: " + error.message);
    });
}



//sends an HTTP request from the request builder
function sendRequest() {

    //read the request inputs
    const method = methodSelect.value;
    const url = urlInput.value;
    const params = collectParams();
    const headers = collectHeaders();
    const body = bodyInput.value;

    //parse the request body only when one is provided
    let parsedBody = null;

    if (body.trim() !== "") {
        try {
            parsedBody = JSON.parse(body);
        } catch {
            alert("Body must contain valid JSON!");
            return;
        }
    }

    //prevent empty URLs
    if (url.trim() === "") {
        alert("URL can't be empty!");
        return;
    }

    //send the request details to the backend for execution
    fetch("http://127.0.0.1:5000/execute", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        //send the selected HTTP method, URL and parsed body to Chimera for execution
        body: JSON.stringify({
            endpoint_id: selectedEndpoint.id,
            method: method,
            url: url,
            params: params,
            headers: headers,
            body: method === "GET" ? null : parsedBody
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

    //refresh history after a new execution
    loadExecutionHistory();
}



//loads execution history for the currently selected endpoint
function loadExecutionHistory() {

    if (!selectedEndpoint) {
        historyList.innerHTML = '<p class="history-empty">Select an endpoint to view history</p>';
        return;
    }

    fetch(`http://localhost:8080/executions/endpoint/${selectedEndpoint.id}`)

        .then((response) => {

            if (!response.ok) {
                throw new Error("Failed to load execution history");
            }

            return response.json();

        })

        .then((executions) => {

            historyList.innerHTML = "";

            if (executions.length === 0) {
                historyList.innerHTML = '<p class="history-empty">No execution history yet</p>';
                return;
            }

            executions.forEach((execution) => {

                const historyItem = document.createElement("div");

                historyItem.className = "history-item";

                historyItem.dataset.executionId = execution.id;

                const status = execution.status_code ?? "Failed";

                const responseTime = execution.response_time !== null
                    ? `${execution.response_time} ms`
                    : "-";

                const executedAt = new Date(execution.executed_at);

                historyItem.innerHTML = `
                    <span class="history-status">${status}</span>
                    <span class="history-time">${responseTime}</span>
                    <span class="history-date">${executedAt.toLocaleString()}</span>
                `;

                historyItem.addEventListener("click", () => {
                    showExecution(execution);
                });

                historyList.appendChild(historyItem);
            });

        })

        .catch((error) => {

            historyList.innerHTML =
                `<p class="history-error">${error.message}</p>`;

        });
}



//shows the selected historical execution in the response viewer
function showExecution(execution) {

    statusOutput.textContent = execution.status_code ?? "Request Failed";

    responseOutput.textContent = JSON.stringify(
        execution.response_body,
        null,
        2
    );
}


//reloads execution history when the user requests a refresh
refreshHistoryBtn.addEventListener("click", () => {
    loadExecutionHistory();
});


loadProjects(); //populating sidebar from existing backend state when page opens