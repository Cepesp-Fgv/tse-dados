var tableArea = $('#table-area');
var table = $('#query-table');
var clearBtn = $('#clear-btn');
var downloadBtn = $('#donwload-btn');
var downloadSqlBtn = $('#download-sql-btn');
var tableTools = $('.table-tools');
var jobInput = $('#job-input');
var yearInput = $('#year-input');
var agregacaoRegionalInput = $('#regionalAggregation-input');
var politicalAggregationInput = $('#politicalAggregation-input');
var munFilterInput = $('#filter-mun-input');
var ufFilterInput = $('#filter-uf-input');
var brancosInput = $('#brancos-input');
var nulosInput = $('#nulos-input');
var electedInput = $('#only-elected-input');
var brancosNulosRegion = $('#brancos-nulos-region');
var columnsMessage = $('#selected-columns-message');
var progressMessage = $('#progress-message');
var errorMessage = $('#error-message');
var busyMessage = $('#busy-message');

toastr.options = {closeButton: true, positionClass: 'toast-top-right', onclick: null};

$(document).ready(function () {
    $('#select-all').click(selectAllColumns);
    $('#select-default').click(selectDefaultColumns);
    $('input[name="c[]"]').change(updateSelectedColumnsCounter);

    toggleMunFilter();
    toggleUfFilter();
    toggleBrancosNulos();
    updateSelectedColumnsCounter();
});

yearInput.change(function () {
    var years = $(this).val();
    $('#modal-anos-input').val(years.join(','));
});

jobInput.change(function () {
    var cargo = $(this).val();
    var years = getYears(cargo);
    yearInput.html('');

    for (var i = 0; i < years.length; i++) {
        yearInput.append('<option value="' + years[i] + '">' + years[i] + '</option>');
    }

    $('#modal-cargo-input').val(cargo);
});

agregacaoRegionalInput.change(function (e) {
    toggleMunFilter();
    toggleUfFilter();
});

politicalAggregationInput.change(function (e) {
    toggleBrancosNulos();
});

function toggleMunFilter() {
    if (agregacaoRegionalInput.val() === "7") {
        $('#filter-mun').show('slow');
    } else {
        $('#filter-mun').hide('slow');
    }
}

function toggleUfFilter() {
    var reg, filter;
    reg = parseInt(agregacaoRegionalInput.val());
    filter = $('#filter-uf');
    if ([6, 8, 9].indexOf(reg) !== -1) {
        filter.show('slow');
        if (reg === 9) {
            filter.find('select').prop('required', true);
        } else {
            filter.find('select').removeAttr('required');
        }
    } else {
        filter.find('select').removeAttr('required');
        filter.hide('slow');
    }
}

function toggleBrancosNulos() {
    if (parseInt(politicalAggregationInput.val()) === 4) {
        brancosNulosRegion.hide('slow');
    } else {
        brancosNulosRegion.show('slow');
    }
}

function getSelectedColumns() {
    var columns = [];
    $.each($('input[name="c[]"]:checked'), function () {
        columns.push($(this).val());
    });

    return columns;
}

function selectAllColumns() {
    $('input[name="c[]"]').prop('checked', true);
    updateSelectedColumnsCounter();
}

function selectDefaultColumns() {
    $('input[name="c[]"]').each(function () {
        $(this).prop('checked', DEFAULT_COLUMNS.indexOf($(this).val()) !== -1);
    });
    updateSelectedColumnsCounter();
}

function disableUnselectedColumns() {
    $('input[name="c[]"]:not(:checked)').prop('disabled', true);
}

function enableAllColumns() {
    $('input[name="c[]"]').prop('disabled', false);
}

function updateSelectedColumnsCounter() {
    var columns = getSelectedColumns();

    columnsMessage.removeClass().addClass('alert');
    if (columns.length === 0) {
        columnsMessage.addClass('alert-danger').html('Selecione ao menos uma coluna.');
    } else if (columns.length >= 30) {
        columnsMessage.addClass('alert-danger').html('Você só pode selecionar no máximo 30 colunas.');
        disableUnselectedColumns();
    } else {
        enableAllColumns();
        columnsMessage.addClass('alert-primary').html(columns.length + ' colunas selecionadas.');
    }
}

function getYears(job) {
    switch (parseInt(job)) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
        case 9:
        case 10:
            return [2018, 2014, 2010, 2006, 2002, 1998];
        case 11:
        case 12:
        case 13:
            return [2016, 2012, 2008, 2004, 2000];
        default:
            return [];
    }
}

function headerCol(i) {
    return table.find('th:eq(' + i + ')');
}

function download(queryId) {
    toastr.success('Your query download has began, please wait for a few minute...', 'Downloading CSV');

    $.fileDownload('/api/consulta/athena/result', {
        data: {id: queryId, ignore_version: true}
    });
}

function downloadSql() {
    var params = getQueryData(table.DataTable().ajax.params());
    params.start = 0;
    params.length = -1;

    toastr.success('Your SQL download has began, please wait for a few minute...', 'Downloading SQL');
    $.fileDownload('/consulta/sql', {
        data: params
    });
}

function clear() {
    table.find('thead input').val('');
    table.DataTable().columns().every(function (i) {
        table.DataTable().columns(i).search('');
    });
    table.DataTable().draw();
}

function columnSearch(column, search) {
    column
        .search(search)
        .draw();
}

function initializeColumnSearch(i) {

    var column = table.DataTable().columns(i);
    var footerCol = headerCol(i);
    var inputGroup = $(
        '<div class="input-group input-group-sm">' +
        '<div class="input-group-btn">' +
        '<button class="btn btn-default">' +
        '<i class="glyphicon glyphicon-search"></i>' +
        '</button>' +
        '</div>' +
        '<input type="text" class="form-control" style="min-width: 50px" />' +
        '</div>'
    );
    var input = inputGroup.find('input');
    var button = inputGroup.find('button');

    if (footerCol.find('input').length > 0) return;

    input.keyup(function (e) {
        if (e.keyCode === 13) {
            columnSearch(column, input.val());
        }
    });

    button.click(function (e) {
        e.preventDefault();
        columnSearch(column, input.val());
    });

    footerCol.append(inputGroup);
}

function initializeColumns() {
    table.DataTable().columns().every(function (i) {
        initializeColumnSearch(i);
    });
}

function getQueryData(dataTable) {
    var q = {};
    q.table = TABLE;
    q.draw = dataTable.draw;
    q.start = dataTable.start;
    q.length = dataTable.length;
    q.format = "json";
    q.c = COLUMNS;
    q.cargo = parseInt(jobInput.val());
    q.agregacao_regional = parseInt(agregacaoRegionalInput.val());

    if (politicalAggregationInput.length > 0)
        q.agregacao_politica = parseInt(politicalAggregationInput.val());

    q.anos = yearInput.val();
    if (munFilterInput.is(':visible'))
        q.mun_filter = munFilterInput.find('option:selected').val();

    if (ufFilterInput.is(':visible'))
        q.uf_filter = ufFilterInput.find('option:selected').val();

    if (brancosInput.is(':checked'))
        q.brancos = true;

    if (nulosInput.is(':checked'))
        q.nulos = true;

    if (electedInput.is(':checked'))
        q.only_elected = true;

    q.filters = {};
    for (var i = 0; i < dataTable.columns.length; i++) {
        var name = dataTable.columns[i]['name'];
        var value = dataTable.columns[i]['search']['value'];

        if (!(value == null || value === undefined || value === ''))
            q.filters[name] = value;
    }

    return q;
}

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout((function () {
            resolve();
        }), time);
    });
}

function cepespGetStatus(query_id) {
    return $.get('/api/consulta/athena/status', {id: query_id});
}

function cepespGetResult(query_id, start, length) {
    return $.get('/api/consulta/athena/result', {
        id: query_id,
        start: start,
        length: length,
        format: 'json',
        ignore_version: true
    });
}

function showQueryResult(data, callback, status, sleep, message) {
    status = status || "QUEUED";
    sleep = sleep || 1000;

    if (status && (status === "RUNNING" || status === "QUEUED")) {
        delay(sleep).then(function () {
            cepespGetStatus(data.id)
                .done(function (response) {
                    showQueryResult(data, callback, response.status, sleep * 2, response.message);
                })
                .error(showErrorResult);
        });
    } else if (status && status === "SUCCEEDED") {
        downloadBtn.unbind('click').click(function () {
            download(data.id)
        });

        cepespGetResult(data.id, data.start, data.length)
            .done(function (response) {
                $('#query-table_wrapper').fadeIn();
                progressMessage.fadeOut();
                callback(response);
            })
            .error(showErrorResult);
    } else {
        var xhr = {responseJSON: {error: message, status: status === "FAILED" ? 500 : 429}};
        showErrorResult(xhr);
    }
}

function showErrorResult(xhr) {
    if (xhr.status === 200)
        return;

    console.warn(xhr.responseJSON.error);

    $('#query-table_wrapper').fadeOut();
    progressMessage.fadeOut();

    if (xhr.status === 503 || xhr.status === 504 || xhr.status === 429) {
        busyMessage.fadeIn();
    } else {
        errorMessage.fadeIn();
    }
}


function populateTable() {

    var cols = [];
    for (var i = 0; i < COLUMNS.length; i++) {
        var col = COLUMNS[i];
        cols.push({"name": col, "title": TRANSLATED_COLUMNS[i], "data": col});
    }

    tableArea.fadeIn('slow');
    table.dataTable({
        ajax: function (data, callback) {
            $('#query-table_wrapper').fadeOut();
            progressMessage.fadeIn();
            $.get('/api/consulta/athena/query', getQueryData(data)).done(function (response) {
                data.id = response.id;
                showQueryResult(data, callback);
            }).fail(showErrorResult);
        },
        processing: true,
        ordering: false,
        serverSide: true,
        columns: cols,
        pagingType: 'simple_numbers',
        bInfo: false,
        responsive: false,
        initComplete: function () {
            tableTools.removeAttr('disabled');
            clearBtn.click(clear);
            downloadSqlBtn.click(downloadSql);
            $('#query-table_filter').hide();
            $('#loading-alert').fadeOut('slow');

            initializeColumns();
        }
    });

}

toggleUfFilter();
toggleMunFilter();