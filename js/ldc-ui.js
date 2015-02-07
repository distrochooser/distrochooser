var ldc;

$(document).ready(function(){
	$.post( "./rest.php", { method: "GetSystemVars", args: "[]",lang: "2" })
	.done(function( data ) {		
		ldc = new LDC($.parseJSON(data),1);
	});
});
