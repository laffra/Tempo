var last_email = "";
var last_url = "";

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  console.log("updated " + JSON.stringify(changeInfo));
  chrome.identity.getProfileUserInfo(function (userInfo) {
    updateTab(userInfo.email, tab);
  });
});

chrome.tabs.onActivated.addListener(function(activeInfo) {
  console.log("activated " + JSON.stringify(activeInfo));
  chrome.tabs.get(activeInfo.tabId, function (tab) {
    chrome.identity.getProfileUserInfo(function(userInfo) {
      updateTab(userInfo.email, tab);
     });
  });
});

function updateTab(email, tab) {
  if (last_email === email && last_url === tab.url) {
    return
  }
  last_email = email;
  last_url = tab.url;
  var port_number = 1187;
  while (port_number < 1287) {
    try {
      var url = "http://localhost:" + port_number + "/tempo?" +
        "url=" + encodeURIComponent(tab.url) + "&" +
        "fav=" + encodeURIComponent(tab.favIconUrl || "") + "&" +
        "email=" + encodeURIComponent(email) + "&" +
        "title=" + encodeURIComponent(tab.title);
      var xhr = new XMLHttpRequest();
      xhr.open('GET', url);
      xhr.send();
      break;
    } catch (e) {
      console.log(e);
    }
    port_number++;
      break;
  }
}