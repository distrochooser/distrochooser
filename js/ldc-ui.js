var ldc;
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,    
    function(m,key,value) {
      vars[key] = value;
    });
    return vars;
}
$(document).ready(function(){
	var lang = getUrlVars()["l"];
	var ref = getUrlVars()["r"];
	if (lang == null)
		lang = 1;
	if (ref == null)
		ref = "";
	$.post( "./rest.php", { method: "GetSystemVars", args: "[]",lang: lang})
	.done(function( data ) {		
		ldc = new LDC($.parseJSON(data),lang);
	});
});
