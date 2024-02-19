var campanhaID;
var page;

// Função para carregar e popular a tabela via AJAX
function carregarCampanhas(page) {
    $.ajax({
        url: '/campanhas?page=' + page,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            //console.log(data);
            // Limpar a tabela antes de popular com os novos dados
            $('#tabela-campanhas tbody').empty();

            // Verificar se a resposta contém o array 'campanhas'
            if ('campanhas' in data && Array.isArray(data.campanhas)) {
                // Popula a tabela com os dados recebidos
                data.campanhas.forEach(function (campanha) {
                    $('#tabela-campanhas tbody').append(`
            <tr data-aos="fade-right">
              <td>${campanha.id}</td>
              <td>${campanha.nome}</td>
              <td>${parseFloat(campanha.meta).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
              <td>${campanha.criador}</td>
              <td>${new Date(campanha.dt_criacao).toLocaleString()}</td>
              <td>${new Date(campanha.dt_inicio).toLocaleDateString()}</td>
              <td>${new Date(campanha.dt_fim).toLocaleDateString()}</td>
              <td><button class="uk-icon-link uk-margin-small-right" uk-icon="file-edit" onclick="detalheCampanha(${campanha.id})"></button></td>
            </tr>
          `);
                });
            } else {
                console.warn('Array de campanhas está vazio ou ausente na resposta.');
            }
            atualizarPaginacao(data.paginacao);
        },
        error: function (error) {
            console.error('Erro ao obter campanhas via AJAX:', error);
        }
    });
}

// Função para atualizar a estrutura da paginação UIkit
function atualizarPaginacao(paginacao) {
    // Limpa a paginação antes de atualizar
    $('#pagina-campanhas').empty();

    // Adiciona o botão de página anterior
    if (paginacao.has_prev) {
        $('#pagina-campanhas').append(`
        <li><a href="#" onclick="carregarcampanhas(${paginacao.prev_page})"><span uk-pagination-previous></span></a></li>
      `);
    } else {
        $('#pagina-campanhas').append('<li class="uk-disabled"><span uk-pagination-previous></span></li>');
    }

    // Adiciona os botões de páginas
    paginacao.pages.forEach(function (page) {
        if (page === '...') {
            $('#pagina-campanhas').append('<li class="uk-disabled"><span>…</span></li>');
        } else if (page === paginacao.current_page) {
            $('#pagina-campanhas').append(`<li class="uk-active"><span>${page}</span></li>`);
        } else {
            $('#pagina-campanhas').append(`<li><a href="#" onclick="carregarcampanhas(${page})">${page}</a></li>`);
        }
    });

    // Adiciona o botão de próxima página
    if (paginacao.has_next) {
        $('#pagina-campanhas').append(`
        <li><a href="#" onclick="carregarcampanhas(${paginacao.next_page})"><span uk-pagination-next></span></a></li>
      `);
    } else {
        $('#pagina-campanhas').append('<li class="uk-disabled"><span uk-pagination-next></span></li>');
    }
}

function NovaCampanha() {
    // Obtenha os valores do formulário
    var nome = $('#input-nome').val();
    var dt_inicio = $('#input-dt-inicio').val();
    var dt_fim = $('#input-dt-fim').val();
    var meta = $('#input-meta').val();
    var tipo = $('#slct-tipo').val();

    // Crie um objeto com os dados do formulário
    var formData = {
        'nome': nome,
        'dt_inicio': dt_inicio,
        'dt_fim': dt_fim,
        'meta': meta,
        'tipo': tipo
    };

    //console.log(formData);

    // Faça a requisição AJAX
    $.ajax({
        type: 'POST',
        url: '/campanhas/add_campanha',
        data: JSON.stringify(formData),  // Converte os dados para JSON
        contentType: 'application/json;charset=UTF-8',  // Define o cabeçalho Content-Type
        success: function (response) {
            // Exibe um SweetAlert de sucesso se a requisição for bem-sucedida
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'campanha adicionada com sucesso.'
            });

            //Recarrega campanhas
            carregarCampanhas(1);
        },
        error: function (error) {
            // Exibe um SweetAlert de erro se a requisição falhar
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'Ocorreu um erro ao adicionar a campanha. Tente novamente mais tarde.'
            });
        }
    });
}

function detalheCampanha(id) {
    // Faça a requisição AJAX para obter os detalhes da campanha
    $.ajax({
        type: 'GET',
        url: '/campanhas/campanha/' + id,
        dataType: 'json',
        success: function (data) {
            campanhaID = id;
            //console.log(data);
            // Preencha os campos do modal com os dados recebidos
            $('#input-nome-detalhes').val(data.nome);
            $('#input-telefone-detalhes').val(data.telefone);
            $('#input-cidade-detalhes').val(data.cidade);
            $('#slct-estado-detalhes').val(data.estado);
            $('#slct-pais-detalhes').val(data.pais);

            // Abra o modal de detalhes da campanha
            UIkit.modal('#modal-detalhes-campanha').show();
        },
        error: function (error) {
            console.error('Erro ao obter detalhes da campanha via AJAX:', error);
        }
    });
}

function updateCampanha() {
    // Obtenha os valores do formulário
    var id = campanhaID;
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
        url: '/campanhas/updt_campanha/' + id,
        data: JSON.stringify(formData),  // Converte os dados para JSON
        contentType: 'application/json;charset=UTF-8',  // Define o cabeçalho Content-Type
        success: function (response) {
            // Exibe um SweetAlert de sucesso se a requisição for bem-sucedida
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'campanha atualizada com sucesso.'
            });

            //Recarrega campanhas
            carregarCampanhas(1);
        },
        error: function (error) {
            // Exibe um SweetAlert de erro se a requisição falhar
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'Ocorreu um erro ao atualizar a campanha. Tente novamente mais tarde.'
            });
        }
    });
}

// Chama a função ao carregar a página
$(document).ready(function () {
    carregarCampanhas(1);
    var cleave = new Cleave('#input-meta', {
        numeral: true,
        numeralThousandsGroupStyle: 'thousand'
    });
});

// Adicione um evento de input para detectar mudanças no campo de busca
$('#searchCampanha').on('input', function () {
    // Obtém o valor do campo de busca
    var searchTerm = $(this).val();

    // Chama a função para carregar campanhas com o termo de busca
    carregarCampanhasComBusca(searchTerm);
});

// Função para carregar e popular a tabela via AJAX com parâmetro de busca
function carregarCampanhasComBusca(searchTerm) {
    $.ajax({
        url: '/campanhas/buscar_campanhas?search=' + searchTerm,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // Limpar a tabela antes de popular com os novos dados
            $('#tabela-campanhas tbody').empty();

            // Verificar se a resposta contém o array 'campanhas'
            if ('campanhas' in data && Array.isArray(data.campanhas)) {
                // Popula a tabela com os dados recebidos
                data.campanhas.forEach(function (campanha) {
                    $('#tabela-campanhas tbody').append(`
                        <tr>
                            <td>${campanha.id}</td>
                            <td>${campanha.nome}</td>
                            <td><a href="https://api.whatsapp.com/send?phone=55${campanha.telefone}&text=Olá, ${campanha.nome}! Tudo bem?" target="_blank" uk-icon="icon: whatsapp"></a> ${campanha.telefone}</td>
                            <td>${campanha.cidade}</td>
                            <td><button class="uk-icon-link uk-margin-small-right" uk-icon="file-edit" onclick="detalhecampanha(${campanha.id})"></button></td>
                        </tr>
                    `);
                });
            } else {
                console.warn('Array de campanhas está vazio ou ausente na resposta.');
            }
        },
        error: function (error) {
            console.error('Erro ao obter campanhas via AJAX:', error);
        }
    });
}

