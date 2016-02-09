window.ParsleyConfig = {

    errorsWrapper: '<span class="help-block"></span>',
    errorTemplate: '<span></span>',
    successClass: 'has-success',           // Class name on each valid input
    errorClass: 'has-error',               // Class name on each invalid input

    classHandler: function (el) {
        // Return the $element that will receive these above success or error
        // classes Could also be (and given directly from DOM) a valid selector like '#div'
        return el.$element.closest(".form-group");
    },

};