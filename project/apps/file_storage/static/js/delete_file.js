$('#delete_file_modal').submit(function (e) {
    e.preventDefault()
    $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        dataType: 'json',
        success: function (response) {
            console.log(response)
            const message = response.message

            if (response.status === 204) {
                if (window.location.href === response.url){
                    window.location.reload()
                }
                else {
                    window.location.href = response.url
                }
            } else if (response.status === 400) {
                $('.alert-warning').text(message).removeClass('d-none')
            }

        },
        error: function (response) {
                console.log('error' - response)
            }
    })
})
