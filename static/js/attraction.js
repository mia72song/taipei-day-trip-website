// 向後端請求attraction的api
function getAttractionById(){
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

// 向後端預定新的行程
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
        if(response.status!==500){
            return response.json()
        }else{
            console.log(response.json())
        }
    })
    return p
}