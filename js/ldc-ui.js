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
	$("#share,.sshare,#shareMenuEntry").click(function(){
		DisplayShareDialog();
		var result = ldc.SerializeResult();	
		if (result != "")			
			$("#shareMyResult").val("http://distrochooser.de/?r=l&answers="+result);
		else
			$("#shareMyResult").val("http://distrochooser.de/?r=l");
	});
	$("#PersonalTextLink").val("http://distrochooser.de/?r=l");
	$("#PersonalTextLink,#shareMyResult").click(function(){
		$(this).select();
	})
	$("#contact,.scontact,#contactMenuEntry").mousedown(function(e){
		$("#modalImprint").modal();
		e.preventDefault();
	});
	$("#privacy,.sprivacy,#privacyMenuEntry").mousedown(function(e){
		$("#modalPrivacy").modal();
		e.preventDefault();
	});	
	$("#about").click(function(e){
		$.post( "./rest.php", { method: "GetInstalledDistros", args: "[]",lang: lang})
		.done(function( data ) {				
			var distros = $.parseJSON(data);
			$("#distros").empty();
			for (var i = 0; i < distros.length; i++) {
				$("#distros").append("<li><a href='"+distros[i].Homepage+"'>"+distros[i].Name+"</a></li>");
			};
		});			
		$.post( "./rest.php", { method: "GetTestCount", args: "[]",lang: lang})
		.done(function( data ) {				
			$("#modalAbout").modal();
			e.preventDefault();
			$("#tc").text($.parseJSON(data));
		});		
	});	
	
	$("#homelink").css("display","none");	
	$("#rightBar").css("display","none");	
	
});
