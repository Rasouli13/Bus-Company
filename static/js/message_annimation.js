document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.popup-message');
    
    messages.forEach(msg => {
        setTimeout(() => {
            msg.classList.add('show');
        }, 100);

        setTimeout(() => {
            msg.classList.remove('show');
        }, 5100);

        setTimeout(() => {
            msg.remove();
        }, 5600);
    });
});
