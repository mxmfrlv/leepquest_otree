var name_array = [];
var form_map = {};
$(document).ready(function() {
	$("form#form :input")
    .each(function() {
		// console.log(this.name);
		var name = this.name;
		if($(this).hasClass("otree-btn-next") && !name) name="otree-btn-next";
        name_array.push(name);
		if(!form_map[name]) form_map[name] = []
		form_map[name].push(this)
    });
	console.log(form_map)
for(var name in form_map) {
	if(form_map[name].length>1) {
		if(form_map[name][0].type == "checkbox") {
			for(var i = 0; i<form_map[name].length; i++) {
				var checked = (Math.random()<0.5);
				form_map[name][i].checked=checked?"checked":false;
			}
		}
		else {
			var choosen=Math.floor(Math.random()*form_map[name].length);
			if($(form_map[name][choosen]).is(":button")) $(form_map[name][choosen]).click();
			else form_map[name][choosen].checked="checked";
		}
	}
	else {
		for(var i = 0; i<form_map[name].length; i++) {
			if($(form_map[name][i]).is(":button")) {
				// $(form_map[name][i]).prop("disabled",false);
				if($(form_map[name][i]).hasClass("otree-btn-next")) {
					setTimeout(function(me) {$(me).prop("disabled",false); $(me).click();$(me).click();}(form_map[name][i]), 300);
				}
				else $(form_map[name][i]).click();
			}
			else {
				var min=0, max=100;
				if(form_map[name][i].hasAttribute("min")) min=form_map[name][i].min;
				if(form_map[name][i].hasAttribute("max")) max=form_map[name][i].max;
				var choosen=parseFloat(min)+Math.floor(Math.random()*(parseFloat(max)+1-parseFloat(min)));
				$(form_map[name][i]).val(choosen);
				console.log(form_map[name][i], form_map[name][i].value, choosen, min, max);
			}
		}
	}
}
// setTimeout(function() {$("form#form").submit();}, 100);
});