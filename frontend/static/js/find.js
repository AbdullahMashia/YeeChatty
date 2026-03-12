


let users = document.getElementById("users");
let p_mate = document.getElementById("online");


window.onload =  find_users();


let single_request_sent_id = 0;


let aaa = [2,4,1,5];

async function find_users()
{
    let response = await fetch("/api/users/find");
    let users_r = await response.json();
     p_mate.addEventListener("click",()=>{
        console.log("clicked");
        find_users() ;
 } );



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

    let children = users.childElementCount;
    let elements = users.querySelectorAll("li");


//clearning for search result
    if(children > 0)
    {
            users.removeChild(users.firstChild);
            elements.forEach(e=>{
                    e.remove();
             })
    }




    if( !Array.isArray(users_arr))
    {


        if (users_arr["success"])
            users_arr = [users_arr];
        else{
            let err_m = document.createElement("div");
            err_m.style.padding= "3vw";

            err_m.style.backgroundColor = "grey";
            err_m.style.border = "0.3vw solid red";
            err_m.style.borderRadius= "1vw ";
            err_m.style.fontSize = "2rem";

            err_m.style.top = "-50%";

            err_m.innerText = users_arr["m"];
            users.appendChild(err_m);
            return;
        }
    }
    if(single_request_sent_id !=0)
    console.log("single ===>",single_request_sent_id);
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
                'rec_id':e.target.id,

            };

            let response = await fetch("/api/requests", {
                method: "POST",
                heaers:{
                   "Content-Type": "application/json",

                },
                body: JSON.stringify(request)
            });

            let serv_res = await response.json();

            if(serv_res["success"] == true)
            {

                console.log(e.target.parentElement);

               users.removeChild(e.target.parentElement);
               single_request_sent_id = e.target.id;



            }
            else{
                 console.log(serv_res);
            }


}



async function find_user()
{

    let username = document.getElementById("username").value;

    console.log(username);


    let res = await fetch("/api/users/find",{
        method:"POST",
        headers:{
            "Content-Type": "application/json",

        },
        body: JSON.stringify({ "username":username})
    });
    let ser_res = await res.json();
    console.log(ser_res);


    builder(ser_res);
}



