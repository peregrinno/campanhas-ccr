// Função para carregar e popular a tabela via AJAX
function carregarPessoas() {
    $.ajax({
        url: '/pessoas?page=${page}',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            // Limpar a tabela antes de popular com os novos dados
            $('#tabela-pessoas tbody').empty();

            // Verificar se a resposta contém o array 'pessoas'
            if ('pessoas' in data && Array.isArray(data.pessoas)) {
                // Popula a tabela com os dados recebidos
                data.pessoas.forEach(function (pessoa) {
                    $('#tabela-pessoas tbody').append(`
            <tr>
              <td>${pessoa.nome}</td>
              <td>${pessoa.telefone}</td>
              <td>${pessoa.cidade}</td>
              <td><button class="uk-icon-link uk-margin-small-right" uk-icon="file-edit"></button></td>
            </tr>
          `);
                });
            } else {
                console.warn('Array de pessoas está vazio ou ausente na resposta.');
            }
        },
        error: function (error) {
            console.error('Erro ao obter pessoas via AJAX:', error);
        }
    });
}

// Função para atualizar a estrutura da paginação UIkit
function atualizarPaginacao(paginacao) {
    // Limpa a paginação antes de atualizar
    $('#pagina-pessoas').empty();

    // Adiciona o botão de página anterior
    if (paginacao.has_prev) {
        $('#pagina-pessoas').append(`
        <li><a href="#" onclick="carregarPessoas(${paginacao.prev_page})"><span uk-pagination-previous></span></a></li>
      `);
    } else {
        $('#pagina-pessoas').append('<li class="uk-disabled"><span uk-pagination-previous></span></li>');
    }

    // Adiciona os botões de páginas
    paginacao.pages.forEach(function (page) {
        if (page === '...') {
            $('#pagina-pessoas').append('<li class="uk-disabled"><span>…</span></li>');
        } else if (page === paginacao.current_page) {
            $('#pagina-pessoas').append(`<li class="uk-active"><span>${page}</span></li>`);
        } else {
            $('#pagina-pessoas').append(`<li><a href="#" onclick="carregarPessoas(${page})">${page}</a></li>`);
        }
    });

    // Adiciona o botão de próxima página
    if (paginacao.has_next) {
        $('#pagina-pessoas').append(`
        <li><a href="#" onclick="carregarPessoas(${paginacao.next_page})"><span uk-pagination-next></span></a></li>
      `);
    } else {
        $('#pagina-pessoas').append('<li class="uk-disabled"><span uk-pagination-next></span></li>');
    }
}

function NovaPessoa() {
    // Obtenha os valores do formulário
    var nome = $('#input-nome').val();
    var telefone = $('#input-telefone').val();
    var cidade = $('#input-cidade').val();
    var estado = $('#slct-estado').val();
    var pais = $('#slct-pais').val();

    // Crie um objeto com os dados do formulário
    var formData = {
        nome: nome,
        telefone: telefone,
        cidade: cidade,
        estado: estado,
        pais: pais
    };

    // Faça a requisição AJAX
    $.ajax({
        type: 'POST',
        url: '/add_pessoa',
        data: JSON.stringify(formData),  // Converte os dados para JSON
        contentType: 'application/json;charset=UTF-8',  // Define o cabeçalho Content-Type
        success: function (response) {
            // Exibe um SweetAlert de sucesso se a requisição for bem-sucedida
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Pessoa adicionada com sucesso.'
            });

            //Recarrega pessoas
            carregarPessoas();
        },
        error: function (error) {
            // Exibe um SweetAlert de erro se a requisição falhar
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'Ocorreu um erro ao adicionar a pessoa. Tente novamente mais tarde.'
            });
        }
    });
}

// Chama a função ao carregar a página
$(document).ready(function () {
    carregarPessoas();
});

