// 向後端請求attraction的api
function getDataById(){
    let p;
    let attraction_id=parseInt(window.location.pathname.split("/")[2]);
    if(attraction_id>0){
        const url=`${window.origin}/api/attraction/${attraction_id}`;
        p =fetch(url).then(response=>{
            if(response.status===200){
                return response.json()
            }else{
                console.log(response.json())
            }
        })
    }
    return p
}

function createBooking(data){
    const url=`${window.origin}/api/booking`;
    let p=fetch(url, {
        method:"post", 
        credentials:"include",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    }).then(response=>{
        if(response.status===403){
            alert("請先登入會員");
        }
        if(response.status!==500){
            return response.json()
        }else{
            console.log(response.json())
        }
    }).catch(error=>{
        console.log(error)
    });
    return p
}