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
            console.log(data.campanhas);
            // Verificar se a resposta contém o array 'campanhas'
            if ('campanhas' in data && Array.isArray(data.campanhas)) {
                // Popula a tabela com os dados recebidos
                data.campanhas.forEach(function (campanha) {
                    $('#tabela-campanhas tbody').append(`
            <tr data-aos="fade-right">
              <td>${campanha.id}</td>
              <td>${campanha.nome}</td>
              <td>${parseFloat(campanha.meta).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
              <td>${campanha.tipo}</td>
              <td>${new Date(campanha.dt_criacao).toLocaleString()}</td>
              <td>${new Date(`${campanha.dt_inicio}T23:59:59Z`).toLocaleDateString()}</td>
              <td>${new Date(`${campanha.dt_fim}T23:59:59Z`).toLocaleDateString()}</td>
              <td class="uk-margin"><button class="uk-icon-link uk-margin-small-right" uk-icon="file-edit" onclick="detalheCampanha(${campanha.id})"></button></td>
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
        <li><a href="#" onclick="carregarCampanhas(${paginacao.prev_page})"><span uk-pagination-previous></span></a></li>
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
            $('#pagina-campanhas').append(`<li><a href="#" onclick="carregarCampanhas(${page})">${page}</a></li>`);
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
    carregarTipos()

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
            $('#input-dt-inicio-detalhes').val(data.dt_inicio);
            $('#input-dt-fim-detalhes').val(data.dt_fim);
            $('#input-meta-detalhes').val(data.meta);
            $('#slct-tipo-detalhes').val(data.tipo);

            // Abra o modal de detalhes da campanha
            UIkit.modal('#modal-detalhes-campanha').show();
        },
        error: function (error) {
            console.error('Erro ao obter detalhes da campanha via AJAX:', error);
        }
    });
}

function updateCampanha() {
    var id = campanhaID;
    var nome = $('#input-nome-detalhes').val();
    var dtInicio = $('#input-dt-inicio-detalhes').val();
    var dtFim = $('#input-dt-fim-detalhes').val();
    var meta = $('#input-meta-detalhes').val();
    var tipo = $('#slct-tipo-detalhes').val();

    // Cria um objeto com os dados do formulário
    var formData = {
        id: id,
        nome: nome,
        dt_inicio: dtInicio,
        dt_fim: dtFim,
        meta: meta,
        tipo: tipo
    };


    // Faz a requisição AJAX
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
                text: 'Campanha atualizada com sucesso.'
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

    var cleaveMeta = new Cleave('#input-meta', {
        numeral: true,
        numeralThousandsGroupStyle: 'thousand'
    });
    
    var cleaveMetaDetalhes = new Cleave('#input-meta-detalhes', {
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
                            <td>${parseFloat(campanha.meta).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                            <td>${campanha.criador}</td>
                            <td>${new Date(campanha.dt_criacao).toLocaleString()}</td>
                            <td>${new Date(`${campanha.dt_inicio}T23:59:59Z`).toLocaleDateString()}</td>
                            <td>${new Date(`${campanha.dt_fim}T23:59:59Z`).toLocaleDateString()}</td>
                            <td class="uk-margin"><button class="uk-icon-link uk-margin-small-right" uk-icon="file-edit" onclick="detalheCampanha(${campanha.id})"></button></td>
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

function carregarTipos(){
    $.ajax({
        url: '/dimensoes/tipos',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $("#slct-tipo select").empty();

            if ('tipos' in data) {
                data.tipos.forEach(function (tipo){
                    $("#slct-tipo select").append(`
                        <option value="${tipo.id}">${tipo.nome}</option>
                    `);
                });
            } else {
                console.warn('Erro ao carregar tipos');
            }
        },
        error: function (error) { 
            console.error('Erro na requisição de tipos.')
        }
    });
}