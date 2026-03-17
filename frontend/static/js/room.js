

let messages = document.getElementById("messages");
let chat_square = document.getElementById("chat_square");
let send_but = document.getElementById("sender_but");
let message_field = document.getElementById("sender_text");
let message ;
let user_info = document.getElementById("user_info");
let conv_id ;
let username ;
let sent_at;
let room_name;
let chat_empty = false;
let messaging_started = false;

const socket =io({autoConnect:false});

    socket.on('connect',()=>console.log('connected successfully'));
    socket.on('error',()=>console.log("connection failed"));
    socket.on('join_room',(data)=>console.log(`joined room ${data["room"]}`))
    socket.on('new_message',(data)=>message_popping(data));

window.addEventListener("load",message_loader);

let date =new Date();
let join_room_d;

let new_message_d;







function build(messages_load,chat_empty)
{
    console.log("conver_id:=>",conv_id);
    console.log('chat empty = >',chat_empty);


    if(chat_empty)
    {
        empty_chat_splash(chat_empty,messaging_started,messages_load["m"]);

    }
    else{
         messages_load.forEach(element => {

        message_build(element);

    });
    }



    // Sending event listners


  messages.scrollTop = messages.scrollHeight;


}



async function message_loader(){
    let res = await fetch(`/api/chats/room`);
    let ser_res = await res.json();



    if(Array.isArray(ser_res))
    {
        conv_id = ser_res[0]["conv_id"];
        username = ser_res[0]["myusername"]
        console.log("user_name = >",username);
        room_name = ser_res[0]["room_name"];
        ser_res.shift();
        chat_empty= false;


    }
    else{

        if(ser_res["status"]=="empty")
        {
            chat_empty= true;
            conv_id = ser_res["conv_id"];
            username = ser_res["myusername"]
            console.log("user_name = >",username);
            room_name = ser_res["room_name"];
            console.log("empty triggered");

        }
        else{
            console.log(ser_res['m']);
            return;

        }


    }


            send_but.addEventListener('click',send_message);
            window.addEventListener('keypress',(e)=>{
            if(e.key =='Enter')
            {
                send_message();
            }
            });

              build(ser_res,chat_empty);



    joining_room();

    console.log("response=>",ser_res);

    user_info.innerText = room_name;


}





function joining_room(){

    socket.connect();

    join_room_d =  {'conv_id':conv_id,'user_soc_id': date.getMilliseconds()};

    socket.emit('join_room',join_room_d);




    // socket.emit('send_message',new_message_d);











}



function time_format(){

    const now = new Date();
    const year = now.getUTCFullYear();
    const month = String(now.getUTCMonth()+1).padStart(2,'0');
    const day = String(now.getUTCDate()).padStart(2,'0');
    const minutes = String(now.getUTCMinutes()).padStart(2,'0');
    const hour = String(now.getUTCHours()).padStart(2,'0');
    const second = String(now.getUTCSeconds()).padStart(2,'0');

    return `${year}-${month}-${day} ${hour}:${minutes}:${second}`;

}



function message_popping(new_message)
{

         message_build(new_message);





}








function message_build(element){




            let message_container = document.createElement("li");
            let message= document.createElement("p");


            let m_info = document.createElement("p");

            m_info.classList.add("m_info");
            message.innerText =element["content"];
            message_container.appendChild(message);



      if(element["username"]== username)
            {


                message.classList.add("my_m");
                message_container.classList.add("my_c");







            }
            else{

                       message.classList.add("recv_me");
            message_container.classList.add("recv_c");








            }
                     m_info.innerText=element["sent_at"];

            message_container.appendChild(m_info);

            messages.appendChild(message_container);
             messages.scrollTop = messages.scrollHeight;

}








function send_message()
{
    messaging_started = true;

    empty_chat_splash(chat_empty,messaging_started);



    if(message_field.value !='')
    {

                    message = message_field.value;
            sent_at = time_format();

            new_message_d  = {'conv_id':conv_id,'username':username,'content':message,'sent_at':sent_at};
            socket.emit('send_message',new_message_d);
             message_field.value = '';
    }


}





function empty_chat_splash(chat_empty ,messaging_started,no_messages){


    if(chat_empty && !messaging_started)
    {
        let m = document.createElement("li");
        m.innerText = no_messages;
        m.style.padding = "2vw";
        m.style.backgroundColor = "grey";
        m.style.fontSize = "2rem";
        messages.style ="     align-items: center;justify-content: center;";
        messages.appendChild(m);
        chat_square.style.background="transparent";
        return;
    }

    else if (chat_empty,messaging_started ){
        messages.remove(messages.lastChild);
        chat_square.style.backgroundImage = 'url("/static/media/imgs/chatBack.jpg")';

    }

}




