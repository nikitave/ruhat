chrome.tabs.onUpdated.addListener((tabId,changeInfo,tabInfo)=>{ 
    if (tabInfo.url && tabInfo.url.includes("daber.space/workspace")){
        chrome.tabs.sendMessage(tabId,{
            type: "NEW",
        });
    }
});
