/*
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
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