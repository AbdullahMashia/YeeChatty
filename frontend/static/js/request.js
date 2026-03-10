

let requests = document.getElementById("requests");
let request_square = document.getElementById("request_square");

let in_users = ["ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed"
];

let i_r = document.getElementById("in");
let o_r = document.getElementById("out");

let m  = Math.random() * 15;
let x = Math.random() * 10;


for( let a =1; a<4; a++)
{
 let req = document.createElement("li");
        let accept_request = document.createElement("h3");
        let refuse_request = document.createElement("h3");
         let user = document.createElement("p");
        accept_request.innerText="✅";
        refuse_request.innerText ="❌";
         if(a%2==0)
         {
        let ls = document.createElement("ul");
        ls.id="check";
        ls.appendChild(accept_request);
        ls.appendChild(refuse_request);


        req.appendChild(user);
        req.appendChild(ls);

        user.innerText = in_users[a];


        req.classList.add("in_req")
        requests.appendChild(req);

         }



    else{


        user.innerText = in_users[a];
        req.appendChild(user);
        req.appendChild(refuse_request);
        req.classList.add("o_req");
        requests.appendChild(req);

    }


}



request_square.scrollTop =0;


o_r.addEventListener("click",()=>{
    hide_first_page();

});






