function buscaExpande(){
      if ($('#campoBusca').hasClass('buscaExpande')){
          $('#campoBusca').removeClass('buscaExpande');
          $('#campoBusca').addClass('buscaEsconde')
      }else{
         $('#campoBusca').addClass('buscaExpande');
         $('#campoBusca').removeClass('buscaEsconde')
      }
}

function menuAparece() {
    if ($('#menuLateral').hasClass('menuSome')) {
        $('#menuLateral').removeClass('menuSome');
        $('#menuLateral').addClass('menuAparece')
    }else{
        $('#menuLateral').addClass('menuSome');
        $('#menuLateral').removeClass('menuAparece')
    }
}
