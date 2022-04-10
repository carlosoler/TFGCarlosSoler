$(document).ready(function() {
    $('#survey_form').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
        },
        message: "",
        fields: {
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
            capAnalitica_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
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
            pensamientoCritico_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            innovacion_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            liderazgo_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            tomaDecisiones_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            solucionProblemas_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            marketing_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            ecommerce_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            disenoGrafico_level: {
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
            redesSociales_level: {
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
            inteligenciaArtificial_level: {
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
            machineLearning_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            analisisDatos_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            basesDatos_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            cloud_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            iot_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            redes_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            sistemasOperativos_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            desarrolloWeb_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            disenoWeb_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            r_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            java_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            pascal_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
                    }
                }
            },
            python_level: {
                validators: {
                    notEmpty: {
                        message: 'Por favor introduzca su nivel correspondiente'
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

