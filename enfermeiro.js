document.getElementById('enfermeiro-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Obtém os dados dos campos do formulário
    const leito = document.getElementById('leito').value;
    const gerenciado = document.querySelector('select[name="gerenciado"]').value;
    const curativos = document.querySelector('select[name="curativos"]').value;
    const risco = document.querySelector('select[name="risco"]').value;
    const reconciliacao = document.querySelector('select[name="reconciliacao"]').value;
    const reabilitacao = document.querySelector('select[name="reabilitacao"]').value;

    // Exibe os dados no console
    console.table({
        'Número do Leito': leito,
        'Paciente Gerenciado': gerenciado,
        'Necessita de Curativos': curativos,
        'Risco de Queda': risco,
        'Reconciliação de Medicação': reconciliacao,
        'Reabilitação/Diálise': reabilitacao
    });

    // Envia os dados para o backend (API Flask)
    fetch('http://127.0.0.1:5000/enviar_enf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            leito,
            gerenciado,
            curativos,
            risco,
            reconciliacao,
            reabilitacao
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
        alert(data.message);  // Exibe a mensagem de sucesso ou erro

        // Limpa o formulário após o envio
        document.getElementById('enfermeiro-form').reset();

        // Se houver campos que precisam ser restaurados para um valor inicial específico (se necessário),
        // você pode definir um valor padrão para os campos após reset.
        // Por exemplo, para um campo de "select", caso precise garantir que ele vá para o primeiro valor,
        // pode ser feito assim:
        document.querySelector('select[name="gerenciado"]').selectedIndex = 0;
        document.querySelector('select[name="curativos"]').selectedIndex = 0;
        document.querySelector('select[name="risco"]').selectedIndex = 0;
        document.querySelector('select[name="reconciliacao"]').selectedIndex = 0;
        document.querySelector('select[name="reabilitacao"]').selectedIndex = 0;
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao enviar os dados.');
    });
});
