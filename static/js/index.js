let url;
let p;
let ajaxRequested=false;// 監測是否正在發出ajax請求
function getDataByPage(page){
    if(!ajaxRequested){
        ajaxRequested=true;
        url=`${window.origin}/api/attractions?page=${page}`;
        let p=fetch(url).then(response=>{
            ajaxRequested=false;
            if(response.status===200){
                return response.json()
            }else{
                console.log(response.json())
            }
        })
        return p
    }else{
        console.log("ajax請求已發送，請耐心等待…")
    }
}

function getDataByKeyword(keyword, page){
    if(!ajaxRequested){
        ajaxRequested=true;
        url=`${window.origin}/api/attractions?keyword=${keyword}&page=${page}`;
        let p=fetch(url).then(response=>{
            ajaxRequested=false;
            if(response.status===200){
                return response.json()
            }else{
                console.log(response.json())
            }
        })
        return p
    }else{
        console.log("ajax請求已發送，請耐心等待…")
    }
}