document.getElementById('tecnico-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Captura o número do leito
    const leito = document.getElementById('leito').value;

    // Captura as vias de medicação e suas quantidades
    const via = Array.from(document.querySelectorAll('input[name="via[]"]:checked')).map(el => {
        const quantityInput = document.getElementById(`${el.id}_qty`);
        const quantity = quantityInput ? quantityInput.value : 0;  // Se o campo de quantidade estiver vazio, define como 0
        return `${el.value} (Quantidade: ${quantity})`;
    });

    // Captura os outros campos do formulário
    const insulina = document.getElementById('insulina').value;
    const manha = document.getElementById('manha').value;
    const peso = document.getElementById('peso').value;
    const solicitante = document.getElementById('solicitante').value;

    // Enviar os dados para o backend (API Flask)
    fetch('http://127.0.0.1:5000/enviar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            leito,
            via,
            insulina,
            manha,
            peso,
            solicitante
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
        alert(data.message);  // Exibe a mensagem de sucesso ou erro retornada pelo servidor

        // Limpa o formulário após o envio
        document.getElementById('tecnico-form').reset();

        // Remove as quantidades de medicação associadas aos checkboxes
        document.querySelectorAll('input[name="via[]"]:checked').forEach(el => {
            const quantityInput = document.getElementById(`${el.id}_qty`);
            if (quantityInput) {
                quantityInput.style.display = 'none';  // Esconde o campo de quantidade
                quantityInput.value = '';  // Limpa o campo de quantidade
            }
            el.checked = false;  // Desmarca o checkbox
        });
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao enviar os dados.');
    });
});
