function realParaFloat(valorEmReal) {
    // Remove o prefixo "R$" e quaisquer caracteres não-dígitos
    var valorLimpo = valorEmReal.replace(/[^\d,]/g, '');
    // Substitui a vírgula decimal por ponto para formar um número de ponto flutuante válido
    var valorFloat = parseFloat(valorLimpo.replace(',', '.'));
    return valorFloat;
}

function getCampanha(id) {
    // Faça a requisição AJAX para obter os detalhes da campanha
    $.ajax({
        type: 'GET',
        url: '/campanhas/campanha/' + id,
        dataType: 'json',
        success: function (data) {
            console.log(data);
            campanhaID = id;

            // Preencha os campos do modal com os dados recebidos
            $('#nomeCampanhaSelecionada').text(data.nome);
            $('#idCampanhaSelecionada').val(data.id);
            //$('#slct-tipo-detalhes select').val(data.tipo[0]);

        },
        error: function (error) {
            console.error('Erro ao obter detalhes da campanha via AJAX:', error);
        }
    });
}

// Função para calcular o total em Reais
function calcularTotal() {
    var quantidade = parseFloat($('#quantidadeDeRifas').val());
    var valorUnitario = parseFloat($('#valorDaRifa').val().replace(/[^\d,]/g, '').replace(',', '.'));
    var total = quantidade * valorUnitario;
    // Formatar o total em Reais com 2 casas decimais e o símbolo R$
    $('#totalDeRifasEmReais').val('R$ ' + total.toFixed(2));
}

function confirmarGeracao() {
    let qtdDeRifas = $("#quantidadeDeRifas").val();
    let vlrDaRifa = $("#valorDaRifa").val();
    let nmCampanha = $("#nomeCampanhaSelecionada").val();
    let idCampanha = $("#idCampanhaSelecionada").val();
    Swal.fire({
        title: "Confirme os dados!",
        text: `Você deseja gerar ${qtdDeRifas} no valor de ${vlrDaRifa} para a campanha ${nmCampanha}?`,
        icon: "warning",
        showDenyButton: true,
        confirmButtonText: "Confirmar",
        denyButtonText: "Cancelar",
        dangerMode: true,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            gerarRifas(idCampanha, qtdDeRifas, vlrDaRifa);
        } else if (result.isDenied) {
            Swal.fire("Nada aconteceu...", "", "info");
        }
    });

}

function gerarRifas(id, qtdDeRifas, vlrDaRifa) {
    let formData = {
        'idCampanha': id,
        'qtdDeRifas': qtdDeRifas,
        'vlrDaRifa': realParaFloat(vlrDaRifa)
    }

    $.ajax({
        type: 'POST',
        url: '/rifas/gerarRifas',
        data: JSON.stringify(formData),  // Converte os dados para JSON
        contentType: 'application/json;charset=UTF-8',  // Define o cabeçalho Content-Type
        success: function (response) {
            // Exibe um SweetAlert de sucesso se a requisição for bem-sucedida
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: response.message
            }).then(function () {
                // Recarregar a página após clicar em "OK"
                location.reload();
            });

        },
        error: function (error) {
            // Exibe um SweetAlert de erro se a requisição falhar
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: error.responseJSON.message
            });
        }
    });
}

function calularResumoCotacao() {
    let tdn = $('#totalDeNumeros').text();
    let vdr = $('#vlrDaRifa').val();
    let qdt = $('#quantidadeDeTaloes').val();
    let qdc = $("#quantidadeDeCotistas").val();

    console.log(tdn, vdr, qdt, qdc)

    let numPorTalao = tdn / qdt;
    let talaoPorCotista = qdt / qdc;
    let metaIndividual = (talaoPorCotista * numPorTalao) * vdr;

    $('#numPorTalao').text(numPorTalao);
    $('#talaoPorCotista').text(talaoPorCotista);
    $('#metaIndividual').text('R$ ' + metaIndividual.toFixed(2));

    // Verifique se os números são inteiros
    let numerosSaoInteiros = Number.isInteger(numPorTalao) && Number.isInteger(talaoPorCotista);

    // Atualize a mensagem de erro e habilite/desabilite o botão conforme necessário
    if (numerosSaoInteiros) {
        $('#mensagemErro').text('');
        $('#confirmarGeracaoDeTaloes').prop('disabled', false);
    } else {
        $('#mensagemErro').text('O número de talões por cotista e a quantidade de números por talão devem ser valores inteiros!');
        $('#confirmarGeracaoDeTaloes').prop('disabled', true);
    }
}

function confirmarGeracaoDeTaloes() {
    let qdt = $('#quantidadeDeTaloes').val();

    Swal.fire({
        title: "Confirme os dados!",
        text: `Você deseja gerar ${qdt} talões?`,
        icon: "warning",
        showDenyButton: true,
        confirmButtonText: "Confirmar",
        denyButtonText: "Cancelar",
        dangerMode: true,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            gerarTaloes();
        } else if (result.isDenied) {
            Swal.fire("Nada aconteceu...", "", "info");
        }
    });
}

function gerarTaloes() {
    let formData = {
        'id_campanha': $("#idCampanhaSelecionada").val(),
        'qtdDeTaloes': $('#quantidadeDeTaloes').val(),
        'qtdDeNumeros': $('#totalDeNumeros').text(),
    }

    // Faça a requisição AJAX
    $.ajax({
        type: 'POST',
        url: '/rifas/gerarTaloes',
        data: JSON.stringify(formData),  // Converte os dados para JSON
        contentType: 'application/json;charset=UTF-8',  // Define o cabeçalho Content-Type
        success: function (response) {
            // Exibe um SweetAlert de sucesso se a requisição for bem-sucedida
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: response.message
            }).then(function () {
                // Recarregar a página após clicar em "OK"
                location.reload();
            });

        },
        error: function (response) {
            // Exibe um SweetAlert de erro se a requisição falhar
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: response.error
            });
        }
    });
}

//Roda instruções apenas se 'rifas' estiver na url
if (/\/rifas\//.test(window.location.href)) {

    $('#valorDaRifa').on('input', function () {
        // Remove qualquer não-dígito e qualquer ponto ou vírgula
        var sanitized = $(this).val().replace(/[^0-9]/g, '').replace(/[,\.]/g, '');
        // Divide o valor em partes, mantendo os últimos dois dígitos como centavos
        var amount = sanitized.slice(0, -2) + ',' + sanitized.slice(-2);
        // Formata o valor como moeda brasileira (Real)
        $(this).val('R$ ' + amount);
    });

    // Listener para atualizar o total quando a quantidade de rifas muda
    $('#quantidadeDeRifas').on('input', function () {
        calcularTotal();
    });

    // Listener para atualizar o total quando o valor da rifa muda
    $('#valorDaRifa').on('input', function () {
        calcularTotal();
    });

    // Listener para atualizar o resumo quando a quantidade de talões mudar
    $("#quantidadeDeTaloes").on('input', function () {
        calularResumoCotacao();
    });

    // Listener para atualizar o resumo quando a quantidade de cotistas mudar
    $("#quantidadeDeCotistas").on('input', function () {
        calularResumoCotacao();
    });

    // Listener para atualizar o resumo quando a quantidade de cotistas mudar
    $("#quantidadeDeCotistas").on('input', function () {
        calularResumoCotacao();
    });

    // Listener para atualizar o cotista responsavel pelo talão
    $(".atualizaCotista").on('change', function () {

        let talaoId = $(this).data('id'); // Obtém o ID do talão do atributo data-id

        let formData = {
            'cotista': $(this).val(), // Obtém o valor selecionado no select
            'talaoId': talaoId // Passa o ID do talão como parte dos dados a serem enviados
        };

        $.ajax({
            type: 'POST',
            url: '/rifas/atualizarCotista',
            data: JSON.stringify(formData),
            contentType: 'application/json;charset=UTF-8',
            success: function (response) {
                UIkit.notification({ message: response.message, status: 'success', pos: 'bottom-right' })
            },
            error: function (response) {
                // Exibe um SweetAlert de erro se a requisição falhar
                Swal.fire({
                    icon: 'error',
                    title: 'Erro!',
                    text: response.error
                });
            }
        })
    });
}