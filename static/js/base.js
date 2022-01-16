const url=`${window.origin}/api/user`;

function requestUserData(method, data=null){
    let body;
    if(data){
        body=JSON.stringify(data)
    };
    let p=fetch(url, {
        method,
        headers:{
            "Accept": "application/json", 
            "Content-Type":"application/json", 
            "Access-Control-Origin": "*"
        },
        body
    }).then(response=>{
        if(response.status!==500){
            return response.json()
        }else{
            console.log(response.json())
        }
    })
    return p
}