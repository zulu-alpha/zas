window.ParsleyConfig = {
    classHandler: function (elem) {
        // Return the $element that will receive these above success or error
        // classes Could also be (and given directly from DOM) a valid selector like '#div'
        return $(elem).closest(".form-group");
    },


    errorsContainer: function ( elem, isRadioOrCheckbox ) {
        // Return the $element where errors will be appended Could also be
        // (and given directly from DOM) a valid selector like '#div'
        return $(elem).closest(".help-block")
    },


    errorsWrapper: '<span class="help-block"></span>',
    errorTemplate: '<span></span>',
    successClass: 'has-success',           // Class name on each valid input
    errorClass: 'has-error'               // Class name on each invalid input
};