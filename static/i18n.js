// TODO: Not all elements can be changed, such as meta titles
// TODO: Display the translation proposals

var raw = window.localStorage.getItem("ku-collected-translations")
var collected_translations = JSON.parse(raw)
function init_translation() {
    var i18n_elements = document.querySelectorAll(".ku-i18n")
    i18n_elements.forEach(function (i18n_element) {
        i18n_element.classList.add("ku-i18n-translateable")
        i18n_element.setAttribute("contenteditable", "true")
        var key = i18n_element.getAttribute("data-i18n")

        var localStorageTranslation = collected_translations[key]
        if (localStorageTranslation) {
            i18n_element.textContent = localStorageTranslation
            i18n_element.classList.add("ku-i18n-translateable-fromstorage")
        }
        /* TODO: make collapse elements inactive */
        /* TODO: Inject language code */
        i18n_element.addEventListener("click", click_handler_i18n_value);
        i18n_element.addEventListener("input", function () {
            var new_text = i18n_element.textContent
            collected_translations[key] = new_text
            i18n_element.classList.add("ku-i18n-translateable-done")
            localStorage.setItem("ku-collected-translations", JSON.stringify(collected_translations))

            // Make sure other elements with the same key are updated aswell
            i18n_elements.forEach(other_i18n_element => {
                if (other_i18n_element !== i18n_element) {
                    var other_key = other_i18n_element.getAttribute("data-i18n")
                    if (other_key == key) {
                        other_i18n_element.textContent = new_text
                        other_i18n_element.classList.add("ku-i18n-translateable-done")
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

async function toggleTranslation() {
    var element = document.querySelector(".ku-i18n-controls")
    var i18n_elements = document.querySelectorAll(".ku-i18n")
    var lang_code = document.querySelector("#ku-i18n-lang-code").value
    element.classList.toggle("d-none");
    if (element.classList.contains("d-none")) {
        i18n_elements.forEach(i18n_element => {
            i18n_element.removeAttribute("contenteditable")
            i18n_element.classList.remove("ku-i18n-translateable")
            i18n_element.classList.remove("ku-i18n-translateable-done")
            i18n_element.classList.remove("ku-i18n-translateable-fromstorage")
            i18n_element.removeEventListener("click", click_handler_i18n_value)
        })
        /* save translations */
        // TODO: Language inject
        var url = "/api/i18n/add_suggestion"
        var data = {
            "lang_code": lang_code,
            "dict_values": collected_translations
        }
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const response = await fetch(url, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            body: JSON.stringify(data),
            mode: 'same-origin',
            headers: { 'X-CSRFToken': csrftoken, "Content-Type": "application/json", },
        });
        const body = await response.text()
        console.log(body)
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

if (typeof (turbo) == "undefined") {
    document.addEventListener("turbo:load", attachControls);
} else {
    document.addEventListener("DOMContentLoaded", attachControls);
}