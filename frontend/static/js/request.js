

let requests = document.getElementById("requests");
let request_square = document.getElementById("request_square");


let i_r = document.getElementById("in");
let o_r = document.getElementById("out");


// intro message if not requests
let intro_m = document.createElement("li");

            intro_m.style.background="grey";
           intro_m.style.backgroundColor = "grey";
            intro_m.style.border = "0.3vw solid red";
            intro_m.style.borderRadius= "1vw ";
            intro_m.style.fontSize = "2rem";
            intro_m.style.maxWidth="clamp(40vw,60vw,70vw)";
            intro_m.style.textAlign = "center";

            intro_m.style.padding = "2vw";
            intro_m.style.top = "-50%";




window.addEventListener("load", loading_req());





async function loading_req(){
    let res = await fetch("/api/requests");
    let ser_res = await res.json();




    builder(ser_res);


}











function builder(all_req){

    console.log("requests =",all_req);
    let ele = document.querySelectorAll("#requests li");


    // cleaning page first

    ele.forEach(e=>{
        e.remove();
    });



    if(!Array.isArray(all_req))
    {
        requests.appendChild(intro_m);
        intro_m.innerText = all_req["m"];
        return;
    }


       all_req.forEach(element => {
            //request componenets
            let req = document.createElement("li");
            let user = document.createElement("p");
            let cancel_req = document.createElement("h3");
            let refuse_request = document.createElement("h3");
            req.appendChild(user);
            req.id = element["id"];
             req.id = element["request_id"];
            //check if request is incoming
            if (element["type"]=="incoming"){

                let accept_request = document.createElement("h3");
                let ls = document.createElement("ul");
                accept_request.innerText="✅";

                refuse_request.innerText ="❌";

                //event handlers

                accept_request.addEventListener("click",e=>accept_request_f(e));
                refuse_request.addEventListener("click",e=>deny_request(e));

                ls.id="check";
                ls.appendChild(refuse_request);
                ls.appendChild(accept_request);
                req.appendChild(ls);
                 req.classList.add("in_req")
            }
            else{
                req.classList.add("o_req");

                cancel_req.addEventListener("click",e=>cancel_request(e));
                req.appendChild(cancel_req);
                cancel_req.innerText="❌";
            }




            user.innerText =element["username"];

            requests.appendChild(req);



        });


}




async function accept_request_f(e){

    let res = await fetch("/api/request/handler", {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({"type":"accept","request_id":e.target.parentElement.parentElement.id})
    });
    let ser_res = await res.json();

    loading_req();

    console.log("accept_response = ", ser_res);


}

async function deny_request(e){
    let res = await fetch("/api/request/handler", {
        method:"POST",
        headers:{
            "Content-type":"application/json"
        },
        body: JSON.stringify({"type":"deny","request_id":e.target.parentElement.parentElement.id})
    })

    let ser_res = await res.json();
     loading_req();
    console.log("dey_response= ",ser_res);

}

async function cancel_request(e){
    let res = await fetch("/api/request/handler", {
        method:  "POSt",
        headers:{
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"type":"cancel","request_id":e.target.parentElement.id})
    });
    let ser_res = await res.json();
     loading_req();
    console.log("cancel_response=",ser_res);
}




















