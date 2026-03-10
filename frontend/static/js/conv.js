
let messages = document.getElementById("messages");

let mess = [
     "hello", "hi","what is up?","how are you?","great what about you?","awsome",
    "what is your name","hello", "hi","what is up?","how are you?","great what about you?",
     "hello", "hi","what is up?","how are you?","great what about you?","awsome",
    "what is your name","hello", "hi","what is up?","how are you?","great what about you?",
     "hello", "hi","what is up?","how are you?","great what about you?","awsome",
    "what is your name","hello", "hi","what is up?","how are you?","great what about you?"
];
let colora=["grey","blue",];





let date = "2020 25 32 mon 14:32 pm";


for(let i=0 ; i<30; i++)
{

    let message_container = document.createElement("li");
    let message= document.createElement("p");


    let m_info = document.createElement("p");
    if((i+1)%2==0)
    {
    message.classList.add("recv_me");
    message_container.classList.add("recv_c");
    m_info.innerText=date;











    }
    else{
        message.classList.add("my_m");
        message_container.classList.add("my_c");
        m_info.innerText=date;





    }

     m_info.classList.add("m_info");
    message.innerText =mess[i];
    message_container.appendChild(message);



     message_container.appendChild(m_info);

    messages.appendChild(message_container);

}