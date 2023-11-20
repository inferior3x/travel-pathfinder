const departurePlaceSelector = document.querySelector("#departure-place");
const travelPlaceSelector = document.querySelector("#destination");
// const travelInfoFormSelector = document.querySelector("#travel-info-form");
// const travelPlanButtonSelector = document.querySelector("#travel-info-btn");

//여행지 목록 가져오고 드롭다운에 추가
window.addEventListener('DOMContentLoaded', async()=>{
        showSpinner();
        await fetchByGet("/departure-place",
            (responseData) => {
                for (const departure of responseData){
                    departurePlaceSelector.innerHTML += "<option>" + departure["name"] + "</option>";
                }
            },
            () => {},
        );
        await fetchByGet("/travel-place",
            (responseData) => {
                for (const destination of responseData){
                    travelPlaceSelector.innerHTML += "<option>" + destination["name"] + "</option>";
                }
            },
            () => {},
        );
        hideSpinner();
    }
)

// travelPlanButtonSelector.addEventListener('click', async function(event) {
//     showSpinner();
//     await fetchByPost("/travel-plan",
//         convertFormDataToJson(travelInfoFormSelector),
//         (responseData) => {
//             console.log(responseData);
//             window.location.href = "/travel-plan";
//             console.log(responseData);
//         },
//         () => {},
//     );
//
//     hideSpinner();
// });