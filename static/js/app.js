document.addEventListener('DOMContentLoaded', function () {
    // Üye Listeleme
    fetch('/members')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#member-table tbody');
            tableBody.innerHTML = '';
            data.forEach(member => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${member[1]}</td>
                    <td>${member[2]}</td>
                    <td>${member[3]}</td>
                `;
                tableBody.appendChild(row);
            });
        });

    // Üye Ekleme
    const form = document.querySelector('#add-member-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const name = document.querySelector('#name').value;
        const email = document.querySelector('#email').value;
        const position = document.querySelector('#position').value;

        fetch('/members', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, position })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        });
    });
});
