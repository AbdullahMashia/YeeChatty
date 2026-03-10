let users_l = ["ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed",
    "ali", "abdullah", "Saleh", "mohammed","ahmed"
];

let users = document.getElementById("users");


for(let i=0; i<20; i++)
{
    let field = document.createElement("li");
    let user = document.createElement("p");
    let send_req = document.createElement("p");

    field.classList.add("in_req");

    user.innerText=users_l[i];
    send_req.innerText="✅";

    field.appendChild(user);
    field.appendChild(send_req);

    users.appendChild(field);
}


