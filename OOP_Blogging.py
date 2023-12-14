from datetime import datetime
import time
import logging


# Set the logging configuration to display INFO level messages
logging.basicConfig(level=logging.INFO)


def timing_decorator(func):
    """A decorator that measures the execution time of a function and logs it.
    Args:
        func (callable): The function to be decorated.
    Returns:
        callable: The decorated function.
    Usage:
        @timing_decorator
        def my_function():
    """

    def wrapper(*args, **kwargs):
        # Record the start time
        start_time = time.time()
        # Call the original function
        result = func(*args, **kwargs)
        # Record the end time
        end_time = time.time()
        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        # Log the execution time
        logging.info(f"{func.__name__} took {elapsed_time:.5f} seconds to execute.")
        # Log a sample message
        logging.info("Log: This is a log message.")
        # Return the result of the original function
        return result

    # Return the decorated function
    return wrapper


class User:
    @timing_decorator
    def __init__(self, user_id, username):
        """Constructor method to initialize the User object.
        Args:
            user_id (int): The unique identifier for the user.
            username (str): The username of the user.
        Usage:
            user = User(user_id=1, username="john_doe")
        """
        self.user_id = user_id
        self.username = username

    def __str__(self):
        """
        Method to represent the User object as a string.
        Returns:
            str: A formatted string representing the User.
        """
        return f"User ID: {self.user_id}, Username: {self.username}"


class Post:
    def __init__(self, title, content, author):
        """Constructor method to initialize the Post object.
        Args:
            title (str): The title of the post.
            content (str): The content of the post.
            author (User): The author of the post.
        Usage:
            post = Post(title="Title", content="Content", author=user_instance)
        """
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.now()
        self.updated_at = None

    @timing_decorator
    def update_content(self, new_content):
        """ Method to update the content of the Post.
        Args:
            new_content (str): The new content for the post.
        Usage:
            post.update_content("New content")
        """
        self.content = new_content
        self.updated_at = datetime.now()

    def __str__(self):
        """Method to represent the Post object as a string.
        Returns:
            str: A formatted string representing the Post."""
        # Format the updated_at timestamp or display "Not updated" if not available
        formatted_updated_at = str(self.updated_at) if self.updated_at else "Not updated"
        # Return a formatted string representing the Post
        return f"Post Title: {self.title}\nContent: {self.content}\nAuthor: {self.author.username}\nCreated At: {self.created_at}\nUpdated At: {formatted_updated_at}"


class Blog:
    def __init__(self):
        """ Constructor method to initialize the Blog object.
         Usage:
         blog = Blog()"""
        self.posts = []
        self.delete_post = []

    """Method to add a post to the blog.
        Args:
            post (Post): The post object to be added.
        Usage:
            blog.add_post(post_instance) """

    @timing_decorator
    def add_post(self, post):
        self.posts.extend(post)

    @timing_decorator
    def delete_post_by_title(self, title):
        """Method to delete a post by its title.
        Args:
            title (str): The title of the post to be deleted.
        Returns:
            list: List containing the deleted post(s).
        Usage:
            deleted_posts = blog.delete_post_by_title("Post Title")"""
        posts_to_delete = [post for post in self.posts if post.title == title]

        if posts_to_delete:
            post_to_delete = posts_to_delete[0]
            post_to_delete.updated_at = None  # Set updated_at to None to mark the post as deleted
            self.delete_post.append(post_to_delete)
            self.posts.remove(post_to_delete)
            return [post_to_delete]
        else:
            return []

    @timing_decorator
    def delete_post_by_author(self, author_username):
        """Method to delete posts by a specific author.
        Args:
            author_username (str): The username of the author whose posts should be deleted.
        Returns:
            list: List containing the deleted post(s).
        Usage:
            deleted_posts = blog.delete_post_by_author("author_username")"""
        lowercase_author_username = author_username.lower()
        posts_to_delete = [post for post in self.posts if post.author.username.lower() == lowercase_author_username]

        for post in posts_to_delete:
            post.updated_at = None  # Set updated_at to None to mark the post as deleted

        self.delete_post.extend(posts_to_delete)  # Move the posts to the delete_post list
        self.posts = [post for post in self.posts if post not in posts_to_delete]

        return posts_to_delete

    @timing_decorator
    def search_post_by_title(self, title):
        """Method to search for posts by title.
        Args:
            title (str): The title to search for.
        Returns:
            list: List containing the matching post(s).
        Usage:
            matching_posts = blog.search_post_by_title("Post Title")"""
        return [post for post in self.posts if post.title == title]

    @timing_decorator
    def search_post_by_author(self, author_username):
        """Method to search for posts by author.
        Args:
            author_username (str): The username of the author to search for.
        Returns:
            list: List containing the matching post(s).
        Usage:
            matching_posts = blog.search_post_by_author("author_username")"""
        lowercase_author_username = author_username.lower()
        return [post for post in self.posts if post.author.username.lower() == lowercase_author_username]

    @timing_decorator
    def filter_posts_by_title(self, keyword):
        """Method to filter posts by title using a keyword.
        Args:
            keyword (str): The keyword to filter posts by.
        Returns:
            list: List containing the filtered post(s).
        Usage:
            filtered_posts = blog.filter_posts_by_title("keyword")"""
        return (lambda keyword: [
            post for post in self.posts if keyword.lower() in post.title.lower()
        ])(keyword)

    @timing_decorator
    def filter_posts_by_author(self, author):
        """Method to filter posts by author username.
        Args:
            author (str): The username of the author to filter posts by.
        Returns:
            list: List containing the filtered post(s).
        Usage:
            filtered_posts = blog.filter_posts_by_author("author_username")"""
        return (lambda author: [
            post for post in self.posts if post.author.username.lower() == author.lower()
        ])(author)

    @timing_decorator
    def view_user_posts_by_title(self, author_username, title):
        """Method to view posts by a specific user with a specific title.
        Args:
            author_username (str): The username of the author.
            title (str): The title of the posts to view.
        Returns:
            list: List containing the matching post(s).
        Usage:
            user_posts = blog.view_user_posts_by_title("author_username", "Post Title")"""
        lowercase_author_username = author_username.lower()
        matching_posts = [post for post in self.posts
                          if post.author.username.lower() == lowercase_author_username
                          and post.title == title]

        return matching_posts

    @timing_decorator
    def view_user_posts_by_author(self, author_username):
        """Method to view posts by a specific user.
        Args:
            author_username (str): The username of the author.
        Returns:
            list: List containing the matching post(s).
        Usage:
            user_posts = blog.view_user_posts_by_author("author_username")"""
        lowercase_author_username = author_username.lower()
        return [post for post in self.posts if post.author.username.lower() == lowercase_author_username]

    @timing_decorator
    def update_post_content(self, title, new_content):
        """Method to update the content of a post.
        Args:
            title (str): The title of the post to be updated.
            new_content (str): The new content for the post.
        Returns:
            Post or None: The updated post or None if no matching post is found.
        Usage:
            updated_post = blog.update_post_content("Post Title", "New Content")"""
        matching_posts = [post for post in self.posts if post.title == title]

        if matching_posts:
            post_to_update = matching_posts[0]
            post_to_update.update_content(new_content)
            return post_to_update
        else:
            return None

    @timing_decorator
    def get_posts_generator(self):
        """Generator function to yield deleted posts.
        Returns:
            generator: A generator yielding deleted posts.
        Usage:
            deleted_posts_generator = blog.get_posts_generator()
            for post in deleted_posts_generator:
                # Process each deleted post"""
        # Generator function to yield posts
        for post in self.delete_post:
            yield post

    @timing_decorator
    def print_all_posts(self):
        """Method to print all active posts in the blog.
        Usage:
            blog.print_all_posts()"""
        print("All Posts:")
        for post in self.posts:
            print(post.__str__())


if __name__ == "__main__":
    # Create a new instance of the Blog class
    my_blog = Blog()
    try:
        while True:

            

            choice = input("Enter your choice: ")

            if choice == "1":
                # Option to add posts
                num_posts = int(input("Enter the number of posts to add: "))
                posts = []
                for _ in range(num_posts):
                    title = input("Enter post title: ")
                    content = input("Enter post content: ")
                    author_username = input("Enter author username: ")
                    author = User(user_id=len(my_blog.posts) + 1, username=author_username)
                    new_post = Post(title=title, content=content, author=author)
                    posts.append(new_post)
                my_blog.add_post(posts)
                print(f"{num_posts} post(s) added successfully!")

            elif choice == "2":
                # Option to delete posts by title
                title_to_delete = input("Enter the title of the post to delete: ")
                posts_to_delete = my_blog.delete_post_by_title(title_to_delete)
                if posts_to_delete:
                    print("Post(s) deleted successfully!")
                    for post in posts_to_delete:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "3":
                # Option to delete posts by author
                author_to_delete = input("Enter the username of the author to delete posts: ")
                posts_to_delete = my_blog.delete_post_by_author(author_to_delete)
                if posts_to_delete:
                    print("Post(s) deleted successfully!")
                    for post in posts_to_delete:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "4":
                # Option to search for posts by title
                title_to_search = input("Enter the title of the post to search: ")
                matching_posts = my_blog.search_post_by_title(title_to_search)

                if matching_posts:
                    print("\nMatching Posts:")
                    for post in matching_posts:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "5":
                # Option to search for posts by author
                author_to_search = input("Enter the username of the author: ")
                matching_posts = my_blog.search_post_by_author(author_to_search)
                if matching_posts:
                    print("\nMatching Posts:")
                    for post in matching_posts:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "6":
                # Option to update post content
                title_to_update = input("Enter the title of the post to update: ")
                new_content = input("Enter the new content for the post: ")
                updated_post = my_blog.update_post_content(title_to_update, new_content)
                if updated_post:
                    print("Post content updated successfully!")
                    print(updated_post)
                else:
                    print("No matching posts found for update.")

            elif choice == "7":
                # Option to filter posts by title
                keyword_to_filter = input("Enter the keyword to filter by title: ")
                filtered_posts = my_blog.filter_posts_by_title(keyword_to_filter)
                if filtered_posts:
                    print("\nFiltered Posts:")
                    for post in filtered_posts:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "8":
                # Option to filter posts by author
                author_to_filter = input("Enter the username to filter by: ")
                filtered_posts = my_blog.filter_posts_by_author(author_to_filter)
                if filtered_posts:
                    print("\nFiltered Posts:")
                    for post in filtered_posts:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "9":
                # Option to view posts by a specific user
                author_to_view = input("Enter the username of the author: ")
                matching_posts = my_blog.view_user_posts_by_author(author_to_view)
                if matching_posts:
                    print("\nMatching Posts:")
                    for post in matching_posts:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "10":
                # Option to view posts by a specific user and title
                author_to_view = input("Enter the username of the author: ")
                title_to_view = input("Enter the title of the post: ")
                matching_posts = my_blog.view_user_posts_by_title(author_to_view, title_to_view)
                if matching_posts:
                    print("\nMatching Posts:")
                    for post in matching_posts:
                        print(post)
                else:
                    print("No matching posts found.")

            elif choice == "11":
                # Option to print all posts
                my_blog.print_all_posts()

            elif choice == "12":
                # Option to print updated posts
                updated_posts = [post for post in my_blog.posts if post.updated_at is not None]
                if updated_posts:
                    print("\nUpdated Posts:")
                    for post in updated_posts:
                        print(post)
                else:
                    print("No updated posts found.")

            elif choice == "13":
                # Option to print deleted posts
                deleted_posts = [post for post in my_blog.delete_post if post.updated_at is None]
                if deleted_posts:
                    print("\nDeleted Posts:")
                    for post in my_blog.delete_post:
                        print(post)
                        if post:
                            deleted_posts = my_blog.posts.append(post)
                        else:
                            print("No deleted")
                else:
                    print("No deleted posts found.")

            elif choice == '14':
                # Option to print deleted posts using a generator
                print("\nPosts:")
                for post in my_blog.get_posts_generator():
                    print(post)

            elif choice == "15":
                # Option to exit the program
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a valid option.")

    except Exception as e:
        print(f"An error occurred: {e}")
       
