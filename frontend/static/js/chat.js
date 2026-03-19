


let chats = document.getElementById("chats");
let intro_m = document.createElement("li");
let user_name = document.getElementById("user_name");


window.addEventListener("load", chat_loader);









async function  chat_loader(){

    let response = await fetch("/api/chats");

    let ser_res = await response.json();

    builder(ser_res);


    console.log(ser_res);
}




function builder(all_chats){

    console.log("requests =",all_chats);
    let ele = document.querySelectorAll("#requests li");


    // cleaning page first




    if(!Array.isArray(all_chats))
    {

        intro_m.innerText = all_chats["m"];
        // styling empty chats message


        intro_m.style.backgroundColor = "grey";
        intro_m.style.fontSize = "2rem";
        intro_m.style.width="fit-content";
        intro_m.style.padding = "3vw";
        chats.style = "display:flex;align-items:center; justify-content:center";
        chats.appendChild(intro_m);
        return;
    }


       all_chats.forEach(element => {
            //chat componenets
            let req = document.createElement("li");
            let user = document.createElement("p");

            req.appendChild(user);
            user.innerText = element["username"];
            let ccc_id = element["conversations_id"];
            console.log("conv_id =",ccc_id);


           req.addEventListener("click",async function open_room(){

                let res = await fetch("/room",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                    },

                    body:JSON.stringify({"type":"open_room","conv_id":element["conversations_id"]})
                });


                location.replace("/room");

            });








            chats.appendChild(req);



        });


}




