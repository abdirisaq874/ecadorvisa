/*
    JA 2015.08.17
    Implementa utilitarios jquery
*/

$(document).ready(function() {
    $(".JS_BtnKendo").kendoButton();
    $(".JS_TxtKendo").kendoMaskedTextBox();

    
    if ($('#btnGridExcel').length) // use this if you are using id to check
    {
        $("#btnGridExcel > span").removeClass().addClass('ui-icon-excel');
    }
    if ($('#btnGridPdf').length) // use this if you are using id to check
    {
        $("#btnGridPdf > span").removeClass().addClass('ui-icon-pdf');
    }
    if ($('#btnGridView').length) // use this if you are using id to check
    {
        $("#btnGridView > span").removeClass().addClass('ui-icon ui-icon-person');
    }
    if ($('#btnGridAdd').length) // use this if you are using id to check
    {
        $("#btnGridAdd > span").removeClass().addClass('ui-icon ui-icon-plusthick');
    }
    if ($('#btnGridEdit').length) // use this if you are using id to check
    {
        $("#btnGridEdit > span").removeClass().addClass('ui-icon ui-icon-wrench');
    }
    if ($('#btnGridDelete').length) // use this if you are using id to check
    {
        $("#btnGridDelete > span").removeClass().addClass('ui-icon ui-icon-trash');
    }
    if ($('.btnGridPlay').length) // use this if you are using id to check
    {
        $(".btnGridPlay > span").removeClass().addClass('ui-icon ui-icon-play');
    }

    $(".JS_OnlyNumber").keyup(function() {
        this.value = (this.value + '').replace(/[^0-9]/g, '');
    });

});

/*
 * Método que permite obtener el id de un grid
*/
function GetSelectedValueId(grid) {
    var entityGrid = grid.data("kendoGrid");
    var selectedItem = entityGrid.dataItem(entityGrid.select());
    if (selectedItem == null) return false;
    return selectedItem.Id;
}

/*
 * Método que permite obtener loa datos de un row de un grid
*/
function GetSelectedValue(grid) {
    var entityGrid = grid.data("kendoGrid");
    var selectedItem = entityGrid.dataItem(entityGrid.select());
    if (selectedItem == null) return false;
    return selectedItem;
}

/*Método que se ejecuta cuando se inicia la carga de datos del Grid*/
function onRequestStart(arg) {
    $.blockUI({
        message: '<h4>Espere por favor..</h4>'
    });
}

/*Método que se ejecuta cuando se termina la carga de datos del Grid*/
function onRequestEnd(arg) {
    $.unblockUI();
}

function onClose(e) {
    var windows = $("#window");
    windows.html('');
    $("#windowcontainer").append("<div id='window'></div>");
}