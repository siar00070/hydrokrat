document.addEventListener("DOMContentLoaded", function () {

    document.body.insertAdjacentHTML("beforeend", `

    <style>
    #chatbotFrame{
        position:fixed;
        bottom:90px;
        right:20px;
        width:360px;
        height:520px;
        border:none;
        z-index:9999;
        border-radius:12px;
        overflow:hidden;
        background:white;
        display:none;
        box-shadow:0 4px 15px rgba(0,0,0,0.3);
    }

    #chatbotButton{
        position:fixed;
        bottom:20px;
        right:20px;
        width:60px;
        height:60px;
        border-radius:50%;
        background:#007bff;
        color:white;
        font-size:28px;
        border:none;
        cursor:pointer;
        z-index:10000;
        box-shadow:0 4px 12px rgba(0,0,0,0.3);
    }
    </style>

    <iframe 
    id="chatbotFrame"
    src="pump_selection_chatbot.html">
    </iframe>

    <button id="chatbotButton">💬</button>

    `);

    const btn = document.getElementById("chatbotButton");
    const frame = document.getElementById("chatbotFrame");

    btn.addEventListener("click", function () {

        if (frame.style.display === "block") {
            frame.style.display = "none";
        } else {
            frame.style.display = "block";
        }

    });

});