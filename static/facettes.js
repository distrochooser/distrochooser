document.querySelectorAll("input[data-ku-facette]").forEach(el => {
    checkedStateHandler(el)
    el.addEventListener("change", (e) => checkedStateHandler(e.target))
})

function checkedStateHandler(el) {
    /* Get rid of the weight container if the facette is not selected */
    const isRadio = document.querySelectorAll("input[value='nothing']").length === 1;
    var checked  = false;
    var data_id = false;
    if (isRadio) {
        checked = document.querySelectorAll("input[data-ku-facette]:not([value='nothing']):checked").length > 0
        const selection = document.querySelector("input[data-ku-facette]")
        data_id = selection ? selection.getAttribute("data-ku-facette") : null;
    } else {
        data_id = el.getAttribute("data-ku-id")
        checked = el.checked;
    }

    console.debug("The page is in radio select mode: " + isRadio + ". The data id is: " + data_id + "the checked state is: " + checked)

    var weightContainer = document.querySelector("#"+data_id+"-weight-container")
    
    if (checked) {
        weightContainer.classList.remove("d-none");
    } else {
        weightContainer.classList.add("d-none");
    }
}