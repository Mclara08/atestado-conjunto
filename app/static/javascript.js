(function(win, doc){
    'use strict';

    //Verifica se o usuário quer deletar o atestado
    if(doc.querySelector('.btnDel')){
        let btnDel = doc.querySelectorAll('.btnDel');
        for(let i=0; i < btnDel.length; i++){
            btnDel[i].addEventListener('click', function(event){
                if(confirm('Deseja mesmo apagar este atestado?')){
                    return true;
                }else{
                    event.preventDefault();
                }
            });
        }
    }

})(window, document);