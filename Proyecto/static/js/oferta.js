$(document).ready(function() {
    $('#survey_form').bootstrapValidator({
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
                        message: 'Por favor introduzca un nombre de contacto'
                    },
                    regexp: {
                        regexp: '^[A-Za-záéíóúáéíóúÁÉÍÓÚñÑàèìòùÀÈÌÒÙ -]+$',
                        message: 'Por favor introduzca correctamente un nombre de contacto'
                    }
                }
            },
             title_job: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Por favor introduzca el titulo del trabajo'
                    },
                    regexp: {
                        regexp: '^[A-Za-záéíóúáéíóúÁÉÍÓÚñÑàèìòùÀÈÌÒÙ -]+$',
                        message: 'Por favor introduzca correctamente el titulo del trabajo'
                    }
                }
            },
            city: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Por favor introduzca la ciudad'
                    },
                    regexp: {
                        regexp: '^[A-Za-záéíóúáéíóúÁÉÍÓÚñÑàèìòùÀÈÌÒÙ -]+$',
                        message: 'Por favor introduzca correctamente la ciudad'
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
            grado: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su grado'
                    }
                }
            },
            nota_media: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nota media'
                    }
                }
            },
            ingles_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel de ingles'
                    }
                }
            },
            aleman_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel de aleman'
                    }
                }
            },
            frances_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel de frances'
                    }
                }
            },
            trabajoEquipo_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            comunicacion_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            matematicas_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            estadistica_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            gestionProyectos_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            sostenibilidad_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            bigData_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            progra_level:{
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione su nivel correspondiente'
                    }
                }
            }
        }
    })

    .on('success.form.bv', function(e) {
        $('#success_message').slideDown({ opacity: "show" }, "slow")
            $('#survey_form').data('bootstrapValidator').resetForm();

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

