const form = document.getElementById("uploadForm");
const summaryText = document.getElementById("summaryText");
const showFilesBtn = document.getElementById("showFilesBtn");
const filesContainer = document.getElementById("filesContainer");

// fix 4 - moved outside submit handler so it only registers once
showFilesBtn.addEventListener("click", () => {
    const entries = JSON.parse(showFilesBtn.dataset.entries || "[]");

    let html = "";
    for (const entry of entries) {
        html += `
            <div class="file-entry">
                <h3>${entry.filename}</h3>
            </div>
        `;
    }
    filesContainer.innerHTML = html;
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const input = document.getElementById("fileInput");
    const files = input.files;
    const formData = new FormData();
    const keyword = document.getElementById("kword").value;

    formData.append("keyword", keyword);
    for (const file of files) {
        formData.append("files", file);
    }

    const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    summaryText.innerText = data.summary;

    // store entries on the button so the click handler can access them
    showFilesBtn.dataset.entries = JSON.stringify(data.entries);
});