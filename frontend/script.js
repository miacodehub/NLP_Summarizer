const form = document.getElementById("uploadForm");
const answerText = document.getElementById("answerText");
const filesContainer = document.getElementById("filesContainer");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const input = document.getElementById("fileInput");
    const files = input.files;
    const query = document.getElementById("query").value;

    const formData = new FormData();

    formData.append("query", query);

    for (const file of files) {
        formData.append("files", file);
    }

    // Clear previous results
    answerText.innerText = "Processing...";
    filesContainer.innerHTML = "";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            answerText.innerText =
                data.detail || "Something went wrong.";
            return;
        }

        answerText.innerText = data.answer;

        for (const source of data.sources) {

            const entry = document.createElement("div");

            entry.className = "file-entry";

            entry.innerHTML = `
                <strong>${source.filename}</strong>
                <span>
                    Similarity: ${source.score.toFixed(3)}
                </span>
            `;

            filesContainer.appendChild(entry);
        }

    } catch (error) {

        answerText.innerText =
            "Could not connect to the backend.";

        console.error(error);
    }
});