window.addEventListener('DOMContentLoaded', async()=>{
    showSpinner();
    await fetchByPost("/travel-plan",
        convertQueryStringToJson(),
        (responseData) => {
            console.log(responseData);
        },
        () => {},
    );

    hideSpinner();
});