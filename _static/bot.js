var bot_name_array = [];
var bot_hidden_types = [];
var form_map = {};
var bot_submit_but_name='';
var bot_submit_index=0;
var bot_submit_timeout;
var bot_loaded=false;
function botSubmitForm(name,i) {
	clearTimeout(bot_submit_timeout);
	if(!bot_loaded) return
	console.log('botSubmitForm',name,i);
	var me = form_map[name][i];
	$("form.otree-form").on("submit",function() {
		clearTimeout(bot_submit_timeout);
	});
	console.log("now clicking submit button", me);
	$(me).prop("disabled",false); $(me).click();$(me).click();
	
	// if('prev' in form_map && form_map['prev'].length==1) {console.log("now click prev button"); $(form_map['prev'][0]).click();}
	if($(me).is(':visible')) {
		bot_submit_timeout=setTimeout(function() {console.log(form_map,name,i); botSubmitForm(name,i);}, 300);
		console.log("set timeout again");
	}
}
function botProceedInput(index) {
	var name = bot_name_array[index];
	if(name!="-hidden-noname-") { //name!="_"
		if(form_map[name].length>1) {
			if(form_map[name][0].type == "checkbox") {
				for(var i = 0; i<form_map[name].length; i++) {
					var checked = (Math.random()<0.5);
					//form_map[name][i].checked=checked?"checked":false;
					if(checked) {$(form_map[name][i]).click(); console.log("clicked to check",name);}
					else console.log("chosen not to check",name);
				}
			}
			else {
				var name_inputs=[], n_visible=0, n_invisible=0;
				for(var i = 0; i<form_map[name].length; i++) {
					if($(form_map[name][i]).is(":visible")) n_visible++;
					else n_invisible++;
				}
				for(var i = 0; i<form_map[name].length; i++) {
					if(n_visible>0 && n_invisible>0 && $(form_map[name][i]).is(":visible")) name_inputs.push(form_map[name][i]);
					if(n_visible==0 || n_invisible==0) name_inputs.push(form_map[name][i]);
				}
				var choosen=Math.floor(Math.random()*name_inputs.length);
				$(name_inputs[choosen]).click(); console.log("clicked",name);
				// if($(name_inputs[choosen]).is(":button")) $(name_inputs[choosen]).click();
				// else name_inputs[choosen].checked="checked";
			}
		}
		else {
			for(var i = 0; i<form_map[name].length; i++)  {
				if($(form_map[name][i]).is(":button")) {
					// $(form_map[name][i]).prop("disabled",false);
					if($(form_map[name][i]).hasClass("otree-btn-next") && bot_submit_index<=1) {
						bot_submit_timeout=setTimeout(function() {console.log(form_map,name,i); botSubmitForm(name,0);}, 300);
						console.log("Timeout set",name);
					}
					else if(name!="prev") {$(form_map[name][i]).click(); console.log("clicked",name);}
				}
				else {
					if(form_map[name][i].type == "checkbox") {
						var checked = (Math.random()<0.5);
						//form_map[name][i].checked=checked?"checked":false;
						if(checked) {$(form_map[name][i]).click(); console.log("clicked to check",name);}
						else console.log("chosen not to check",name);
					}
					else if(form_map[name][i].type.split('-')[0] == "select") {
						var options = form_map[name][i].getElementsByTagName("option");
						var values = [];
						for(var io = 0; io<options.length; io++) {
							if(options[io].value) values.push([io,options[io].value])
						}
						var choosen=Math.floor(Math.random()*values.length);
						form_map[name][i].value=values[choosen][1];
						console.log(name,form_map[name][i].type+" value set to ",values[choosen][1]);
							
					}
					else if(form_map[name][i].type != "hidden" || !$(form_map[name][i]).val() ) {
						var min=0, max=100;
						if(form_map[name][i].hasAttribute("min")) min=form_map[name][i].min;
						if(form_map[name][i].hasAttribute("max")) max=form_map[name][i].max;
						var choosen=parseFloat(min)+Math.floor(Math.random()*(parseFloat(max)+1-parseFloat(min)));
						$(form_map[name][i]).val(choosen); console.log("value set",name);
						console.log(form_map[name][i], form_map[name][i].value, choosen, min, max);
					}
				}
			}
		}
	}
	if(index<bot_name_array.length-1) setTimeout(function() {botProceedInput(index+1);},50);
}
$(document).ready(function() {
	$("form#form :input")
    .each(function() {
		// console.log(this.name);
		var name = this.name;
		if($(this).hasClass("otree-btn-next")) {
			if(!name) name="otree-btn-next";
			if(bot_submit_but_name) bot_name_array.push(bot_submit_but_name);
			if(bot_submit_index>0) name+="-".name.toString()
			bot_submit_but_name = name;
			bot_submit_index++;
			console.log("otree-btn-next",bot_submit_index);
		}
		else if (this.type!="hidden") {
			if(!name) name="_";
			if(bot_name_array.indexOf(name)<0) bot_name_array.push(name);
		}
		else if (this.type == "hidden") {
			if(!name) name="-hidden-noname-";
			if(bot_hidden_types.indexOf(name)<0) bot_hidden_types.push(name);
		}
		if(!form_map[name]) form_map[name] = []
		form_map[name].push(this)
    });
	if(bot_hidden_types.length>0) for(var h=0; h<bot_hidden_types.length; h++) {bot_name_array.push(bot_hidden_types[h]);}
	if(bot_submit_but_name) bot_name_array.push(bot_submit_but_name);
	console.log(bot_name_array,form_map)
	if(bot_name_array.length>0) setTimeout(function() {bot_loaded=true; botProceedInput(0);},500);
// for(var name in form_map) {

// }
// setTimeout(function() {$("form#form").submit();}, 100);
});