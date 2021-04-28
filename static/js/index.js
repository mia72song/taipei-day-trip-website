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
    const url=`${window.origin}/api/attractions`;
    const databox=document.querySelector(".box");
    fetch(url).then(
        response=>response.json()
    ).then(resp_data=>{
        const data=resp_data["data"];
        // console.log(data[0]);
        for(let d of data){
            const item=createItemNode(d);
            databox.appendChild(item);
        }
    }).catch(error=>{
        console.log(error);
    })
}

function getDataByKeyword(keyword, page=0){

}
addEventListener("load", ()=>{
    getDataByPage();
})