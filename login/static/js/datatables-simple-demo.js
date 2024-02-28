window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
    const datatables = document.getElementsByClassName('datatablesSimple');
    for (var i = 0; i <= datatables.length; i++){
        if (datatables[i]) {
            new simpleDatatables.DataTable(datatables[i]);
        }
    }
  
    
});


