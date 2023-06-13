function Accept(friend_id){
    alert(friend_id)
}
function Delete(friend_id)
{
    alert(friend_id)
}

function performAction(friendId) {
    // Specify the URL of your Flask route with the friendId as a query parameter
    var url = '/delete_friend?friend_id=' + friendId; // Replace with your Flask route URL

    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Set up the AJAX request
    xhr.open('GET', url, true);

    // Define the callback function to handle the AJAX response
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Request successful, handle the response here
                console.log(xhr.responseText);
                // Optionally, update the page dynamically based on the response
            } else {
                // Request failed, handle the error here
                console.error('Request failed with status ' + xhr.status);
            }
        }
    };

    // Send the AJAX request
    xhr.send();
}
