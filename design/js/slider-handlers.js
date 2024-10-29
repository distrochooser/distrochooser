document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.weight').forEach(weightContainer => {
        const slider = weightContainer.querySelector('input[type="range"]');
        const minusButton = weightContainer.querySelector('.bi-dash-circle-fill');
        const plusButton = weightContainer.querySelector('.bi-plus-circle-fill');

        minusButton.addEventListener('click', () => {
            if (slider.value > slider.min) {
                slider.value = parseInt(slider.value) - 1;
            }
        });

        plusButton.addEventListener('click', () => {
            if (slider.value < slider.max) {
                slider.value = parseInt(slider.value) + 1;
            }
        });
    });
});
