# Feedback Service Documentation

The feedback service supports the following endpoints:
#### GET: `/comments`

Retrieves all comments for a specified course. Optionally, can also return replies to a specific comment if  `replied_to_id` is provided.

**Parameters:**

- `course_id` (str): the identifier of the course for which comments are requested.
- `replied_to_id` (Optional[uuid.UUID]): specifies the comment identifier to which replies are being sought. If provided, only replies to this comment will be returned.
- `current_user_id` (Optional[str]): the identifier of the current user (optional). If specified, the retrieved comments will be marked with user's previous assessment.

#### POST: `/comment`

Post a new comment on the course discussion thread.

**Parameters:**

- `publishable_comment` ([PublishableUserComment](feedback_service/user_comment.py#L28)): contains the course thread ID, whether this comment is a reply, and user's ID.

Returns [CompleteUserComment](feedback_service/user_comment.py#L36) object with all necessary comment properties.

#### PUT: `/comment`

Edits the comment's text message.

**Parameters:**

- `comment` [IdentifiableUserComment](./feedback_service/user_comment.py#L22): stores all the info required to identify the comment.
- `new_comment_text` (str): new comment body. The previous text gets erased forever.


#### DELETE: `/comment`

Simulates comment deletion. The comment body is erased and the comment's attribute `is_deleted` is set to `True`.
The comment's ghost is left to ensure the correct tree structure of the discussion.

*TODO: add deletion of empty tree branches. For example, if the deleted comment is the last one in the branch, it should be deleted completely from the database.* 

**Parameters:**

`comment` [IdentifiableUserComment](./feedback_service/user_comment.py#L22): stores all the info required to identify the comment.

#### PUT: `/rate_comment`

Allows to specify the new rating (assessment) for a given comment. Each user can leave the rating on every comment at most once.

**Parameters:**

- `comment` [IdentifiableUserComment](./feedback_service/user_comment.py#L22): stores all the info required to identify the comment.
- `assessor_user_id` (str): the assessor's ID. It is used to check whether he has already rated the comment.
- `assessment` (int): either $0$, $1$, or $2$.
	- $0$ means `No Assessment`. Used when the user wants to take back his previous like/dislike.
	- $1$ means `Like Assessment`. Represents a like.
	- $2$ means `Dislike Assessment`. Represents a dislike.
