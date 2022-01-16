const bookingApiUrl=`${window.origin}/api/booking`;

function getBookingList(url=bookingApiUrl){
    let p=fetch(url).then(response=>{
        if(response.status===403){
            location.href="/";
        }else if(response.status===200){
            return response.json()                        
        }else{
            console.log(response.json());
        }
    })
    return p
}

function delBooking(dataObj, url=bookingApiUrl){
    let p=fetch(url, {
        method:"delete",
        credentials: "include", 
        headers:{
            "Accept": "application/json", 
            "Content-Type":"application/json"
        },
        body:JSON.stringify(dataObj)
    }).then(response=>{
        if(response.status===403){
            location.href="/";
        }else if(response.status==200){
            return response.json();
        }else{
            console.log(response.json());
        }
    })
    return p
}

function createOrder(dataObj){
    const url=`${window.origin}/api/orders`;
    let p=fetch(url, {
        method:"post", 
        credentials: "include", 
        headers:{
            "Accept": "application/json", 
            "Content-Type":"application/json"
        },
        body:JSON.stringify(dataObj)
    }).then(response=>{
        if(response.status===403){
            location.href="/";
        }else if(response.status===500){
            console.log(response.json());
        }else{
            return response.json()
        }
    })
    return p
}