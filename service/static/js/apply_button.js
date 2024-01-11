function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $(".apply-button").each(function () {
        var button = $(this);
        var pk = button.data('pk');
        var appliedKey = "applied_" + pk;

        $.ajax({
            url: "/check_application/" + pk + "/",
            type: "GET",
            dataType: "json",
            success: function (data) {
                if (data.applied) {
                    setButtonState(true);
                } else {
                    setButtonState(false);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error:", xhr, status, error);
            }
        });

        button.click(function () {
            if (button.hasClass("btn-secondary")) {
                $.ajax({
                    url: "/remove_application/" + pk + "/",
                    type: "POST",
                    dataType: "json",
                    headers: {
                        "X-CSRFToken": getCookie('csrftoken')
                    },
                    success: function (data) {
                        console.log("Success response:", data);
                        setButtonState(false);
                    },
                    error: function (xhr, status, error) {
                        console.error("Error:", xhr, status, error);
                    }
                });
            } else {
                $.ajax({
                    url: "/apply/" + pk + "/",
                    type: "POST",
                    dataType: "json",
                    headers: {
                        "X-CSRFToken": getCookie('csrftoken')
                    },
                    success: function (data) {
                        console.log("Success response:", data);
                        setButtonState(true);
                    },
                    error: function (xhr, status, error) {
                        console.error("Error:", xhr, status, error);
                    }
                });
            }
        });

        function setButtonState(applied) {
            if (applied) {
                button.removeClass("btn-primary").addClass("btn-secondary").prop("disabled", false).text("Remove");
            } else {
                button.removeClass("btn-secondary").addClass("btn-primary").prop("disabled", false).text("Apply");
            }
        }
    });
});
