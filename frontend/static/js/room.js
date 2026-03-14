



// let messages = document.getElementById("messages");
// let chat_square = document.getElementById("chat_square");

// let conv_id =0;




// window.addEventListener("load",message_loader);



// function builder(messages_load)
// {
//     console.log("conver_id:=>",conv_id);
//     if (!Array.isArray(messages_load))
//     {
//         let m = document.createElement("li");
//         m.innerText = messages_load["m"];
//         m.style.padding = "2vw";
//         m.style.backgroundColor = "grey";
//         m.style.fontSize = "2rem";
//         messages.style ="     align-items: center;justify-content: center;";
//         messages.appendChild(m);
//         chat_square.style.background="transparent";
//         return;


//     }

//       messages_load.forEach(element => {



//             let message_container = document.createElement("li");
//             let message= document.createElement("p");


//             let m_info = document.createElement("p");
//             if(element["type"]== "rec")
//             {
//             message.classList.add("recv_me");
//             message_container.classList.add("recv_c");
//             m_info.innerText=element["sent_at"];











//             }
//             else{
//                 message.classList.add("my_m");
//                 message_container.classList.add("my_c");
//                 m_info.innerText=element["sent_at"]





//             }

//             m_info.classList.add("m_info");
//             message.innerText =element["content"];
//             message_container.appendChild(message);



//             message_container.appendChild(m_info);

//             messages.appendChild(message_container);


//     });





// }



// async function message_loader(){
//     let res = await fetch(`/api/chats/room`);
//     let ser_res = await res.json();



//     if(Array.isArray(ser_res))
//     {
//         conv_id = ser_res[0]["conv_id"];
//         ser_res.shift();
//     }



//     console.log();
//     builder(ser_res);
//     console.log("response=>",ser_res);


// }





// function joining_room(){
//     const socket =io({transport:['websocket'],query:{token:'xyz'}});
//     let data = {'event':'join_room','m':"fuckyou_man"};

//         socket.emit('join_room',data);









// }













let messages = document.getElementById("messages");
let chat_square = document.getElementById("chat_square");
let conv_id = 0;
let socket = null;   // store socket globally

window.addEventListener("load", message_loader);

function builder(messages_load) {
    console.log("conv_id:=>", conv_id);
    if (!Array.isArray(messages_load)) {
        // single message (error or single)
        let m = document.createElement("li");
        m.innerText = messages_load["m"];
        m.style.padding = "2vw";
        m.style.backgroundColor = "grey";
        m.style.fontSize = "2rem";
        messages.style.alignItems = "center";
        messages.style.justifyContent = "center";
        messages.appendChild(m);
        chat_square.style.background = "transparent";
        return;
    }

    messages_load.forEach(element => {
        let message_container = document.createElement("li");
        let message = document.createElement("p");
        let m_info = document.createElement("p");

        if (element["type"] == "rec") {
            message.classList.add("recv_me");
            message_container.classList.add("recv_c");
        } else {
            message.classList.add("my_m");
            message_container.classList.add("my_c");
        }
        m_info.innerText = element["sent_at"];
        m_info.classList.add("m_info");
        message.innerText = element["content"];

        message_container.appendChild(message);
        message_container.appendChild(m_info);
        messages.appendChild(message_container);
    });
}

async function message_loader() {
    let res = await fetch(`/api/chats/room`);
    let ser_res = await res.json();

    if (Array.isArray(ser_res) && ser_res.length > 0) {
        conv_id = ser_res[0]["conv_id"];
        ser_res.shift();                 // now safely inside the if block
    } else {
        console.error("Unexpected response format:", ser_res);
        return;
    }

    console.log("response=>", ser_res);
    builder(ser_res);
    joining_room();   // connect socket after loading messages
}

function joining_room() {
    console.log("Creating socket...");
    socket = io({ transports: ['websocket'] });
    socket.on('connect', () => {
        console.log("Socket connected, emitting join_room with conv_id:", conv_id);
        socket.emit('join_room', { conversation_id: conv_id });
    });
    socket.on('new_message', (data) => {
        console.log("New message received:", data);
    });
    socket.on('error', (err) => console.error("Socket error:", err));
}













