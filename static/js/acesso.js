function autenticarCredencias() {
    var username = $('#email').val();
    var password = $('#psw').val();

    // Envia os dados para o servidor
    $.ajax({
        type: 'POST',
        url: '/autenticacao',  // Rota no backend para lidar com a autenticação
        data: JSON.stringify({ username: username, password: password }),
        contentType: 'application/json;charset=UTF-8',
        success: function (response) {
            // Redireciona para index.html se a autenticação for bem-sucedida
            if (response.success) {
                Swal.fire({
                    icon: "sucess",
                    title: "Ótimo!",
                    text: "Usuário autenticado com sucesso!"
                });
                setTimeout(function () {
                    window.location.href = '/';
                }, 2000);
            } else {
                Swal.fire({
                    icon: "error",
                    title: "Oops...",
                    text: "Autenticação inválida ou não encontrada...",
                });


            }
        },
        error: function () {
            alert('Erro ao processar a requisição.');
        }
    });
}