async function manageAjaxCalls(jobj) {
    const type = "POST";
    
    try {
        let response = await $.ajax({
            url: urlManageAjaxCalls,  
            type: type,
            data: { 
                data: JSON.stringify(jobj), 
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()  
            },
            success: function (response) {
                console.log("Success:", response);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.error("Error:", thrownError);
            }
        });
        return response;
    } catch (error) {
        console.error("AJAX request failed:", error);
        throw error; 
    }
}
