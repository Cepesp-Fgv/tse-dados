import cepesp from "./cepesp";
import Fuse from "fuse.js";

let tableArea = $('#table-area');
let table = $('#query-table');
let clearBtn = $('#clear-btn');
let downloadBtn = $('#donwload-btn');
let downloadSqlBtn = $('#download-sql-btn');
let tableTools = $('.table-tools');
let jobInput = $('#job-input');
let yearInput = $('#year-input');
let agregacaoRegionalInput = $('#regionalAggregation-input');
let politicalAggregationInput = $('#politicalAggregation-input');
let munFilterInput = $('#filter-mun-input');
let ufFilterInput = $('#filter-uf-input');
let brancosInput = $('#brancos-input');
let nulosInput = $('#nulos-input');
let electedInput = $('#only-elected-input');
let partyFilterInput = $('#party-filter-input');
let nameFilterInput = $('#name-filter-input');
let governmentPeriodInput = $('#government-period-input');
let brancosNulosRegion = $('#brancos-nulos-region');
let columnsMessage = $('#selected-columns-message');
let progressMessage = $('#progress-message');
let errorMessage = $('#error-message');
let busyMessage = $('#busy-message');
let completeMessage = $('#complete-message');

$.fn.dataTableExt.sErrMode = (e) => {
    console.warn(e);
};


$(() => {
    $('#select-all').click(selectAllColumns);
    $('#select-default').click(selectDefaultColumns);
    $('input[name="c[]"]').change(updateSelectedColumnsCounter);

    toggleMunFilter();
    toggleUfFilter();
    toggleBrancosNulos();
    updateSelectedColumnsCounter();
});

jobInput.change(function () {
    if (yearInput.hasClass('not-change-year'))
        return;

    let cargo = $(this).val();
    let selected = yearInput.val();
    let years = cepesp.getYears(cargo);
    yearInput.html('');

    for (let i = 0; i < years.length; i++) {
        let s = selected.indexOf(`${years[i]}`) !== -1 ? 'selected' : '';
        yearInput.append(`<option value="${years[i]}" ${s}>${years[i]}</option>`);
    }
});

agregacaoRegionalInput.change(function (e) {
    toggleMunFilter();
    toggleUfFilter();
    refreshColumns();
});

politicalAggregationInput.change(function (e) {
    toggleBrancosNulos();
    refreshColumns();
});

function initNameAutoComplete(names) {
    let fuse = new Fuse(names || [], {
        shouldSort: true,
        threshold: 0.6,
        location: 0,
        distance: 100,
        maxPatternLength: 32,
        minMatchCharLength: 1,
    });

    nameFilterInput.autocomplete({hint: true}, [
        {
            displayKey: 'value',
            source: (q, cb) => {
                let results = fuse.search(q).slice(0, 5).map(i => {
                    return {value: names[i]}
                });
                cb(results);
            },
        }
    ]);
}

function refreshColumns() {
    let selected = getSelectedColumns();
    let columns_list = $('.columns-modal-list');

    cepesp.getColumns(getQueryData()).then((data) => {
        window.DEFAULT_COLUMNS = data.default_columns;
        columns_list.html('');

        for (let i = 0; i < data.columns.length; i++) {
            let column = data.columns[i];
            let translated = data.translated_columns[column];
            let checked = (selected.includes(column) || window.DEFAULT_COLUMNS.includes(column)) ? ' checked' : '';
            let description = data.descriptions[column];

            columns_list.append(`
                <div class="col-md-4">
                    <div class="custom-control custom-checkbox mt-2" style="overflow-wrap: break-word">
                        <input type="checkbox" class="custom-control-input" name="c[]"
                               value="${column}"
                               id="columns-${i}"
                               ${checked}>
                        <label class="custom-control-label d-block"
                               for="columns-${i}">${translated}</label>
                        <small class="text-muted d-block">${description}</small>
                    </div>
                </div>
            `)
        }

        updateSelectedColumnsCounter();
    })
}

function toggleMunFilter() {
    if (agregacaoRegionalInput.val() === "7") {
        $('#filter-mun').show('slow');
    } else {
        $('#filter-mun').hide('slow');
    }
}

function toggleUfFilter() {
    let reg, filter;
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
    let pol = parseInt(politicalAggregationInput.val())
    if (pol === 2 || pol == 1) {
        brancosNulosRegion.show('slow');
    } else {
        brancosNulosRegion.hide('slow');
    }
}

function getSelectedColumns() {
    let columns = [];
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
        $(this).prop('checked', window.DEFAULT_COLUMNS.indexOf($(this).val()) !== -1);
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
    let columns = getSelectedColumns();

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

function headerCol(i) {
    return table.find('th:eq(' + i + ')');
}

function downloadWithAthenas(queryId) {
    toastr.success('Your query download has began, please wait for a few minute...', 'Downloading CSV');

    $.fileDownload('/api/consulta/athena/result', {
        data: {id: queryId, ignore_version: true}
    });
}

function downloadWithLambda() {
    let data = getQueryData();
    data.length = -1;
    data.start = 0;
    data.format = 'csv';
    toastr.success('Your query download has began, please wait for a few minute...', 'Downloading CSV');

    $.fileDownload('https://api.cepespdata.io/api/query', {data});
}

function downloadSql() {
    let params = getQueryData();
    params.start = 0;
    params.length = -1;

    toastr.success('Your SQL download has began, please wait for a few minute...', 'Downloading SQL');
    $.fileDownload('/consulta/sql', {
        data: params
    });
}

function clear() {
    table.find('thead input').val('');
    table.DataTable().draw();
}

function columnSearch(column, search) {
    column
        .search(search)
        .draw();
}

function initializeColumns() {
    for (let i = 0; i < COLUMNS.length; i++) {
        let column = table.DataTable().columns(i);
        let name = COLUMNS[i];
        let default_value = DEFAULT_FILTERS[name] || "";
        let footerCol = headerCol(i);
        let inputGroup = $(`
            <div class="input-group input-group-sm" style="min-width:80px">
                <div class="input-group-prepend">
                    <button class="btn btn-outline-secondary" type="button"><i class="fa fa-search"></i></button>
                </div>
                <input type="text" class="form-control" value="${default_value}" id="column-${i}-filter">
            </div>
        `);

        let input = inputGroup.find('input');
        let button = inputGroup.find('button');

        if (footerCol.find('input').length > 0) return;

        input.keydown((e) => {
            if (e.keyCode === 13) {
                e.preventDefault();
                columnSearch(column, input.val());
                return false;
            }
        });

        button.click((e) => {
            e.preventDefault();
            columnSearch(column, input.val());
        });

        footerCol.append(inputGroup);
    }

}

function getQueryData(dataTable) {
    let q = {};
    let dt = dataTable || table.DataTable().ajax.params() || {};

    q.table = window.TABLE;
    q.draw = dt.draw;
    q.start = 0;
    q.length = 25;
    q.format = "json";
    q.c = getSelectedColumns();

    if (jobInput.length > 0)
        q.cargo = jobInput.val();

    if (yearInput.length > 0)
        q.anos = yearInput.val();

    if (agregacaoRegionalInput.length > 0)
        q.agregacao_regional = parseInt(agregacaoRegionalInput.val());

    if (politicalAggregationInput.length > 0)
        q.agregacao_politica = parseInt(politicalAggregationInput.val());

    if (munFilterInput.is(':visible'))
        q.mun_filter = munFilterInput.find('option:selected').val();

    if (ufFilterInput.is(':visible'))
        q.uf_filter = ufFilterInput.find('option:selected').val();

    if (partyFilterInput.length > 0)
        q.party = partyFilterInput.val();

    if (brancosInput.is(':checked'))
        q.brancos = true;

    if (nulosInput.is(':checked'))
        q.nulos = true;

    if (electedInput.is(':checked'))
        q.only_elected = true;

    if (nameFilterInput.length > 0)
        q.name_filter = nameFilterInput.val();

    if (governmentPeriodInput.length > 0)
        q.government_period = governmentPeriodInput.val()

    q.filters = {};
    for (let i = 0; i < window.COLUMNS.length; i++) {
        let name = window.COLUMNS[i];
        let value = $(
            `#column-${i}-filter`
        ).val();

        if (value != null && value !== '')
            q.filters[name] = value;
    }

    if (Object.keys(q.filters).length === 0) {
        q.filters = DEFAULT_FILTERS;
    }

    q.lang = LANG;

    q.mode = QUERY_MODE || "athenas";

    return q;
}

function showErrorResult(error) {
    let status = error.response ? error.response.status : 500;
    let message = error.response && error.response.data.error ? error.response.data.error : error;

    if (status === 200)
        return;

    console.warn(message);

    $('#query-table_wrapper').fadeOut();
    progressMessage.hide();
    completeMessage.hide();

    if (status === 503 || status === 504 || status === 429) {
        busyMessage.show();
    } else {
        errorMessage.show();
    }
}


function onQueryStatusUpdate(status, message, elapsed) {
    if (status === "RUNNING" || status === "QUEUED") {
        downloadBtn.prop('disabled', true).unbind('click');
    } else if (status === "SUCCEEDED") {
        progressMessage.hide();
        completeMessage.show();
    } else {
        showErrorResult(new Error(message));
    }
}


function initializeTable() {

    let cols = [];
    for (let i = 0; i < window.COLUMNS.length; i++) {
        let col = window.COLUMNS[i];
        cols.push({"name": col, "title": window.TRANSLATED_COLUMNS[i], "data": col});
    }

    downloadSqlBtn.click(downloadSql);

    tableArea.fadeIn('slow');
    table.DataTable({
        ajax: function (params, callback) {
            $('#query-table_wrapper').fadeOut();
            progressMessage.fadeIn();

            if (QUERY_MODE === "lambda") {
                downloadBtn.prop('disabled', false).unbind('click').click((e) => {
                    e.preventDefault();
                    downloadWithLambda();
                });

                cepesp
                    .lambdaQuery(getQueryData(params))
                    .catch(showErrorResult)
                    .then(function (data) {
                        $('#query-table_wrapper').fadeIn();
                        progressMessage.fadeOut();
                        callback(data);
                    });
            } else  {
                cepesp
                    .runQuery(getQueryData(params), onQueryStatusUpdate)
                    .catch(showErrorResult)
                    .then(function ({info, results}) {
                        $('#query-table_wrapper').fadeIn();
                        completeMessage.fadeOut();
                        callback(results);

                        downloadBtn.prop('disabled', false).unbind('click').click((e) => {
                            e.preventDefault();
                            downloadWithAthenas(info.id);
                        });

                    });
            }
        },
        processing: true,
        ordering: false,
        serverSide: true,
        columns: cols,
        paging: false,
        bInfo: false,
        responsive: false,
        initComplete: function () {
            tableTools.removeAttr('disabled');
            clearBtn.click(clear);

            $('#query-table_filter').hide();
            $('#loading-alert').fadeOut('slow');

            initializeColumns();
        }
    });

}

window.initializeTable = initializeTable;
window.initNameAutoComplete = initNameAutoComplete;