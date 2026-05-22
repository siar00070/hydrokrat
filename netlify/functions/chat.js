exports.handler = async function(event) {

  try {

    const { message } = JSON.parse(event.body);

    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content: `
You are Hydrokrat AI Assistant.

Hydrokrat Ventures is an authorized KSB pumps distributor in Tamil Nadu.

You help customers with:
- Fire Fighting Pumps
- HVAC Pumps
- Booster Systems
- Water Transfer Pumps
- Industrial Pump Solutions

Reply professionally like a sales engineer.
Keep replies short, clear, and professional.
Always encourage WhatsApp enquiry for quotations.
`
          },
          {
            role: "user",
            content: message
          }
        ],
        temperature: 0.7
      })
    });

    const data = await response.json();

    return {
      statusCode: 200,
      body: JSON.stringify({
        reply: data.choices[0].message.content
      })
    };

  } catch (error) {

    return {
      statusCode: 500,
      body: JSON.stringify({
        error: error.message
      })
    };

  }

};
