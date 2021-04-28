let nextPage=0;
let ajaxRequested=false;  // 監測是否正在發出ajax請求
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
            const databox=document.querySelector(".box");
            for(let d of data){                
                const item=createItemNode(d);
                databox.appendChild(item);
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

function getDataByKeyword(keyword, page=0){

}
addEventListener("load", ()=>{
    getDataByPage();
})
addEventListener("scroll", ()=>{
    if(nextPage){
        const scrollY=window.scrollY // 文檔在垂直方向已滚动的像素值
        const innerHeight=window.innerHeight; // 螢幕視窗「包括捲軸」的高度
        /* const scrollHeight=document.documentElement.scrollHeight;
        文檔的完整高度（包含捲軸之外部分）**會有瀏覽器相容性的問題 */  
        let scrollHeight=Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );
        if(scrollY+innerHeight>=scrollHeight-100){
            console.log("To the Bottom!!");
            getDataByPage(nextPage);
        }
    }else{
        const main=document.querySelector("main");
        const end=document.createElement("h3");
        end.textContent="-- End --";
        end.setAttribute("style", "text-align:center;");
        main.appendChild(end);
    }
})