document.querySelectorAll("input[data-ku-facette]").forEach(el => {
    checkedStateHandler(el)
    el.addEventListener("change", (e) => checkedStateHandler(e.target))
})

function checkedStateHandler(el) {
    /* Get rid of the weight container if the facette is not selected */
    var data_id = el.getAttribute("data-ku-id")
    var checked = el.checked;

    var weightContainer = document.querySelector("#"+data_id+"-weight-container")
    
    if (checked) {
        weightContainer.classList.remove("d-none");
    } else {
        weightContainer.classList.add("d-none");
    }
}