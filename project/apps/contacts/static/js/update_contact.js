(function () {
        function submitForm(row, success, failure) {
            const id = row.find("input.id").val();
            const token = Cookies.get("csrftoken");
            const name = row.find("input.name").val();
            const address = row.find("input.address").val();
            const email = row.find("input.email").val();
            const phones = row.find("input.phones").val();
            const birthday = row.find("input.birthday").val().split("-");
            const birthdayDay = birthday[2];
            const birthdayMonth = birthday[1];
            const birthdayYear = birthday[0];

            $.ajax({
                type: 'POST',
                url: `update_contact/${id}`,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                contentType: 'application/x-www-form-urlencoded; charset=utf-8',
                data:
                    "csrfmiddlewaretoken=" + token + "&" +
                    "name=" + name +"&" +
                    "address=" + address +"&" +
                    "email=" + email +"&" +
                    "phones=" + phones +"&" +
                    "birthday_day=" + birthdayDay +"&" +
                    "birthday_month=" + birthdayMonth +"&" +
                    "birthday_year=" + birthdayYear +"&"
                ,
                success: function (response) {
                    console.log(response);
                    if (response.errors) {
                        failure(response.errors)
                    } else {
                        success()
                    }
                    return response;
                }
            });
        }

        $(".update-button").each(function () {
            const button = $(this);
            // Update button click handler
            button.click(function () {
                const row = button.parent().parent();

                // Replaces each field with a text input
                row.find("span").css("display", "none");
                row.find("input").css("display", "");

                // Replaces Update with Submit
                button.css("display", "none");
                const submitButton = $('<a type="button" class="btn btn-primary update-button">Submit</a>');
                button.parent().append(submitButton);

                // Submit button click handler
                submitButton.click(function () {
                    const row = submitButton.parent().parent();
                    submitForm(row, function() {
                        window.location.reload();
                    }, function(errors) {
                        for (const fieldName in errors) {
                            var errorField = document.getElementById("error")
                            errorField.textContent = `${fieldName}: ${errors[fieldName]}`
                            errorField.style.color = "red"
                        }
                    })
                });
            });
        });
    }
)
();

