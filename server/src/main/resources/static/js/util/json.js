function convertFormDataToJson(formElement){
    const jsonData = {};
    new FormData(formElement).forEach((value, key) => {
        jsonData[key] = value;
    })
    return jsonData;
}

function convertQueryStringToJson(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const jsonData = {};
    for (const [key, value] of urlParams.entries()) {
        jsonData[key] = value;
    }
    return jsonData;
}