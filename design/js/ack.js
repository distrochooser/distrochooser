function ack(result_id) {
    var url = "/api/ack/" + result_id
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url, {
        mode: 'same-origin',
        headers: { 'X-CSRFToken': csrftoken, "Content-Type": "application/json", },
    });
}

window.ack = ack