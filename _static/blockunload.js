var asciiF5 = 116;
var bcksp = 8;
var ctrl = 17;
var Rchar=82;
var bRet = true;
var formactive=0;
var ctrl_active=false;
if(document.all){
document.onkeydown = onKeyPress; document.onkeyup = onKeyUp; //document.onmousedown=onKeyPress;
}else if (document.layers || document.getElementById){
document.onkeypress = onKeyPress; document.onkeydown = onKeyPress; //document.onmousedown=onKeyPress;
document.onkeyup = onKeyUp;
}
document.oncontextmenu = new Function ("return false");
function onKeyPress(evt) {
window.status = '';
var oEvent = (window.event) ? window.event : evt;

var nKeyCode = oEvent.keyCode ? oEvent.keyCode :
oEvent.which ? oEvent.which :
void 0;
var bIsFunctionKey = false;
// console.log("keypress, key=",nKeyCode)
if(nKeyCode == ctrl) ctrl_active=true;
if(oEvent.charCode == null || oEvent.charCode == 0){
//alert(oEvent.keyCode);
bIsFunctionKey = (nKeyCode == asciiF5 || (ctrl_active && nKeyCode == Rchar && formactive==0))
}
// alert(oEvent.charCode+"\r\n"+nKeyCode);
if(bIsFunctionKey){
bRet = false;
try{
//oEvent.returnValue = false;
oEvent.cancelBubble = true;

if(document.all){ //IE
oEvent.keyCode = 0;
}else{ //NS
oEvent.preventDefault();
oEvent.stopPropagation();
}
}catch(ex){
//alert(ex);
}
return bRet;
}

}
function onKeyUp(evt) {
	window.status = '';
	var oEvent = (window.event) ? window.event : evt;

	var nKeyCode = oEvent.keyCode ? oEvent.keyCode :
	oEvent.which ? oEvent.which :
	void 0;
	var bIsFunctionKey = false;
	if(oEvent.charCode == null || oEvent.charCode == 0){
	//alert(oEvent.keyCode);
		// console.log("keyup, key=",nKeyCode)
		if(nKeyCode == ctrl) ctrl_active=false;
	}
}


function activeform(x) {formactive=x}


window.correctlyFinished=false;
window.addEventListener('beforeunload', function (e) {
  window.QuittingWindow=true;
  if(!window.correctlyFinished) {
      e.preventDefault();
      var confirmationMessage = "\o/";
      e.returnValue = confirmationMessage;
      return confirmationMessage;
  }
  else delete e['returnValue'];
});
document.forms[0].onsubmit=function() {window.correctlyFinished=true;}