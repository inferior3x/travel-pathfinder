function convertFormDataToJson(formElement){
    const jsonData = {};
    new FormData(formElement).forEach((value, key) => {
        jsonData[key] = value;
    })
    return jsonData;
}