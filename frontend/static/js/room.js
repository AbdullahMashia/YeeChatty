

let messages = document.getElementById("messages");
let chat_square = document.getElementById("chat_square");

let mess = [
     "hello", "hi","what is up?","how are you?","great what about you?","awsome",
    "what is your name","hello", "hi","what is up?","how are you?","great what about you?",
     "hello", "hi","what is up?","how are you?","great what about you?","awsome",
    "what is your name","hello", "hi","what is up?","how are you?","great what about you?",
     "hello", "hi","what is up?","how are you?","great what about you?","awsome",
    "what is your name","hello", "hi","what is up?","how are you?","great what about you?"
];
let colora=["grey","blue",];



window.addEventListener("load",message_loader);

let date = "2020 25 32 mon 14:32 pm";


function builder(messages_load)
{
    if (!Array.isArray(messages_load))
    {
        let m = document.createElement("li");
        m.innerText = messages_load["m"];
        m.style.padding = "2vw";
        m.style.backgroundColor = "grey";
        m.style.fontSize = "2rem";
        messages.style +="     align-items: center;justify-content: center;";
        messages.appendChild(m);
        chat_square.style.background="transparent";
        return;


    }

      messages_load.forEach(element => {



            let message_container = document.createElement("li");
            let message= document.createElement("p");


            let m_info = document.createElement("p");
            if(element["type"]== "rec")
            {
            message.classList.add("recv_me");
            message_container.classList.add("recv_c");
            m_info.innerText=element["sent_at"];











            }
            else{
                message.classList.add("my_m");
                message_container.classList.add("my_c");
                m_info.innerText=element["sent_at"]





            }

            m_info.classList.add("m_info");
            message.innerText =element["content"];
            message_container.appendChild(message);



            message_container.appendChild(m_info);

            messages.appendChild(message_container);


    });





}



async function message_loader(){
    let res = await fetch(`/api/chats/room`);
    let ser_res = await res.json();

    builder(ser_res);
    console.log("response=>",ser_res);
}
















