const OpenAI = require("openai");
const fs = require("fs");
const path = require("path");

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

let catalogueData = "";
try {
    catalogueData = fs.readFileSync(
        path.join(__dirname, "../../data/catalogue-data.txt"),
        "utf8"
    );
    catalogueData = catalogueData.substring(0, 15000);
} catch (e) {
    catalogueData = "General KSB pump catalogue information";
}

exports.handler = async (event) => {
    // Return early if not a POST request
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: "Method Not Allowed" };
    }

    try {
        const body = JSON.parse(event.body || "{}");
        
        // --- SECURE CONTEXT RESOLUTION LAYER ---
        let processedMessages = [];
        let stringToParse = "";

        // Check if history is passed and formatted correctly
        if (body.history && Array.isArray(body.history) && body.history.length > 0) {
            processedMessages = body.history.map(msg => ({
                role: msg.role === "assistant" ? "assistant" : "user",
                content: String(msg.content || "")
            }));
            stringToParse = String(body.history[body.history.length - 1].content || "");
        } else if (body.message) {
            // Fallback immediately to standard single-message style if history fails
            processedMessages = [{ role: "user", content: String(body.message) }];
            stringToParse = String(body.message);
        } else {
            processedMessages = [{ role: "user", content: "Hello" }];
            stringToParse = "hello";
        }

        const userMessageLower = stringToParse.toLowerCase();
        const flowMatch = userMessageLower.match(/(\d+)\s*m3\/hr/i);
        const headMatch = userMessageLower.match(/(?:,|\s)(\d+)\s*m(?!3)/i);
        const hvacMatch = userMessageLower.includes("hvac");
        
        let applicationType = "general"; 
        let engineeringData = "general\n";

        if (flowMatch) engineeringData += `Flow: ${flowMatch[1]} m3/hr\n`;
        if (headMatch) engineeringData += `Head: ${headMatch[1]} m\n`;
        if (hvacMatch) {
            applicationType = "hvac";
            engineeringData += `Application: HVAC\n`;
        }

        if (
            userMessageLower.includes("home") ||
            userMessageLower.includes("house") ||
            userMessageLower.includes("domestic")
        ) {
            applicationType = "domestic";
        }

        let relevantCatalogue = "";
        if (applicationType === "hvac") {
            relevantCatalogue = catalogueData.split("=====").filter(text =>
                text.toLowerCase().includes("hvac") || text.toLowerCase().includes("etaline") || text.toLowerCase().includes("etanorm")
            ).join("\n");
        } else if (applicationType === "domestic") {
            relevantCatalogue = catalogueData.split("=====").filter(text =>
                text.toLowerCase().includes("domestic") || text.toLowerCase().includes("home") || text.toLowerCase().includes("submersible") || text.toLowerCase().includes("mini")
            ).join("\n");
        } else {
            relevantCatalogue = catalogueData.substring(0, 12000);
        }
        relevantCatalogue = relevantCatalogue.substring(0, 12000);

        const systemMessage = {
            role: "system",
            content: `
You are Hydrokrat AI, a senior KSB pump selection expert capable of sizing pumps for Domestic, Commercial, Industrial, Agricultural, and Solar applications.

CATALOGUE DATA:
${relevantCatalogue}

ENGINEERING INPUT FROM PARSER:
${engineeringData}

// --- UPDATE JUST THE "OUTPUT FORMAT" SECTION INSIDE YOUR CHAT.JS SYSTEM PROMPT ---

==================================================
OUTPUT FORMAT (STRICTLY USE THIS FOR ALL REPLIES):
Make your answers incredibly punchy, clean, and spaced out. 
Avoid clumped text. Use clear bullet points and line breaks (<br>).

🚀 **RECOMMENDED PUMP**
* **Model:** [Exact Model Name & Series]
* **Category:** [Domestic / HVAC / Fire Fighting / Agri / Solar / Dewatering]

---

🔧 **WHY IT FITS YOUR SETUP**
* [Give a short, 1-sentence explanation of why it works for their specific history]
* [Mention a standout benefit like "Quiet operation" or "Clog-resistant design"]

---

📊 **ESTIMATED TECH SPECS**
* **Flow Rate:** [Standard range range, e.g., 3 – 6 m³/h]
* **Max Head:** [Standard head range, e.g., Up to 10 meters]

---

💡 **QUICK PRO-TIP**
* [Short, high-value 1-sentence installation or operational tip]

==================================================
`
        };

        const finalMessages = [systemMessage, ...processedMessages];

        const completion = await openai.chat.completions.create({
            model: "gpt-4.1-mini", // Reverted back to your explicit target engine
            messages: finalMessages,
            temperature: 0.7,
            max_tokens: 350
        });

        return {
            statusCode: 200,
            headers: { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*" // Failsafe for local dev testing
            },
            body: JSON.stringify({ reply: completion.choices[0].message.content })
        };

    } catch (error) {
        console.error("Backend Stack Trace:", error);
        return {
            statusCode: 500,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ reply: "AI Server Error: " + error.message })
        };
    }
};