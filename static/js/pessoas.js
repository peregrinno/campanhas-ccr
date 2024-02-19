var pessoaID;
var page;

// Função para carregar e popular a tabela via AJAX
function carregarPessoas(page) {
    $.ajax({
        url: '/pessoas?page='+ page,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            //console.log(data);
            // Limpar a tabela antes de popular com os novos dados
            $('#tabela-pessoas tbody').empty();

            // Verificar se a resposta contém o array 'pessoas'
            if ('pessoas' in data && Array.isArray(data.pessoas)) {
                // Popula a tabela com os dados recebidos
                data.pessoas.forEach(function (pessoa) {
                    $('#tabela-pessoas tbody').append(`
            <tr data-aos="fade-right">
              <td>${pessoa.id}</td>
              <td>${pessoa.nome}</td>
              <td><a href="https://api.whatsapp.com/send?phone=55${pessoa.telefone}&text=Olá, ${pessoa.nome}! Tudo bem?" target=_blank uk-icon="icon: whatsapp"></a> ${pessoa.telefone}</td>
              <td>${pessoa.cidade}</td>
              <td><button class="uk-icon-link uk-margin-small-right" uk-icon="file-edit" onclick="detalhePessoa(${pessoa.id})"></button></td>
            </tr>
          `);
                });
            } else {
                console.warn('Array de pessoas está vazio ou ausente na resposta.');
            }
            atualizarPaginacao(data.paginacao);
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
        url: '/pessoas/add_pessoa',
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
            carregarPessoas(1);
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

function detalhePessoa(id) {
    // Faça a requisição AJAX para obter os detalhes da pessoa
    $.ajax({
      type: 'GET',
      url: '/pessoas/pessoa/' + id, 
      dataType: 'json',
      success: function (data) {
        pessoaID = id;
        //console.log(data);
        // Preencha os campos do modal com os dados recebidos
        $('#input-nome-detalhes').val(data.nome);
        $('#input-telefone-detalhes').val(data.telefone);
        $('#input-cidade-detalhes').val(data.cidade);
        $('#slct-estado-detalhes').val(data.estado);
        $('#slct-pais-detalhes').val(data.pais);        
  
        // Abra o modal de detalhes da pessoa
        UIkit.modal('#modal-detalhes-pessoa').show();
      },
      error: function (error) {
        console.error('Erro ao obter detalhes da pessoa via AJAX:', error);
      }
    });
}

function updatePessoa() {
    // Obtenha os valores do formulário
    var id = pessoaID;
    var nome = $('#input-nome-detalhes').val();
    var telefone = $('#input-telefone-detalhes').val();
    var cidade = $('#input-cidade-detalhes').val();
    var estado = $('#slct-estado-detalhes').val();
    var pais = $('#slct-pais-detalhes').val();

    // Crie um objeto com os dados do formulário
    var formData = {
        id: id,
        nome: nome,
        telefone: telefone,
        cidade: cidade,
        estado: estado,
        pais: pais
    };

    // Faça a requisição AJAX
    $.ajax({
        type: 'POST',
        url: '/pessoas/updt_pessoa/' + id,
        data: JSON.stringify(formData),  // Converte os dados para JSON
        contentType: 'application/json;charset=UTF-8',  // Define o cabeçalho Content-Type
        success: function (response) {
            // Exibe um SweetAlert de sucesso se a requisição for bem-sucedida
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Pessoa atualizada com sucesso.'
            });

            //Recarrega pessoas
            carregarPessoas(1);
        },
        error: function (error) {
            // Exibe um SweetAlert de erro se a requisição falhar
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'Ocorreu um erro ao atualizar a pessoa. Tente novamente mais tarde.'
            });
        }
    });
}

// Chama a função ao carregar a página
$(document).ready(function () {
    carregarPessoas(1);
});

// Adicione um evento de input para detectar mudanças no campo de busca
$('#searchPessoa').on('input', function() {
    // Obtém o valor do campo de busca
    var searchTerm = $(this).val();

    // Chama a função para carregar pessoas com o termo de busca
    carregarPessoasComBusca(searchTerm);
});

// Função para carregar e popular a tabela via AJAX com parâmetro de busca
function carregarPessoasComBusca(searchTerm) {
    $.ajax({
        url: '/pessoas/buscar_pessoas?search=' + searchTerm,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // Limpar a tabela antes de popular com os novos dados
            $('#tabela-pessoas tbody').empty();

            // Verificar se a resposta contém o array 'pessoas'
            if ('pessoas' in data && Array.isArray(data.pessoas)) {
                // Popula a tabela com os dados recebidos
                data.pessoas.forEach(function (pessoa) {
                    $('#tabela-pessoas tbody').append(`
                        <tr>
                            <td>${pessoa.id}</td>
                            <td>${pessoa.nome}</td>
                            <td><a href="https://api.whatsapp.com/send?phone=55${pessoa.telefone}&text=Olá, ${pessoa.nome}! Tudo bem?" target="_blank" uk-icon="icon: whatsapp"></a> ${pessoa.telefone}</td>
                            <td>${pessoa.cidade}</td>
                            <td><button class="uk-icon-link uk-margin-small-right" uk-icon="file-edit" onclick="detalhePessoa(${pessoa.id})"></button></td>
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

