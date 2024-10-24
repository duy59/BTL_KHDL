# In-memory storage for blog posts
blog_posts = []

# Create a new blog post
async def create_blog_post(data):
    try:
        slug = data.get('slug')

        # Check if a blog post with the same slug already exists
        existing_blog_post = next((post for post in blog_posts if post['slug'] == slug), None)
        if existing_blog_post:
            return {'error': 'Slug already exists'}

        blog_posts.append(data)
        return data
    except Exception as error:
        return {'error': str(error)}

# Get all blog posts
async def get_all_blog_posts(condition={}):
    try:
        # Filter blog posts based on condition
        filtered_posts = [post for post in blog_posts if all(post.get(key) == value for key, value in condition.items())]
        return filtered_posts
    except Exception as error:
        return {'error': str(error)}

# Get a single blog post by ID
async def get_blog_post_by_id(id):
    try:
        blog_post = next((post for post in blog_posts if post['id'] == id), None)
        if not blog_post:
            return {'error': 'Blog post not found'}
        return blog_post
    except Exception as error:
        return {'error': str(error)}

# Get a single blog post by condition
async def get_single_blog_post_by_condition(condition={}):
    try:
        blog_post = next((post for post in blog_posts if all(post.get(key) == value for key, value in condition.items())), None)
        if not blog_post:
            return {'status': False, 'error': 'Blog post not found'}
        return {'status': True, 'blog_post': blog_post}
    except Exception as error:
        print('Error fetching blog posts by condition:', error)
        raise {'status': False, 'error': str(error)}

# Update a blog post by ID
async def update_blog_post_by_id(id, data):
    try:
        index = next((i for i, post in enumerate(blog_posts) if post['id'] == id), -1)
        if index == -1:
            return {'error': 'Blog post not found'}
        blog_posts[index].update(data)
        return blog_posts[index]
    except Exception as error:
        return {'error': str(error)}

# Delete a blog post by ID
async def delete_blog_post_by_id(id):
    try:
        index = next((i for i, post in enumerate(blog_posts) if post['id'] == id), -1)
        if index == -1:
            return {'error': 'Blog post not found'}
        blog_posts.pop(index)
        return {'message': 'Blog post deleted successfully'}
    except Exception as error:
        return {'error': str(error)}

# Update status for all blog posts
async def update_status_for_all_blog_posts():
    try:
        global blog_posts
        blog_posts = [
            {**post, 'deleted': True} if post['category']['slug'] != 'bat-dong-san' else post
            for post in blog_posts
        ]
        print('Updated documents:', blog_posts)
        return blog_posts
    except Exception as error:
        print('Error updating status for all blog posts:', error)
        raise error