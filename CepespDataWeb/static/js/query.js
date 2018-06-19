var tableArea = $('#table-area');
var table = $('#query-table');
var clearBtn = $('#clear-btn');
var downloadBtn = $('#donwload-btn');
var tableTools = $('.table-tools');
var jobInput = $('#job-input');
var yearInput = $('#year-input');
var agregacaoRegionalInput = $('#regionalAggregation-input');
var politicalAggregationInput = $('#politicalAggregation-input');
var munFilterInput = $('#filter-mun-input');
var ufFilterInput = $('#filter-uf-input');
var brancosInput = $('#brancos-input');
var nulosInput = $('#nulos-input');
var brancosNulosRegion = $('#brancos-nulos-region');

$.fn.dataTableExt.sErrMode = 'throw';
toastr.options = {closeButton: true, positionClass: 'toast-top-right', onclick: null};

$(document).ready(function () {
    $(".dropdown-toggle").dropdown();
    $('#select-all').click(selectAllColumns);
    $('#select-default').click(selectDefaultColumns);

    toggleMunFilter();
    toggleUfFilter();
    toggleBrancosNulos();
});

jobInput.change(function (e) {
    var years = getYears(parseInt($(this).find('option:selected').val()));
    yearInput.html('');

    for (var i = 0; i < years.length; i++) {
        yearInput.append('<option value="' + years[i] + '">' + years[i] + '</option>');
    }
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

function selectAllColumns() {
    $('input[name="selected_columns[]"]').prop('checked', true);
}

function selectDefaultColumns() {
    $('input[name="selected_columns[]"]').each(function () {
        $(this).prop('checked', DEFAULT_COLUMNS.indexOf($(this).val()) !== -1);
    });
}

function getYears(job) {
    switch (job) {
        case 1:
        case 3:
        case 5:
        case 6:
        case 7:
        case 8:
            return [2014, 2010, 2006, 2002, 1998];
        case 11:
        case 13:
            return [2016, 2012, 2008, 2004, 2000];
        default:
            return [];
    }
}

function headerCol(i) {
    return table.find('th:eq(' + i + ')');
}

function download() {
    var params = table.DataTable().ajax.params();
    params.format = "csv";
    toastr.success('Your query download has began, please wait for a few minute...', 'Downloading CSV');

    $.fileDownload(ENDPOINT, {
        data: params
    });
}

function downloadSql() {
    var cargo = parseInt(jobInput.val());
    var ano = parseInt(yearInput.val());

    toastr.success('Your SQL download has began, please wait for a few minute...', 'Downloading SQL');
    $.fileDownload('/consulta/tse/sql', {
        data: {cargo: cargo, ano: ano}
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
        '<input type="text" class="form-control" style="min-width: 100px" />' +
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

function populateTable() {

    var cols = [];
    for (var i = 0; i < COLUMNS.length; i++) {
        var col = COLUMNS[i];
        cols.push({"name": col, "title": TRANSLATED_COLUMNS[i], "data": col});
    }

    tableArea.fadeIn('slow');
    table.dataTable({
        ajax: {
            url: ENDPOINT,
            data: function (d) {
                d.format = "json";
                d.selected_columns = COLUMNS;
                d.cargo = parseInt(jobInput.val());
                d.agregacao_regional = parseInt(agregacaoRegionalInput.val());

                if (politicalAggregationInput.length > 0)
                    d.agregacao_politica = parseInt(politicalAggregationInput.val());

                d.anos = yearInput.val();
                if (munFilterInput.is(':visible'))
                    d.mun_filter = munFilterInput.find('option:selected').val();

                if (ufFilterInput.is(':visible'))
                    d.uf_filter = ufFilterInput.find('option:selected').val();

                if (brancosInput.is(':checked'))
                    d.brancos = true;

                if (nulosInput.is(':checked'))
                    d.nulos = true;
            }
        },
        processing: true,
        ordering: false,
        serverSide: true,
        responsive: true,
        columns: cols,
        initComplete: function () {
            tableTools.removeAttr('disabled');
            clearBtn.click(clear);
            downloadBtn.click(download);
            $('#query-table_filter').hide();
            $('#loading-alert').fadeOut('slow');

            initializeColumns();
        }
    });

}

toggleUfFilter();
toggleMunFilter();