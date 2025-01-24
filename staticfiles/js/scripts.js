$(document).ready(function () {
    // Handle new post submission
    $('#new-post-form').submit(function (e) {
        e.preventDefault();
        const formData = $(this).serialize(); // Serialize form data

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            headers: { 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() },
            data: formData,
            success: function (data) {
                if (data.success) {
                    // Prepend the new post to the list of blog posts
                    $('#blog-posts-container').prepend(`
                        <div class="card my-3">
                            <div class="card-body">
                                <h5>${data.title}</h5>
                                <p>${data.content}</p>
                                <small>By ${data.user} | ${data.created_at}</small>

                                <!-- Likes -->
                                <button class="btn btn-primary btn-sm like-btn" data-post-id="${data.post_id}">
                                    Like (<span id="like-count-${data.post_id}">0</span>)
                                </button>

                                <!-- Comments -->
                                <h6 class="mt-3">Comments</h6>
                                <div id="comment-list-${data.post_id}">
                                    <p>No comments yet.</p>
                                </div>

                                <!-- Add Comment -->
                                <form class="comment-form mt-2" data-post-id="${data.post_id}">
                                    <input type="text" name="content" placeholder="Add a comment" class="form-control form-control-sm mb-2">
                                    <button type="submit" class="btn btn-secondary btn-sm">Post Comment</button>
                                </form>
                            </div>
                        </div>
                    `);

                    // Clear the form
                    $('#new-post-form')[0].reset();
                }
            },
            error: function () {
                alert('Error creating post. Please try again.');
            }
        });
    });

    // Handle Likes
    $('.like-btn').on('click', function () {
        const postId = $(this).data('post-id');

        $.ajax({
            url: `/blog/${postId}/like/`,
            type: 'POST',
            headers: { 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() },
            success: function (data) {
                if (data.liked !== undefined) {
                    $(`#like-count-${data.post_id}`).text(data.total_likes);
                } else {
                    alert('Error liking post.');
                }
            },
            error: function () {
                alert('Error liking post. Please try again.');
            }
        });
    });

    // Handle Add Comment
    $('.comment-form').on('submit', function (e) {
        e.preventDefault();

        const postId = $(this).data('post-id');
        const commentInput = $(this).find('input[name="content"]');
        const commentContent = commentInput.val();

        $.ajax({
            url: `/blog/${postId}/comment/`,
            type: 'POST',
            headers: { 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() },
            data: { content: commentContent },
            success: function (data) {
                if (data.success) {
                    $(`#comment-list-${data.post_id}`).append(`
                        <div class="mb-2">
                            <p>
                                <strong>${data.comment_user}</strong>: ${data.comment_content}
                            </p>
                        </div>
                    `);
                    commentInput.val(''); // Clear input field
                } else {
                    alert('Error adding comment.');
                }
            },
            error: function () {
                alert('Error adding comment. Please try again.');
            }
        });
    });
});
