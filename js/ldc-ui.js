var ldc;
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,    
    function(m,key,value) {
      vars[key] = value;
    });
    return vars;
}
function DisplayShareDialog(){
	$("#shareDialogContent .fa,.socialicons, #shareDialogContent a").each(function(index, value) { 	   
	    $(this).removeAttr("style");
	    $(this).attr("style","display: initial !important;");
	});
	$("#shareDialog").modal();
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
	$.post( "./rest.php", { method: "NewVisitor", args: "\""+document.referrer+"\"",lang: lang});
	$("#share").click(function(){
		DisplayShareDialog();
	});
	$("#homelink").css("display","none");	

});
