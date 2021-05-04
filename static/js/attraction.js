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