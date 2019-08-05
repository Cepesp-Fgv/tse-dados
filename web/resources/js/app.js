window.$ = window.jQuery = require('jquery');
window.Popper = require('popper.js/dist/umd/popper.js').default;

require('bootstrap');
require('datatables.net-bs4');
require('jquery-file-download');
require('autocomplete.js/index_jquery');

window.toastr = require("toastr");

// Utils
window.wait = (time) => {
    return new Promise( (resolve) => setTimeout((() => resolve()), time))
};

toastr.options = {closeButton: true, positionClass: 'toast-top-right', onclick: null};

/* Set the defaults for DataTables initialisation */
$.extend(true, $.fn.dataTable.defaults, {
    "dom": "<'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r><'table-responsive't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",
    "language": {
        "lengthMenu": " _MENU_ records ",
        "paginate": {
            "previous": '<i class="fa fa-angle-left"></i>',
            "next": '<i class="fa fa-angle-right"></i>'
        }
    }
});

$(() => {
  $('[data-toggle="tooltip"]').tooltip();
});
