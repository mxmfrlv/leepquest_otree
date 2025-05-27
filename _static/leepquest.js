if(allvars.length==1 && allvars[0]=="") allvars=[];
var varsanswered = Array(allvars.length).fill(0);
var varsshown = Array(allvars.length).fill(0);
var sliderpresent=(slidervars.length>0 && slidervars[0]!='');
var nqanswered=0;
var waitnext_timer_handler;
var screen_listing=false;
var need_confirm_empty_optional=false, empty_optional_confirmed=false;
var starttime;

var prev_button_clicked=false, next_button_clicked=false;

if(window.bys === undefined && by >0) window.bys = Array(allvars.length/by).fill(by);
// console.log(allvars);
function bindSliderUpdate(slider,sl,starthidden,cdecimals) {
	//console.log(slider,sl,starthidden,cdecimals);
	slider.noUiSlider.on('update', function (values, handle) {
		if(document.getElementById("slidershown_"+slidervars[sl]).value == 0) {
			document.getElementById("slidershown_"+slidervars[sl]).value=1;
			$("#slider_"+slidervars[sl]+" .noUi-tooltip").hide();
			if(starthidden) $("#slider_"+slidervars[sl]+" .noUi-handle").hide();
		}
		else {
		 var resultval=values[handle]; if(cdecimals==0) resultval=Math.round(resultval);
		 $("#sliderinput_"+slidervars[sl]).val(resultval).change();
		 //additional_onchange(slidervars[sl]);
		 if(js_vars.fixedsum_sliders !== undefined) {
			 var my_i=-1; var my_vars=[];
			 for(var i in js_vars.fixedsum_sliders) {
				if(i%2 == 0) {
					var clist=js_vars.fixedsum_sliders[i];
					if(!$.isArray(clist)) clist=split(',');
					if(clist.length == 1) clist=clist[0].split(';');
					if(clist.indexOf(slidervars[sl])>-1) {
						my_i=i; my_vars=clist; break;
					}
				}
			 }
			 if(my_i>-1 && js_vars.fixedsum_sliders.length>my_i) {
				var my_sum=js_vars.fixedsum_sliders[Number(my_i)+1];
				my_residual=my_sum-resultval;
				var other_vars=[];
				for(var h in my_vars) if(my_vars[h]!=slidervars[sl]) other_vars.push(my_vars[h]);
				if(other_vars.length==1) {
					var other_slider=document.getElementById("slider_"+other_vars[0]);
					// console.log(other_slider.noUiSlider.get(),(other_slider.noUiSlider.get()!=my_residual), resultval,my_sum,my_residual,my_i,js_vars.fixedsum_sliders,(Number(my_i)+1),js_vars.fixedsum_sliders[my_i+1]);
					if(other_slider.noUiSlider.get()!=my_residual) other_slider.noUiSlider.set(my_residual);
				}
			 }
		 }
		 if(starthidden && !$("#slider_"+slidervars[sl]+" .noUi-handle").is(':visible')) {
			var appspeed=(sliderbeh=="span")?0:300;
			$("#slider_"+slidervars[sl]+" .noUi-handle").show(appspeed);
			// console.log("should show "+"#field_"+slidervars[sl],slidervars,sl,handle,event, event.target);
			if (sliderbeh=="span") slider.noUiSlider.updateOptions({
				behaviour: 'tap',
			});
			// console.log('updated');
		 }
		 $("#slider_"+slidervars[sl]+" .noUi-tooltip").show();
		}
	});
}
additional_onchange=function(varname){};
function bindOnChangeForTime(field) {
	if(field === null) return;
	// console.log(field.name,field.type);
	field.onchange=function() {
		var timenow_ch=(new Date()).getTime();
		if(document.getElementById(field.name+"_time")!==null) $("#"+field.name+"_time").val((timenow_ch-starttime)/1000);
		if(document.getElementById(field.name+"_errormessage")!==null) $("#"+field.name+"_errormessage").hide();
		additional_onchange(field.name);
		// console.log("field.name: ",field.name, field.value);
		// console.log("starttime:",starttime,"timenow: ",timenow_ch,"field.name: ",field.name, $("#"+field.name+"_time").val());
	}
}
///dependencies
function dependfunc(depended,dependon,depvals,inv) {
	// console.log(document.forms[0][dependon].value,',by='+by,dependon,depended,depvals,inv);
	var negform=false;
	if(depvals.substr(0,1)=='!') {
		negform=true; depvals=depvals.substr(1);
	}
	var adepvals=depvals.split(',');
	var depok=negform;
	for(var i=0; i<adepvals.length; i++) {
		if(adepvals[i]==document.forms[0][dependon].value || (document.forms[0][dependon].type=="checkbox" && document.forms[0][dependon].checked)) depok=!negform;
		// console.log("dependon;",dependon,"value",document.forms[0][dependon].value,"check_equals_to",adepvals[i],"depended:",depended,"depended elem:",document.forms[0][depended],"dependon elem:",document.forms[0][dependon]);
	}
	if(depok) {
		if(document.getElementById(depended+'_errormessage') == null) {
			$( '<div class="alert-warning" style="display:none" title="required" id="'+depended+'_errormessage">'+js_vars.lq_lexicon.please_answer_question+'</div>' ).insertBefore( $( '#field_'+depended+'_number_placeholder' ) );
			// console.log(depended,$( '#field_'+depended+'_number_placeholder' ),$('#'+depended+'_errormessage'));
		}
		document.getElementById(depended+'_errormessage').title="required"; //$('#'+depended+'_errormessage').attr("title","required");
		// console.log(typeof document.forms[0][depended].checkValidity)
		if(typeof document.forms[0][depended].checkValidity === 'function' && document.forms[0][depended].type !="checkbox") {
			$('#id_'+depended).prop('required',true);
			//document.forms[0][depended].setCustomValidity(js_vars.lq_lexicon.please_answer_question);
			// console.log('set '+'#id_'+depended+' required');
		}
		// console.log('inserted','by='+by);
		if(inv){
			var imshown=false;
			for(i=0; i<varsshown.length; i++) if(varsshown[i]>0 && allvars[i]==depended) imshown=true;
			$('#field_'+depended).off('show');
			// console.log('off show for '+'#field_'+depended);
			if(imshown) $('#field_'+depended).show();
		}
	}
	if(!depok) {
		// console.log("!depok",document.getElementById(depended+'_errormessage'),"required before:",$('#id_'+depended).prop('required'));
		if(document.getElementById(depended+'_errormessage') != null) {
			document.getElementById(depended+'_errormessage').title=""; 
			$("#"+depended+"_errormessage").hide()
			// if(document.forms[0][depended].checkValidity === 'function') document.forms[0][depended].setCustomValidity("");
			//$('#'+depended+'_errormessage').attr("title","");
			$('#id_'+depended).prop('required',false);
		}
		if(inv) {
			// console.log("invisible, by="+by);
			var imshown=false;
			for(i=0; i<varsshown.length; i++) if(varsshown[i]>0 && allvars[i]==depended) imshown=true;
			if(!imshown) {
				$('#field_'+depended).off('show');
				// console.log('off show for '+'#field_'+depended+' creating new show event');
				$('#field_'+depended).on('show', {depended:depended}, function(event) {
					setTimeout(function() {
						if(by == 1) $(".otree-btn-next").click();
						else $('#field_'+event.data.depended).hide();
					},50);
								
				});
			}
			if(imshown) $('#field_'+depended).hide();
			if(document.forms[0][depended].type == "text") document.forms[0][depended].value="";
			
		}
		// console.log("required after:",$('#id_'+depended).prop('required'));
	}
}
function applydependencies(){
		for(var i=0; i<deps.length; i++) {
			// console.log(deps[i]);
			var depselems=deps[i].split(':');
			var depended=depselems[0].replace(/\s+/g,"");
			var dependon=(depselems.length>1)?depselems[1].replace(/\s+/g,""):"";
			var depvals='1'
			if(depselems.length>2) depvals=depselems[2];
			var inv=false;
			if(depselems.length>3 && depselems[3].substr(0,3).toLowerCase()=="inv") inv=true;
			$('#field_'+dependon).on('change', {depended:depended,dependon:dependon,depvals:depvals,inv:inv}, function(event) {
				setTimeout("dependfunc('"+event.data.depended+"','"+event.data.dependon+"','"+event.data.depvals+"',"+(event.data.inv?'true':'false')+")",50);		  
			});
			$('#id_'+depended).on('keyup', function(event) {
				// console.log(this); 
				$(this).trigger("change");
			});
			if(inv){
				// console.log('inv field_'+depended, "by="+by); 
				var imshown=false;
				for(i2=0; i2<varsshown.length; i2++)  {
					// console.log(i2,varsshown[i2],allvars[i2]); 
					if(varsshown[i2]>0 && allvars[i2]==depended) imshown=true;
				}
				// console.log('inv field_'+depended, "by="+by, "imshown=",imshown);
				if(imshown) setTimeout(hideField.bind(null,depended),50);
				else $('#field_'+depended).on('show', {depended:depended,dependon:dependon}, function(event) {
				setTimeout(function() {
					if(by == 1) $(".otree-btn-next").click();
					else {
						$('#field_'+event.data.depended).hide();
					}
				},50);
				});
				if((imshown || by != 1) && document.forms[0][dependon].value) setTimeout("dependfunc('"+depended+"','"+dependon+"','"+depvals+"',true)",50);
			}
		}
}
function hideField(f){
	$('#field_'+f).hide(); 
	// console.log($('#field_'+f), '#field_'+f+' hidden');
}
///dependencies end
function liveRecv(data) {
	var command=data.substr(0,data.search(/[|]/));
	// console.log('received message, command=',command, "data=", data, data.search(/[|]/));
	if(command.toLowerCase() == "ok" || command.toLowerCase() == "apply" ) {
		$("#blocpage_content").css("visibility","visible"); $("#control_buttons").show(); $("#pleasewait").hide();
		var ctime=(new Date()).getTime();
		if(js_vars.loadtimevar !== undefined) {
			var loadtime=(ctime-starttime)/1000;
			var input_loadtime=document.createElement("input");
			input_loadtime.type="hidden"; input_loadtime.value=loadtime;
			input_loadtime.name=js_vars.loadtimevar;
			input_loadtime.id="blocpage_loadtime";
			$("form").append(input_loadtime);
			// console.log(js_vars.loadtimevar,":",loadtime,input_loadtime);
		}
		starttime=ctime;
		
		prev_button_clicked=false; next_button_clicked=false;

	}
	if(command.toLowerCase() == "ok") {
		if(js_vars.min_times != undefined) {
			var cmintime=js_vars.min_times[0];
			if(cmintime < -1) cmintime=Math.abs(cmintime)-1;
			if(cmintime > 0) {
				$("#control_buttons").hide(); $("#waitnext_text").show(); waitnext_timer_handler=setTimeout(function(){$("#waitnext_text").hide(); $("#control_buttons").show(); }, cmintime*1000)
			}
		}
		if(typeof deps !== 'undefined') applydependencies();
	}
	if(command.toLowerCase() == 'apply') {
		$("#blocpage_content").css("visibility","visible");  $("#pleasewait").hide();
		var datareceived=data.substr(data.search(/[|]/)+1).split('|');
		for(var di in datareceived) {
			var cdata=datareceived[di].split(';');
			if(document.forms[0][cdata[0]] !== undefined && cdata.length>1) {
				document.forms[0][cdata[0]].value=cdata[1];
				if(document.forms[0][cdata[0]].type !== undefined) {
					if(document.forms[0][cdata[0]].type == "checkbox") document.forms[0][cdata[0]].checked = !!parseInt(cdata[1]);
				}
				// console.log(cdata[0],":",document.forms[0][cdata[0]].value, document.forms[0][cdata[0]].type);
			}
			else if(cdata.length>2){
				var input_screentime=document.createElement("input");
				input_screentime.type="hidden"; input_screentime.value=cdata[1];
				input_screentime.name=cdata[0];
				input_screentime.id=cdata[2];
				$("form").append(input_screentime);
				// console.log(input_screentime.id,input_screentime.value);
			}
			if(cdata.length==1) {
				var cbundle=cdata[0].split(":");
				if(cbundle.length==3 && cbundle[0]=="nscr") {
					var delay=0;
					for(var s=1; s<=parseInt(cbundle[1]); s++) {
						screen_listing=true;
						$(".otree-btn-next").delay(delay).trigger('click',[true]);
						delay+=10;
					}
					if(typeof deps !== 'undefined' && deps !='') { applydependencies();} //setTimeout(applydependencies,delay);
					screen_listing=false;
					starttime=parseInt(cbundle[2]);
					if(js_vars.min_times != undefined) {
						var cmintime=(js_vars.min_times.length>cbundle[1])?js_vars.min_times[cbundle[1]]:js_vars.min_times[js_vars.min_times.length-1];
						if(cmintime < -1) cmintime=Math.abs(cmintime)-1;
						if(cmintime > 0) {
							$("#control_buttons").hide(); $("#waitnext_text").show(); clearTimeout(waitnext_timer_handler); waitnext_timer_handler=setTimeout(function(){$("#waitnext_text").hide(); $("#control_buttons").show(); }, cmintime*1000)
						}
						else {
							clearTimeout(waitnext_timer_handler); $("#control_buttons").show(); $("#waitnext_text").hide();
						}
					}
				}
			}
		}
	}
	if(command.toLowerCase() == 'custom' && typeof customLiveRecv === "function") {
		var customdatareceived=data.substr(data.search(/[|]/)+1)
		customLiveRecv(customdatareceived);
	}
}
var additional_validate=function(varname){
	return true;
};
var additional_validate_message=(js_vars.additional_validate_message === undefined)?js_vars.lq_lexicon.please_correct_errors:js_vars.additional_validate_message;
var additional_validate_invalid_action=function(varnames,alertneeded){
	// console.log(varnames);
	if(alertneeded === undefined) alertneeded=false;
	for(var i=0; i<varnames.length; i++) {
		$('label[for="id_'+varnames[i]+'"]').css({'color':'red'});
		// console.log(i,$('label[for="id_'+varnames[i]+'"]'));
	}
	if(alertneeded) alert(additional_validate_message);
};

var alertModalDivActive=false;
var alert_sup_action=function(){};
function alertModal(message,callback) {
	if(callback == undefined) callback=function(){};
	var alertModalDiv = new bootstrap.Modal(document.getElementById('alertModal'), {'keyboard':false, 'backdrop':'static'});
    var newMessage = message.toString().replace(/(?:\r\n|\r|\n)/g, "<br>");
	$("#alert_body").html(newMessage);
	alertModalDiv.toggle();
	alertModalDivActive=true;
	$('#alert_ok').on("click", function() {
		callback();
		$('#alert_ok').off("click");
		alertModalDivActive=false;
		alert_sup_action();
		alert_sup_action=function(){};
	});

}
var confirmModalDivActive=false;
var confirm_sup_action=function(){};
function confirmModal(message, callback) {
	// console.log("confirmModal_start");
    var confirmIndex = true;

    var newMessage = message.replace(/(?:\r\n|\r|\n)/g, "<br>");
    $('#modal_confirm_dialog_body').html("" + newMessage + "");
	//if(confirmModalDivActive) {console.log('already active'); $('#confirm_cancle').click(); $('#modal_confirm_dialog').modal('hide'); return;}
	console.log(confirmModalDivActive);
	var backdrop='static';
	//if(confirmModalDivActive) $('#modal_confirm_dialog').modal('hide');
	var confirmModalDiv = new bootstrap.Modal(document.getElementById('modal_confirm_dialog'), {'keyboard':false, 'backdrop':backdrop});
    //$('#modal_confirm_dialog').modal('show');
	confirmModalDiv.toggle();
	confirmModalDivActive=true;
	console.log($('#modal_confirm_dialog'))
    $('#confirm_cancle').on("click", function() {
		$('#confirm_cancle').off("click");
		confirmModalDivActive=false;
        if(confirmIndex) {
            confirmIndex = false;
            $('#modal_confirm_dialog').modal('hide');
			callback(false);
			confirm_sup_action();
			confirm_sup_action=function(){};
        }
    });

    $('#confirm_ok').on("click", function() {
		$('#confirm_ok').off("click");
		confirmModalDivActive=false;
        if(confirmIndex) {
            confirmIndex = false;
            $('#modal_confirm_dialog').modal('hide');
            callback(true);
			confirm_sup_action();
			confirm_sup_action=function(){};
        }
    });
	// console.log("confirmModal_end");
}


$(document).ready(function() {
$(".replacelinebreaks").each(function(){$( this ).html($( this ).html().replace(/#line#/g,"<br>"));});
$(function () {
	$('[data-toggle="tooltip"]').tooltip();
	$('[data-toggle="tooltip"]').each(function(){
		var ctitle=$( this ).attr('data-bs-original-title'), ctitle_clean=$( ctitle ).text();
		// console.log(ctitle, ctitle_clean);
		$( this ).attr('title',ctitle_clean); $( this ).attr('data-bs-original-title',ctitle_clean); $( this ).attr('area-label',ctitle_clean);
	});
});
$.each(['show', 'hide'], function (i, ev) { // adding show and hide events
		// console.log("each, event",ev,"i",i);
	    var el = $.fn[ev];
	    $.fn[ev] = function () {
			// console.log("inside show or hide, event",ev,"i",i);
	      this.trigger(ev);
	      return el.apply(this, arguments);
	    };
});
if(js_vars.bys_intro != undefined && js_vars.bys_intro[0] != "" ) $("#initial_presentation").html("<h5>"+js_vars.bys_intro[0]+"<br><br></h5>");
if(js_vars.prev_buttons != undefined && js_vars.prev_buttons[0] != 0 ) $("#prevbutton").show();
if(js_vars.min_times != undefined) {
	var cmintime=js_vars.min_times[0];
	if(cmintime < -1) cmintime=Math.abs(cmintime)-1;
	if(cmintime > 0) {
		$("#control_buttons").hide(); //$("#waitnext_text").show(); // in liveRecv()
	}
}
if(js_vars.randomorders != undefined && js_vars.firstrandoms != undefined && js_vars.randomorders.length != 0) {
	for(var q in js_vars.randomorders) {
		for(var o in js_vars.randomorders[q]) {
			if(document.getElementById("table_"+js_vars.firstrandoms[q]) === null) 
				$("#field_"+js_vars.randomorders[q][o]).insertBefore("#beforefield_"+js_vars.firstrandoms[q]);
			else {
				var celem=$("#tr_"+js_vars.randomorders[q][o])[0];
				// console.log(celem);
				$("#table_"+js_vars.firstrandoms[q]).append(celem);
				// console.log($("#table_"+js_vars.firstrandoms[q]).html());
			}
			var orderInput = document.createElement("input");
			orderInput.type="hidden"; orderInput.value=(parseInt(o)+1).toString();
			orderInput.name=js_vars.randomorders[q][o]+"_order";
			$("form").append(orderInput);
			if(js_vars.shownumbers != undefined && js_vars.shownumbers.length>q && parseInt(js_vars.shownumbers[q])) {
				var cnumber=parseInt(o)+1;
				var csnumber=cnumber.toString()+".&nbsp;";
				if(cnumber<10) csnumber="&nbsp;"+csnumber;
				$("#field_"+js_vars.randomorders[q][o]+"_number_placeholder").html(csnumber);
			}
		}
	}
}
else if(js_vars.shownumbers != undefined && js_vars.shownumbers.length != 0) {
	for(var iav in allvars) {
		//console.log(iav,js_vars.shownumbers.length,js_vars.shownumbers[iav])
		if(js_vars.shownumbers.length>iav && parseInt(js_vars.shownumbers[iav])) {
			var cnumber=parseInt(iav)+1;
			var csnumber=cnumber.toString()+".&nbsp;";
			if(cnumber<10) csnumber="&nbsp;"+csnumber;
			$("#field_"+allvars[iav]+"_number_placeholder").html(csnumber);
			$("#field_"+allvars[iav]+"_number_placeholder").parent().find('label').html($("#field_"+allvars[iav]+"_number_placeholder").parent().find('label').html().replace(' ?','&nbsp;?'));
			$("#field_"+allvars[iav]+"_number_placeholder").parent().find('label').prepend($("#field_"+allvars[iav]+"_number_placeholder"));
		}
	}
}
// console.log(js_vars.shownumbers,js_vars.randomorders,js_vars.firstrandoms,js_vars.shownumbers != undefined);
if(document.getElementById("initial_presentation") !== null) $([document.documentElement, document.body]).animate({
	scrollTop: (js_vars.bys_intro != undefined && js_vars.bys_intro[0] != "" )? $("#initial_presentation").offset().top : 0
}, 10);
for(var si=0; si<Math.max(window.bys.length,allvars.length); si++) {$(".initial_presentation_"+(parseInt(si)+1).toString()).hide(); $(".not_initial_presentation_"+(parseInt(si)+1).toString()).show(); if(document.getElementById("initial_presentation_"+(parseInt(si)+1).toString()) !== null) $("#initial_presentation_"+(parseInt(si)+1).toString()).hide();}
$(".initial_presentation_1").show(); $(".not_initial_presentation_1").hide(); if(document.getElementById("initial_presentation_1") !== null) $("#initial_presentation_1").show();

starttime=(new Date()).getTime();
for(var ff in document.forms[0]) {
	if( document.forms[0][ff] !== null) {
		var cfield=document.forms[0][ff];
		if(cfield.name != undefined && allvars.indexOf(cfield.name)>-1) bindOnChangeForTime(cfield);
	}
}
// console.log(by, allvars, bys);
if(by>0) {
	
	for(var iav in allvars) $("#field_"+allvars[iav]).hide();
	// for(var iav in allvars) $("#field_"+allvars[iav]+"_time").hide();
	for(var i=0; i<by; i++) { $("#field_"+allvars[i]).show(); varsshown[i]=1;}
}
if(sliderpresent) {
 for(var sl in slidervars) {
	var slider = document.getElementById("slider_"+slidervars[sl]);
	// console.log(slider, slidervars[sl]);
	var starthidden=false;
	var copts=slideropts[sl].split(':');
	var cmaxval=100, cminval=0, cstep=1;
	if(copts.length>0 && copts[0].replace(/\s+/g,"")!='') cmaxval=parseFloat(copts[0]);
	if(copts.length>1 && copts[1].replace(/\s+/g,"")!='') cminval=parseFloat(copts[1]);
	if(copts.length>2 && copts[2].replace(/\s+/g,"")!='') cstep=parseFloat(copts[2]);
	if(cminval>cmaxval) {var cminval_old=cminval; cminval=cmaxval; cmaxval=cminval_old;}
	var cstart=(cmaxval+cminval)/2;
	if(copts.length>3) {
		if(copts[3].toLowerCase().substr(0,3)=="inv") {
			starthidden=true;
			cstart=cminval;
			var last4=copts[3].toLowerCase().substr(-4).replace(/\s+/g,"");
			if(last4==",min") cstart=cminval;
			if(last4==",max") cstart=cmaxval;
			if(last4==",mid" || last4==",avg") cstart=(cmaxval+cminval)/2;
		}
		else cstart=parseFloat(copts[3]);
	}
	if(typeof js_vars.slider_starts == 'object') {
		if(typeof js_vars.slider_starts[slidervars[sl]] !== 'undefined') {
			cstart=parseFloat(js_vars.slider_starts[slidervars[sl]]);
		}
	}
	var pref='',suff='';
	if(copts.length>4) {
		var aps=copts[4].split('/');
		if(aps.length==1) suff=aps[0];
		if(aps.length>1) {pref=aps[0]; suff=aps[1];}
	}
	if(copts.length>5) {
		var leftright=copts[5].split('/');
		document.getElementById("sliderleft_"+slidervars[sl]).innerHTML=leftright[0].replace(/_/g,"&nbsp;");
		document.getElementById("sliderleft_"+slidervars[sl]).style.marginRight="16px";
		if(leftright.length>1) {
			document.getElementById("sliderright_"+slidervars[sl]).innerHTML=leftright[1].replace(/_/g,"&nbsp;");
			document.getElementById("sliderright_"+slidervars[sl]).style.marginLeft="16px";
		}
	}
	if(starthidden) document.getElementById("sliderhint_"+slidervars[sl]).innerHTML=js_vars.lq_lexicon.click_grey_field_to_answer;
	var cdecimals=0; if(cstep>0 && cstep<1) cdecimals=cstep.toString().length-2;
	sliderbeh='tap'; //starthidden?'snap':'tap';
	var uipips={
			mode: 'range',
			stepped: true,
			format: wNumb({decimals: cdecimals, prefix:pref, suffix:suff}),
	}
	if(verticalsliders.indexOf(slidervars[sl])>-1 || copts.length>6) {
		uipips['mode']=(verticalsliders.indexOf(slidervars[sl])>-1)?'values':'range';
		uipips['density']=5;
		uipips['values']=[0,10,20,30,40,50,60,70,80,90,100];
		if(copts.length>6) {
			var valdens=copts[6].split('/');
			uipips['values']=valdens[0].split(',');
			if(valdens.length>1) uipips['density']=valdens[1];			
		}
	}
	var cslideroptions={
		start:cstart,
		range: {
			'min': cminval,
			'max': cmaxval,
		},
		step:cstep,
		tooltips: wNumb({decimals: cdecimals, prefix:pref, suffix:suff}),
		
		// Show a scale with the slider
		pips: uipips,
		behaviour: sliderbeh
	}
	if(verticalsliders.indexOf(slidervars[sl])>-1) {
		cslideroptions['orientation']='vertical';
		cslideroptions['direction']='rtl';

	}
	else if(copts.length>6) {
		
		for(const vi in uipips['values']) {
			if(uipips['values'][vi] >= cminval && uipips['values'][vi] <= cmaxval) {
				const cperc = (uipips['values'][vi] - cminval)/(cmaxval-cminval)
				cslideroptions.range[Math.round(cperc*100).toString()+'%']=[parseFloat(uipips['values'][vi])];
			}
		}
	}
	// console.log(cslideroptions.pips, cslideroptions.range)
	noUiSlider.create(slider, cslideroptions);
	if(readonlysliders.indexOf(slidervars[sl])>-1) {
		slider.noUiSlider.disable(0);
		$("#slider_"+slidervars[sl]+" .noUi-tooltip").show();
		if(!starthidden) document.forms[0][slidervars[sl]].value = cstart;
		additional_onchange(slidervars[sl])
	}
	else bindSliderUpdate(slider,sl,starthidden,cdecimals);
 }
}

$(".otree-btn-next").click(function(e,a_sup_param){
	// console.log("otree-btn-next");
	prev_button_clicked=false; next_button_clicked=true; need_confirm_empty_optional = false;
	if(by>0 && allvars.length>0) {
		var nanswnow=0, nanswtot=0, bynow=0;
		var force_prevent_default=false;
		var invalidated_vars=[];
		for(i=0; i<varsshown.length; i++) if(varsshown[i]>0 && allvars[i]!="") {
			bynow++;
			var errormessage=false;
			var iamoptional=document.getElementById(allvars[i]+"_validator") !== null && (document.getElementById(allvars[i]+"_validator").value.replace(/Optional/,"")!=document.getElementById(allvars[i]+"_validator").value);
			iamoptional ||= js_vars.optional_vars.indexOf(allvars[i])>=0;
			// console.log("iamoptional =",iamoptional,document.getElementById(allvars[i]+"_validator"))
			// alert(allvars[i]+"_errormessage,"+document.getElementById(allvars[i]+"_errormessage")+","+iamoptional.toString());
			if(iamoptional && document.getElementById(allvars[i]+"_errormessage") !== null) {
				if(document.getElementById(allvars[i]+"_errormessage").title == 'required') { iamoptional=false; errormessage=true;}
				// alert(document.getElementById(allvars[i]+"_errormessage").title+"\r\n"+document.getElementById(allvars[i]+"_errormessage").outerHTML+"\r\n"+$(allvars[i]+"_errormessage").attr("title"));
			}
			if(allvars[i]=="__info__") iamoptional=true;
			// console.log("allvars[i]=",allvars[i], "iamoptional=", iamoptional);
			var ok_pass=(document.forms[0][allvars[i]] !== undefined || allvars[i]=="__info__") && (iamoptional || (document.forms[0][allvars[i]].value!="" && typeof document.forms[0][allvars[i]].checkValidity !== 'function') || (document.forms[0][allvars[i]].value !== "" && typeof document.forms[0][allvars[i]].checkValidity === 'function' && document.forms[0][allvars[i]].checkValidity()));
			// console.log("i=",i,"allvars[i]=",allvars[i],"ok_pass=",ok_pass,"document.forms[0][allvars[i]]=",document.forms[0][allvars[i]],"typeof checkValidity ",typeof document.forms[0][allvars[i]].checkValidity,"iamoptional=",iamoptional,document.getElementById(allvars[i]+"_validator").value); console.log(allvars[i],"checkValidity",((typeof document.forms[0][allvars[i]].checkValidity === 'function')?document.forms[0][allvars[i]].checkValidity():"not a function"),"required:",$('#id_'+allvars[i]).prop('required')); if(typeof document.forms[0][allvars[i]].checkValidity === 'function') console.log("checkValidity:",document.forms[0][allvars[i]].checkValidity(),document.forms[0][allvars[i]].checkValidity);
			if(ok_pass && (!additional_validate(allvars[i]) || (!iamoptional && document.forms[0][allvars[i]].value=="" && $('#id_'+allvars[i]).prop('required')))) { // && slidervars.indexOf(allvars[i])>-1
				force_prevent_default=true;
				if(!additional_validate(allvars[i]) || slidervars.indexOf(allvars[i])<0) invalidated_vars.push(allvars[i]);
				ok_pass=false;
			}
			if(ok_pass && iamoptional && allvars[i]!="__info__" && document.forms[0][allvars[i]].value=="" && js_vars.confirm_blank[i] && !empty_optional_confirmed) {
				force_prevent_default=true;
				ok_pass=false;
				need_confirm_empty_optional=true;
			}
			// console.log(ok_pass,need_confirm_empty_optional,js_vars.confirm_blank[i],js_vars.confirm_blank)
			if(ok_pass) {
				varsanswered[i] = 1;
				nanswnow++;
			}
		}
		if(invalidated_vars.length>0) {
			additional_validate_invalid_action(invalidated_vars);
		}
		// console.log("bynow=",bynow, "nanswnow=", nanswnow);
		if(nanswnow == bynow) {
			nanswtot=0;
			var timenow=(new Date()).getTime();
			for(var i=0; i<varsanswered.length; i++) if(varsanswered[i]>0) {
				if(varsshown[i]>0) {
					$("#field_"+allvars[i]).hide();
					if($("#"+allvars[i]+"_time").val()==0) $("#"+allvars[i]+"_time").val((timenow-starttime)/1000);
				}
				varsshown[i] = 0;
				nanswtot++;
			}
			if(js_vars.hide_initial!=undefined && js_vars.hide_initial && nanswnow>0) $("#initial_presentation").hide();
			var finished_screen_number=1, last_screen_number=allvars.length/by;
			if(window.bys !== undefined && bys.length>1) {
				var cbindex=0, cbsum=0;
				for(var b=0; b<bys.length; b++) {
					cbsum+=parseInt(bys[b]);
					if(cbsum<=nanswtot) cbindex++;
				}
				finished_screen_number=cbindex; last_screen_number=bys.length;
				if(cbindex+1>bys.length) {last_screen_number = cbindex+1; cbindex=bys.length-1;}
				by=parseInt(bys[cbindex]);
				if(js_vars.bys_intro != undefined && js_vars.bys_intro.length>cbindex) {
					// console.log("-"+js_vars.bys_intro[cbindex]+"-");
					var new_presentation_content=js_vars.bys_intro[cbindex];
					if (js_vars.bys_intro[cbindex] != "") new_presentation_content = "<h5>"+js_vars.bys_intro[cbindex]+"<br><br></h5>";
					$("#initial_presentation").html(new_presentation_content);
				}
				if(js_vars.prev_buttons != undefined) {
					var cprevbutshow=(js_vars.prev_buttons.length>cbindex)?js_vars.prev_buttons[cbindex]:js_vars.prev_buttons[js_vars.prev_buttons.length-1];
					if(cprevbutshow != 0) {
						$("#prevbutton").show();
						if(cbindex>0) $("#prevbutton").prop("disabled",false);
					}
					else {$("#prevbutton").hide();}
				}
				for(var si=0; si<Math.max(window.bys.length,allvars.length); si++) {$(".initial_presentation_"+(parseInt(si)+1).toString()).hide(); $(".not_initial_presentation_"+(parseInt(si)+1).toString()).show(); if(document.getElementById("initial_presentation_"+(parseInt(si)+1).toString()) !== null) $("#initial_presentation_"+(parseInt(si)+1).toString()).hide();}
				$((".initial_presentation_"+(parseInt(cbindex)+1).toString())).show(); $((".not_initial_presentation_"+(parseInt(cbindex)+1).toString())).hide(); if(document.getElementById("initial_presentation_"+(parseInt(cbindex)+1).toString()) !== null) $(("#initial_presentation_"+(parseInt(cbindex)+1).toString())).show();
				// console.log("by=",by,"cbindex=",cbindex,"bys=",bys, "js_vars.bys_intro=", js_vars.bys_intro, $("#initial_presentation").html());
			}
			// console.log(js_vars.screentime_prefix,finished_screen_number,$("#screen"+finished_screen_number+"_time"),(document.getElementById("screen"+finished_screen_number+"_time") === null) );
			no_scroll=false;
			if(js_vars.min_times != undefined && (typeof a_sup_param === 'undefined' || a_sup_param === false)) {
				var cmintime=(js_vars.min_times.length>finished_screen_number)?js_vars.min_times[finished_screen_number]:js_vars.min_times[js_vars.min_times.length-1];
				if(cmintime < -1) {
					no_scroll=true;
					cmintime=Math.abs(cmintime)-1;
				}
				if(cmintime > 0) {
					$("#control_buttons").hide(); $("#waitnext_text").show(); clearTimeout(waitnext_timer_handler); waitnext_timer_handler=setTimeout(function(){$("#waitnext_text").hide(); $("#control_buttons").show(); }, cmintime*1000)
				}
				else {
					clearTimeout(waitnext_timer_handler); $("#control_buttons").show(); $("#waitnext_text").hide();
				}
			}
			if(js_vars.screentime_prefix != undefined && document.getElementById("js_by_screen"+finished_screen_number+"_time") === null) {
				var input_screentime=document.createElement("input");
				input_screentime.type="hidden"; input_screentime.value=((timenow-starttime)/1000).toString();
				input_screentime.name=js_vars.screentime_prefix+"screen"+finished_screen_number+"_time";
				input_screentime.id="js_by_screen"+finished_screen_number+"_time";
				$("form").append(input_screentime);
				// console.log(js_vars.screentime_prefix, input_screentime.id, input_screentime.value, input_screentime);
			}
			// $("#js_by_screen"+finished_screen_number+"_time").val((timenow-starttime)/1000);
			// console.log("by=",by,"nanswtot=",nanswtot);
			for(var i = nanswtot; i< nanswtot+by; i++) if(i<allvars.length) if(varsshown[i] == 0) {
				$("#field_"+allvars[i]).show(150); //
				//console.log("allvars_i=",allvars[i],"i=",i,"nanswtot+by=",nanswtot+by);
				varsshown[i] = 1;
			}
			if(!no_scroll && finished_screen_number<last_screen_number && document.getElementById("initial_presentation") !== null) $([document.documentElement, document.body]).animate({
				scrollTop: $("#initial_presentation").offset().top
			}, 10);
			starttime=(new Date()).getTime();
			// console.log("starttime=",starttime);
			if(nanswtot<allvars.length && typeof liveSend === 'function') {
				datatosend=[];
				for(var i = 0; i< nanswtot; i++) {
					var cval = (document.forms[0][allvars[i]] !== undefined) ? document.forms[0][allvars[i]].value : "";
					if(allvars[i]!="__info__" && document.forms[0][allvars[i]].type !== undefined) {
						if(document.forms[0][allvars[i]].type == "checkbox") cval=document.forms[0][allvars[i]].checked?1:0;
					}
					datatosend.push([allvars[i], cval].join(';'));
					var cvaltime = (document.forms[0][allvars[i]+"_time"] !== undefined) ? document.forms[0][allvars[i]+"_time"].value : "";
					datatosend.push([allvars[i]+"_time", cvaltime].join(';'));
				}
				for(var s=1; s<=finished_screen_number; s++) if(js_vars.screentime_prefix != undefined && document.getElementById("js_by_screen"+finished_screen_number+"_time") !== null) {
					datatosend.push([js_vars.screentime_prefix+"screen"+s+"_time", document.getElementById("js_by_screen"+s+"_time").value, "js_by_screen"+s+"_time"].join(';'));
				}
				datatosend.push("nscr:"+finished_screen_number.toString()+":"+starttime.toString());
				liveSend('update|'+datatosend.join('|'));
			}
		}
		else {
			var scrolled=false;
			for(i=0; i<varsshown.length; i++) if(varsshown[i]>0 && document.getElementById(allvars[i]+"_errormessage") !== null && document.forms[0][allvars[i]].value==""  && document.getElementById(allvars[i]+"_errormessage").title=="required") {
				force_prevent_default=true;
				document.getElementById(allvars[i]+"_errormessage").innerHTML=(js_vars.field_required_message === undefined)?js_vars.lq_lexicon.please_answer_question:js_vars.field_required_message;
				document.getElementById(allvars[i]+"_errormessage").style.display="block";
				if(!scrolled) {
					$([document.documentElement, document.body]).animate({
						scrollTop: $("#field_"+allvars[i]).offset().top,
					}, 10);
					scrolled=true;
				}
			}
			if(!scrolled && need_confirm_empty_optional) {
				console.log(js_vars.lq_lexicon)
				confirmModal(js_vars.lq_lexicon.please_confirm_blank_questions,function(confirmed){
					if(confirmed) {
						empty_optional_confirmed=true;
						$(".otree-btn-next").click();
						empty_optional_confirmed=false;
					}
				});
			}
		}
		// console.log("varshown=",varsshown,"varsanswered=",varsanswered,"nanswtot=",nanswtot,"bynow=",bynow,"screen_listing=",screen_listing,"allvars.length=",allvars.length,"allvars=",allvars,"force_prevent_default=",force_prevent_default)
		var will_go_next=false;
		if(nanswtot<allvars.length) { 
			if(nanswnow == bynow || force_prevent_default) e.preventDefault();
			if(nanswnow == bynow) will_go_next=true;
		}
		else {
			$("form.otree-form").on("submit",function() {
				$("#blocpage_content").css("visibility","hidden");
				$("#control_buttons").hide(); $("#waitnext_text").hide(); 
				$("#pleasewait").show();
				$("form.otree-form").off("submit");
			});
			if(typeof js_vars.debug !== 'undefined' && js_vars.debug) {
				for(var i=0; i<varsanswered.length; i++) $("#field_"+allvars[i]).show();
				$([document.documentElement, document.body]).animate({
					scrollTop: $("#pleasewait").offset().top
				}, 1);
			}
			// console.log("nanswtot=",nanswtot,"allvars.length=",allvars.length,"will_go_next=",will_go_next.toString(),allvars,"varsanswered=",varsanswered, document.forms[0][allvars[0]].value);
			// e.preventDefault();
		}
		if(!force_prevent_default && !screen_listing && !will_go_next) {
			// avoiding "blue shadow" around the first option when not answered
			$(".form-check-input").addClass("nofocus");
			$(".form-check-input").on("focus",function() {
				$(this).trigger("blur");
				$(".form-check-input").removeClass("nofocus");
				$(".form-check-input").off("focus");
			});
			
		}
		// console.log("nanswtot=",nanswtot,"allvars.length=",allvars.length,"will_go_next=",will_go_next.toString(),"force_prevent_default=",force_prevent_default.toString(),"allvars=",allvars,"varsanswered=",varsanswered, document.forms[0][allvars[0]].value);
		//setTimeout(function() {$(".otree-btn-next").prop('disabled',false);},750);
	}
});

$("#prevbutton").click(function(e){
	prev_button_clicked=true; next_button_clicked=false;
	if(by>0 && allvars.length>0) {
		if(waitnext_timer_handler!==null && waitnext_timer_handler!==false) {clearTimeout(waitnext_timer_handler); $("#waitnext_text").hide(); $("#control_buttons").show();}
		var nanswtot=0
		for(i=0; i<varsshown.length; i++) { if(varsshown[i]==0) nanswtot++; else break;}
		for(var i=nanswtot; i<varsanswered.length; i++) varsanswered[i]=0;
		var finished_screen_number=1, last_screen_number=allvars.length/by;
		if(window.bys !== undefined && bys.length>1) {
			var cbindex=0, cbsum=0;
			for(var b=0; b<bys.length; b++) {
				cbsum+=parseInt(bys[b]);
				if(cbsum<=nanswtot) cbindex++;
			}
			finished_screen_number=cbindex; last_screen_number=bys.length;
			if(cbindex+1>bys.length) cbindex=bys.length-1;
			var cbindexprev=cbindex-1;
			by=parseInt(bys[cbindexprev]);
			if(js_vars.bys_intro != undefined && js_vars.bys_intro.length>cbindexprev) {
				// console.log("-"+js_vars.bys_intro[cbindexprev]+"-");
				var new_presentation_content=js_vars.bys_intro[cbindexprev];
				if (js_vars.bys_intro[cbindexprev] != "") new_presentation_content = "<h5>"+js_vars.bys_intro[cbindexprev]+"<br><br></h5>";
				$("#initial_presentation").html(new_presentation_content);
			}
			for(var si=0; si<Math.max(window.bys.length,allvars.length); si++) {$(".initial_presentation_"+(parseInt(si)+1).toString()).hide(); $(".not_initial_presentation_"+(parseInt(si)+1).toString()).show(); if(document.getElementById("initial_presentation_"+(parseInt(si)+1).toString()) !== null) $("#initial_presentation_"+(parseInt(si)+1).toString()).hide();}
			$((".initial_presentation_"+(parseInt(cbindexprev)+1).toString())).show(); $((".not_initial_presentation_"+(parseInt(cbindexprev)+1).toString())).hide(); if(document.getElementById("initial_presentation_"+(parseInt(cbindexprev)+1).toString()) !== null) $(("#initial_presentation_"+(parseInt(cbindexprev)+1).toString())).show();
			// console.log("by=",by,"cbindex=",cbindex,"cbindexprev=",cbindexprev,"prev_buttons.length=",js_vars.prev_buttons.length,"bys=",bys, "nanswtot=", nanswtot, "varsshown=",varsshown, "varsanswered=",varsanswered);
		}
		var bynow=0;
		var timenow=(new Date()).getTime();
		for(i=0; i<varsshown.length; i++) if(varsshown[i]>0 && allvars[i]!="") {
			bynow++;
			$("#field_"+allvars[i]).hide();
			varsshown[i] = 0;
		}
		if(cbindexprev==0) {
			if(js_vars.hide_initial!=undefined && js_vars.hide_initial) $("#initial_presentation").show();
			$("#prevbutton").prop("disabled", true);
		}
		if(js_vars.prev_buttons != undefined) {
			var cprevbutshow=(js_vars.prev_buttons.length>cbindexprev)?js_vars.prev_buttons[cbindexprev]:js_vars.prev_buttons[js_vars.prev_buttons.length-1];
			if(cprevbutshow == 0) {
				$("#prevbutton").hide();
			}
		}
		
		for(var i = nanswtot-by; i< nanswtot; i++) if(i>=0 && i<allvars.length) if(varsshown[i] == 0) {
			$("#field_"+allvars[i]).show(150); //
			//console.log("allvars_i=",allvars[i],"i=",i,"nanswtot+by=",nanswtot+by);
			varsshown[i] = 1;
		}
		if(finished_screen_number<last_screen_number && document.getElementById("initial_presentation") !== null) $([document.documentElement, document.body]).animate({
			scrollTop: $("#initial_presentation").offset().top
		}, 10);
		starttime=(new Date()).getTime(); 
	}
});

// console.log(js_vars.withtags);
if(js_vars.withtags.length>0) {
  var proceeded=false;
  $("label").each(function() {
	  var cfor =  $(this).attr("for");
	  var proceed=false;
	  for(var w=0; w<js_vars.withtags.length; w++) {
		  if(cfor.replace(js_vars.withtags[w],'')!=cfor) proceed=true;
	  }
	  if(proceed) {
		  proceeded=true;
		  $( this ).html($( this ).html().replace(/&gt;/gi,">").replace(/&lt;/gi,"<").replace(/&amp;/gi,"&"));
	  }
   // console.log("for="+$(this).attr("for"),$( this ).html());
  });
//   console.log(proceeded);
  if(proceeded) $("option").each(function() {
	  var cfor =  $(this).parent().attr("name");
	  // console.log('cfor',cfor);
	  var proceed=false;
	  for(var w=0; w<js_vars.withtags.length; w++) {
		  if(cfor.replace(js_vars.withtags[w],'')!=cfor) proceed=true;
	  }
	  if(proceed) {
		  $( this ).html($( this ).html().replace(/&gt;/gi,">").replace(/&lt;/gi,"<").replace(/&amp;/gi,"&"));
	  }
	});
}
if(js_vars.withouttags.length>0) {
	// console.log(js_vars.withouttags)
	$('input[type="radio"]').parent().find('label').each(function() {
		var ccontent = $(this).html();
		var cfor =  $(this).attr("for");
		var proceed=false;
		for(var w=0; w<js_vars.withouttags.length; w++) {
			if(cfor.replace(js_vars.withouttags[w],'')!=cfor) proceed=true;
		}
		// console.log($(this).val(), cfor, proceed)
		if(proceed) $(this).html(ccontent.replace(/&/gi,"&amp;").replace(/>/gi,"&gt;").replace(/</gi,"&lt;"));
		
	});
	
}


						  
if(typeof liveSend === 'function') liveSend('load|nscr:0:'+starttime.toString());
});


jQuery.fn.centerHorizontally = function (raw) {
	if(raw === undefined) raw=false;
	if(raw) {
		this.css("position","absolute");
		// this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop()) + "px");
		// console.log("outerWidth:",$(this).outerWidth(),"scrollLeft:",$(window).scrollLeft(),"$(window).width():",$(window).width());
		this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + $(window).scrollLeft()) + "px");
		$( window ).resize(this,function(event){$(event.data).centerHorizontally()});
	}
	else {
		var newdiv = document.createElement("div");
		$(newdiv).addClass("text-center");
		$(this).before(newdiv)
		$(this).attr('align','center')
		$(newdiv).append($(this));
	}
    return this;
}