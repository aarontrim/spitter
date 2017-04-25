function spittboxResponse(responseText, statusText, xhr, $form) {
	if(responseText.search("ERROR!") != 2) {
		$('#feed').prepend($(responseText).fadeIn('slow'));			
	}
	$("#spittbox-text")[0].value = "";
	$("#spitt-submit").text("Spitt");
}

function spittboxPreSubmit(formData, jqForm, options) {
	$("#spitt-submit").text("Submitting...");
}

function bioResponse(responseText, statusText, xhr, $form) {
	if(responseText.search("ERROR!") != 2) {
		$("#user-bio-my").html(responseText);
	}	
	$("#user-bio-my").show();
}

function bioPreSubmit(formData, jqForm, options) {
	$("#user-bio-form").hide();
}

function imgResponse(responseText, statusText, xhr, $form) {
	if(responseText.search("ERROR!") != 2) {
		$("#profile-done").text('Done');
		$("#profile-image-upload").attr("src", responseText);
		location.reload();
		location.href = location.href;
		window.location = window.location;
	} else {
		$("#profile-done").text('ERROR!');
		location.reload();
		location.href = location.href;
		window.location = window.location;
	}
}

function imgPreSubmit(formData, jqForm, options) {
	$("#profile-done").text('Loading...');
	$("#profile-done").on('click', function(e) {
		e.preventDefault();
	});
}

$( document ).ready(function() {
	$("#following").hide();
	$("#followers").hide();
	$("#status-spitt").addClass("hovered");

	$("#spittbox-form").ajaxForm({	success: spittboxResponse, 
									beforeSubmit: spittboxPreSubmit});

	$("#user-bio-form").ajaxForm({
		success: bioResponse,
		beforeSubmit: bioPreSubmit
	});

	$("#profile-image-form").ajaxForm({
		success: imgResponse,
		beforeSubmit: imgPreSubmit
	});

	$("#status-spitt").on('click', function(e) {
		e.preventDefault();
		if(!$(this).hasClass("hovered")) {
			$("#following").hide();
			$("#followers").hide();
			$("#feed").show('slow');
			$("#status-following").removeClass("hovered");
			$("#status-spitt").addClass("hovered");
			$("#status-followers").removeClass("hovered");
		}
	});

	$("#status-following").on('click', function(e) {
		e.preventDefault();
		if(!$(this).hasClass("hovered")) {
			$("#feed").hide();
			$("#followers").hide();
			$("#following").show('slow');
			$("#status-following").addClass("hovered");
			$("#status-spitt").removeClass("hovered");
			$("#status-followers").removeClass("hovered");
		}
	});

	$("#status-followers").on('click', function(e) {
		e.preventDefault();
		if(!$(this).hasClass("hovered")) {
			$("#following").hide();
			$("#feed").hide();
			$("#followers").show('slow');
			$("#status-following").removeClass("hovered");
			$("#status-spitt").removeClass("hovered");
			$("#status-followers").addClass("hovered");
		}
	});

	$("#status-follow_this").on('click', function(e) {
		e.preventDefault();

		if($(this).prop('disabled') != true) {
			if($(this).hasClass("following")) {
				$(this).removeClass("following");
			} else {
				$(this).addClass("following");
			}
		
			$(this).prop('disabled', true);
			$.ajax({url: "follow",
						success: function(result) {
							$("#status-follow_this").prop('disabled', false);
						}
					});
		}
	});

	$("#profile-done").click(function(e) {
		e.preventDefault();
		$("#overlay").hide();
	});

	$("#profileimage-link").click(function(e) {
		e.preventDefault();
		$("#overlay").show();
	});


	$("#profile-image-upload-link").on('click', function(e){
        e.preventDefault();
        if($(this).prop('disabled') != true) {
        	$("#profile-image-file:hidden").trigger('click');
        	$(this).prop('disabled', true);
        }
    });

	$("#upload-window").on('change', "#profile-image-file", function(e) {
		$("#profile-image-form").submit()		
	});

	$("#spittbox-text").on('change keyup paste', function () {
	   $("#charcounter").html($("#spittbox-text")[0].value.length +  "/150");
	});

	$("#spittbox-text").focus(function() {
		var el = $("#spittbox-text");
		if(el[0].value.length == 0) {
			el.css("height", "100px");
		}
	});

	$("#spittbox-text").blur(function() {
		var el = $("#spittbox-text");
		if(el[0].value.length == 0) {
			el.css("height", "31px");
		}
	});

	$("#spitt-submit").on('click', function(e) {
		e.preventDefault();
		if($(this).text() == "Spitt") {
			$("#spittbox-form").submit();
		}
	});

	$("#user-bio-my").on('click', function(e) {
		$("#user-bio-my").hide();
		$("#user-bio-form").show();
		$("#user-bio-text").focus();
	});

	$("#user-bio-form").on('blur focusout', function(e) {
		$(this).submit();
	});

	$("#user-bio-text").on('focus change keyup paste', function () {
	   var s_height = $(this)[0].scrollHeight;
	   $(this).attr('style','height:'+s_height+'px');
	});

});