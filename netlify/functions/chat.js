```javascript id="0a1xjlwm"
async function sendMessage(){

    const message = userInput.value.trim();

    if(!message) return;

    addUserMessage(message);

    userInput.value = "";

    showTyping();

    try{

        const response = await fetch("/.netlify/functions/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        removeTyping();

        if(data.reply){
            addBotMessage(data.reply);
        } else {
            addBotMessage("AI response unavailable.");
        }

    }catch(error){

        removeTyping();

        addBotMessage("Server connection error.");

        console.error(error);

    }

}
```
