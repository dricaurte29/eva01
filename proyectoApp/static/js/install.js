'use strict';

let deferredInstallPrompt = null;
const installButton = document.getElementById('instal');
installButton.addEventListener('click', installPWA);

function installPWA(evt){
    deferredInstallPrompt.prompt();
    
}