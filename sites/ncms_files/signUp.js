function setCookie(cname, cvalue, exdays) {
	    var d = new Date();
	    d.setTime(d.getTime() + (exdays*24*60*60*1000));
	    var expires = "expires="+ d.toUTCString();
	    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
$( document ).ready(function() {
	$('#btnSignUp').click(function(){
		// alert('reached');
		$.ajax({
			url: '/signUp',
			data: $('#formSignUp').serialize(),
			type: 'POST',
			success: function(response){
				alert("Created User !");
				window.location = "/";
			},
			error: function(error){
				alert("Error creating user !");
			}
		});
		return false;
	});
	$('#btnSignIn').click(function(){
		$.ajax({
			url: '/signIn',
			data: $('#formSignIn').serialize(),
			type: 'POST',
			success: function(response){
				window.location = "../home";
				setCookie("email",$("#inputFirstName")[0].value,1);
			},
			error: function(error){
				alert("Wrong username or password");
			}
		});
		return false;
	});
});
// });
