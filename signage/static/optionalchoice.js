(function ($) {
    $(document).ready(function () {
        $.each($('select[name*=url]'), function (i, e) {
            e.onchange = function () {
                var prefix = this.name.split('-'),
                    suffix = prefix[2].split('_'),
                    target = 'input[name=' + prefix[0] + '-' + prefix[1] + '-' + suffix[0] + '_' + (parseInt(suffix[1]) + 1) + ']';
                if(this.value != '') {
                    if(!($(target).attr('_value'))) {
                        $(target).attr('_value',$(target).val());
                    }
                    $(target).val('');
                    $(target).prop('disabled', true);
                } else {
                    $(target).val($(target).attr('_value'));
                    $(target).prop('disabled', false);
                }
            }
            if($(e).val()) {
                $(e).trigger("change");
            }
        })
    })
})(django.jQuery);