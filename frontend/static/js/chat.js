


let chats = document.getElementById("chats");



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
        return;
    }


       all_chats.forEach(element => {
            //request componenets
            let req = document.createElement("li");
            let user = document.createElement("p");

            req.appendChild(user);
            user.innerText = element["username"];

           req.addEventListener("click",()=>location.replace("/conversation"));








            chats.appendChild(req);



        });


}


