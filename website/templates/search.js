$(function() {
    $.ajax({
        url: '{{ url_for("autocomplete") }}'
        }).done(function (data) {
            $('#autocomplete').autocomplete({
                source: data.json_list,
                minLength: 2
            });
        });
    });