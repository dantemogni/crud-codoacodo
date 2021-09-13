/* scripts */

$('#modalDelete').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var id = button.data('id'); // Extract info from data-* attributes
    var name = button.data('name');
    var surname = button.data('surname');
    var modal = $(this);

    modal.find('.modal-title').text('Borrar empleado #' + id);
    modal.find('#delete-name').text(name + ' ' + surname);
    modal.find('#del-btn').attr("href", '/destroy/'+id);
  })