let nextPage=0;
let keyword;
let ajaxRequested=false;  // 監測是否正在發出ajax請求

// 製作景點資訊卡
function createItemNode(data){
    const item=document.createElement("div");
    item.className="item";

    const img=document.createElement("img");
    img.src=data["images"][0];
    item.appendChild(img);
    
    const content=document.createElement("div");
    content.className="content";    

    const spot_name=document.createElement("h4");
    spot_name.id="spot_name";
    spot_name.textContent=data["name"];
    content.appendChild(spot_name);
    const mrt=document.createElement("span");
    mrt.id="mrt";
    mrt.textContent=data["mrt"];
    content.appendChild(mrt);
    const category=document.createElement("span");
    category.id="category";
    category.textContent=data["category"]
    content.appendChild(category);
    
    item.appendChild(content);
    return item
}

// 根據頁數向後端請求api
function getDataByPage(page=0){
    if(!ajaxRequested){  // 監測是否正在發出ajax請求，避免重覆發送
        const url=`${window.origin}/api/attractions?page=${page}`;
        ajaxRequested=true;
        fetch(url).then(response=>{
            if(response.status===200){
                return response.json()
            }else{
                console.log(response.json())
            }            
        }).then(resp_data=>{
            const data=resp_data["data"];
            // console.log(data[0]);
            if(page===0){
                const databox=document.createElement("div");
                databox.className="box";
                const main=document.querySelector("main");
                main.appendChild(databox);
            }            
            for(let d of data){                
                const item=createItemNode(d);
                document.querySelector(".box").appendChild(item);
            }            
            nextPage=resp_data["nextPage"];
            ajaxRequested=false;
        }).catch(error=>{
            console.log(error);
        })
    }else{
        console.log("ajax請求正在發送中……請耐心等候")
    }
}

// 根據關鍵字向後端請求api
function getDataByKeyword(keyword, page=0){
    if(!ajaxRequested){
        const url=`${window.origin}/api/attractions?keyword=${keyword}&page=${page}`;
        fetch(url).then(response=>{
            if(response.status===200){
                return response.json()
            }else{
                console.log(response.json())
            }
        }).then(resp_data=>{
            const data=resp_data["data"];
            // console.log(data);   
            if(page===0){
                const databox=document.createElement("div");
                databox.className="box";
                const main=document.querySelector("main");
                main.appendChild(databox);
            }
            if(data.length>0){
                for(let d of data){                
                    const item=createItemNode(d);
                    document.querySelector(".box").appendChild(item);
                }
            }else{
                const result_div=document.querySelector(".box");
                result_div.textContent="查無資料";
                result_div.style.height="300px";
            }                       
            nextPage=resp_data["nextPage"];
            ajaxRequested=false;
        }).catch(error=>{
            console.log(error);
        })
    }else{
        console.log("ajax請求正在發送中……請耐心等候")
    }
}

// 展示首頁的景點資訊
addEventListener("load", ()=>{
    getDataByPage();
})

// 捲軸滾到視窗最下方時，自動載入下一頁的景點資訊
addEventListener("scroll", ()=>{
    if(nextPage){
        const scrollY=window.scrollY; // 文檔在垂直方向已滚动的像素值
        const innerHeight=window.innerHeight; // 螢幕視窗「包括捲軸」的高度
        /* const scrollHeight=document.documentElement.scrollHeight; 文檔的完整高度（包含捲軸之外部分）
        scrollHeight會有瀏覽器相容性的問題 */  
        let scrollHeight=Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );
        if(scrollY+innerHeight>=scrollHeight-100){
            // console.log("Touch the Bottom!!");
            if(keyword){
                getDataByKeyword(keyword, nextPage);
            }else{
                getDataByPage(nextPage);
            }
        }
    }
})

// 輸入關鍵字搜尋功能
function search(obj){ 
    keyword=obj.keyword.value;
    if(keyword){        
        // 初始化景點列表及nextPage
        const databox=document.querySelector(".box");
        document.querySelector("main").removeChild(databox);
        nextPage=0;
        
        getDataByKeyword(keyword);
        return false;
    }    
    return false;
}