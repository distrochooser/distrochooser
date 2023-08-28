// TODO: Not all elements can be changed, such as meta titles
// TODO: Display the translation proposals
// TODO: Save the proposal *somewhere* 

var collected_translations = {}
function init_translation() {
    var i18n_elements = document.querySelectorAll(".ku-i18n")
    i18n_elements.forEach(function(i18n_element){
        i18n_element.setAttribute("contenteditable", "true")
        var key = i18n_element.getAttribute("data-i18n")
        i18n_element.addEventListener("click", click_handler_i18n_value);
        i18n_element.addEventListener("input", function () {
            var new_text = i18n_element.textContent
            collected_translations[key] = new_text

            // Make sure other elements with the same key are updated aswell
            i18n_elements.forEach(other_i18n_element => {
                if (other_i18n_element !== i18n_element) {
                    var other_key = other_i18n_element.getAttribute("data-i18n")
                    if (other_key == key) {
                        other_i18n_element.textContent = new_text
                    }
                }
            })
        }, false);
    })
}

function click_handler_i18n_value(e) {
    e.stopPropagation();
    e.preventDefault();
}

function toggleTranslation() {
    var element = document.querySelector(".ku-i18n-controls")
    var i18n_elements = document.querySelectorAll(".ku-i18n")
    element.classList.toggle("d-none");
    if (element.classList.contains("d-none")) {
        i18n_elements.forEach(i18n_element => {
            i18n_element.removeAttribute("contenteditable")
            i18n_element.removeEventListener("click", click_handler_i18n_value)
        })
    } else {
        init_translation();
    }
}

function attachControls(e) {
    document.querySelector(".ku-18n-show").addEventListener("click", function (e) {
        e.preventDefault();
        toggleTranslation();
    })

    document.querySelector(".ku-i18n-save").addEventListener("click", function (e) {
        e.preventDefault();
        toggleTranslation();
    })
}

if (typeof(turbo) == "undefined"){
    document.addEventListener("turbo:load", attachControls);
} else {
    document.addEventListener("DOMContentLoaded", attachControls);
}