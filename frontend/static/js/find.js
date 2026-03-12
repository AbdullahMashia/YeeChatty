


let users = document.getElementById("users");


window.onload =  find_users();





async function find_users()
{
    let response = await fetch("/api/users/find");
    let users_r = await response.json();
    console.log(typeof(users_r));

    builder(users_r);





    }

// let x = {
//     "users":[
//         {'u': "ali"},
//         {'u':"Ahmed"},
//         {'u':"sale"}
//     ]
// };
function builder(users_arr){
    users_arr.forEach(ele=>{
        let li = document.createElement("li");
        let user = document.createElement("p");
        let send_req = document.createElement("p");

        // filling data
        user.innerText = ele["username"];
        li.classList.add("in_req");
        send_req.innerText="✅";

        send_req.id = ele["id"];
        li.appendChild(user);
        li.appendChild(send_req);


        send_req.addEventListener("click",e=>requset_sender(users_arr,e));


           users.appendChild(li);


    });




}

async function requset_sender(users_arr,e){
        console.log("id=>",e.target.id);
             let request = {
                'user_id':e.target.id,

            };

            let response = await fetch("/api/requests", {
                method: "POST",
                heaers:{
                   "Content-Type": "application/json"
                },
                body: JSON.stringify(request)
            });

            let serv_res = await response.json();

            if(serv_res["stat"] == true)
            {


               users.removeChild(e.target.parentElement);


            }
            else{
                 console.log(serv_res);
            }


}







