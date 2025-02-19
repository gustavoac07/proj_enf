document.addEventListener("DOMContentLoaded", function() {
  // Selecionando o formulário
  const form = document.getElementById("auxiliar-form");

  // Evento de envio do formulário
  form.addEventListener("submit", function(event) {
      event.preventDefault(); // Impede o envio do formulário

      // Captura os dados do formulário
      const leito = document.getElementById("leito").value;
      const glicemias = document.getElementById("glicemias").value;
      const acamados = document.getElementById("acamados").value;
      const auxilios = document.getElementById("auxilios").value;
      const banhos = document.getElementById("banhos").value;
      const tempoBanho = document.getElementById("tempoBanho").value;
      const horarioBanho = document.getElementById("horarioBanho").value;

      // Envia os dados para o backend (API Flask)
      fetch('http://127.0.0.1:5000/enviar_aux', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              leito,
              glicemias,
              acamados,
              auxilios,
              banhos,
              tempoBanho,
              horarioBanho
          })
      })
      .then(response => response.json())
      .then(data => {
          console.log('Resposta do servidor:', data);
          alert(data.message);  // Exibe a mensagem de sucesso ou erro retornada pelo servidor

          // Limpa o formulário após o envio
          form.reset();
      })
      .catch(error => {
          console.error('Erro:', error);
          alert('Ocorreu um erro ao enviar os dados.');
      });
  });
});
