// function registerJob() {
//     var form = $('#registerForm');
//     form.html('<p>Registering...</p>');
//     $.ajax({
//         url: "{% url 'register_job' jobs.id %}",
//         type: 'post',
//         headers: {'X-CSRFToken': '{{ csrf_token }}'},
//         success: function(response) {
//             if (response.status == 'success') {
//                 form.html('<p>Registered</p>');
//                 setTimeout(function() {
//                     window.location.href = "/";
//                 }, 2000);  // Redirect after 2 seconds
//             }
//         }
//     });
// }

//ajax post request in job_detail