
function SendRemovePhoneNumberRequest(url, token) {
    return fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify({
            'phone_number': null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success === true) {
            return true;
        } else {
            throw new Error(data.detail || 'Failed to remove phone number');
        }
    })
    .catch(error => {
        console.error("Error:", error);
        return false;
    });
}
