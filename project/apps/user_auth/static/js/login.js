$('#login_modal').submit(function (e) {
    e.preventDefault()
    $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        dataType: 'json',
        success: function (response) {
            console.log(response)
            const message = response.message
            if (response.status === 200) {
                console.log(message)
                window.location.reload()
            } else if (response.status === 400) {
                $('.alert-warning').text(message).removeClass('d-none')
            }

        },
        error: function (response) {
                console.log('error' - response)
            }
    })
})
