$(document).ready(function() {
    $('#contact_form').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
        },
        message: "",
        fields: {
            nombre: {
                validators: {
                    stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Por favor introduzca su nombre'
                    },
                    regexp: {
                        regexp: '^[A-Za-záéíóúáéíóúÁÉÍÓÚñÑàèìòùÀÈÌÒÙ -]+$',
                        message: 'Por favor introduzca correctamente su nombre'
                    }
                }
            },
             apellido: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Por favor introduzca su apellido'
                    },
                    regexp: {
                        regexp: '^[A-Za-záéíóúáéíóúÁÉÍÓÚñÑàèìòùÀÈÌÒÙ -]+$',
                        message: 'Por favor introduzca correctamente su apellido'
                    }
                }
            },
			 username: {
                validators: {
                     stringLength: {
                        min: 5,
                    },
                    notEmpty: {
                        message: 'Por favor introduzca su nombre de usuario'
                    },
                    regexp: {
                        regexp: '^[a-zA-Z\\d]+$',
                        message: 'Por favor introduzca correctamente su nombre usuario'
                    }
                }
            },
			 pass: {
                validators: {
                     stringLength: {
                        min: 8,

                    },
                    notEmpty: {
                        message: 'Por favor introduzca su contraseña'
                    },
                    identical: {
                        field: 're_pass',
                        message: 'Las contraseñas no coinciden'
                    },
                    regexp: {
                        regexp: '(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
                        message: 'Por favor introduzca correctamente la contraseña'
                    }
                },
            },
			re_pass: {
                validators: {
                     stringLength: {
                        min: 8,
                    },
                    notEmpty: {
                        message: 'Por favor confirma la contraseña'
                    },
                    identical: {
                        field: 'pass',
                        message: 'Las contraseñas no coinciden'
                    },
                    regexp: {
                        regexp: '(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
                        message: 'Por favor introduzca correctamente la contraseña'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su correo electrónico'
                    },
                    email: {
                        message: 'Por favor introduzca un correo electrónico valido'
                    },
                    regexp: {
                        regexp: '^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$',
                        message: 'Por favor introduzca correctamente el email'
                    }
                }
            },
            tel: {
                validators: {
                    stringLength: {
                        min: 9,
                        max: 9,
                    },
                    notEmpty: {
                        message: 'Por favor introduzca su número de teléfono'
                    },
                    regexp: {
                        regexp: '[6-7]{1}[0-9]{8}',
                        message: 'Por favor introduzca correctamente el número de telefono'
                    }
                }
            }
        }
    })

    .on('success.form.bv', function(e) {
        $('#success_message').slideDown({ opacity: "show" }, "slow")
            $('#contact_form').data('bootstrapValidator').resetForm();

        // Prevent form submission
        e.preventDefault();

        // Get the form instance
        var $form = $(e.target);

        // Get the BootstrapValidator instance
        var bv = $form.data('bootstrapValidator');

        // Use Ajax to submit form data
        $.post($form.attr('action'), $form.serialize(), function(result) {
            console.log(result);
        }, 'json');
    });
});

function validar_dni(value){

				  var validChars = 'TRWAGMYFPDXBNJZSQVHLCKET';
				  var nifRexp = /^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKET]{1}$/i;
				  var str = value.toString().toUpperCase();

				  if (!nifRexp.test(str)) return false;

				  var letter = str.substr(-1);
				  var charIndex = parseInt(str.substr(0, 8)) % 23;

				  if (validChars.charAt(charIndex) === letter) return true;

				  return false;
}
