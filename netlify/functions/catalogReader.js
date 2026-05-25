const fs = require("fs");
const path = require("path");
const pdfParse = require("pdf-parse");

async function readCatalogues() {

    const folderPath =
    path.join(__dirname, "../../catalogues");

    const files = fs.readdirSync(folderPath);

    let fullText = "";

    for (const file of files) {

        if (file.endsWith(".pdf")) {

            const filePath =
            path.join(folderPath, file);

            const dataBuffer =
            fs.readFileSync(filePath);

            const pdfData =
            await pdfParse(dataBuffer);

            fullText +=
            `\\n\\nCATALOGUE: ${file}\\n`;

            fullText += pdfData.text;
        }
    }

    return fullText;
}

module.exports = readCatalogues;