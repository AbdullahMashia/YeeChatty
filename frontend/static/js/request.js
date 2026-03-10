
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






    for(let i=0; i<15;i++)
    {
        let req = document.createElement("li");
        let accept_request = document.createElement("h3");
        let refuse_request = document.createElement("h3");
        let ls = document.createElement("ul");
        ls.id="check";
        ls.appendChild(accept_request);
        ls.appendChild(refuse_request);
        let user = document.createElement("p");

        req.appendChild(user);
        req.appendChild(ls);

        user.innerText = in_users[i];
        accept_request.innerText="✅";
        refuse_request.innerText ="❌";

        req.classList.add("in_req")
        requests.appendChild(req);
    }


request_square.scrollTop =0;


o_r.addEventListener("click",()=>{
    hide_first_page();

});






