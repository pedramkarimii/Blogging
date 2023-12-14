import argparse

# Assuming the necessary imports are in OOP_Blogging module
from OOP_Blogging import *


class User:
    """Class representing a User in the blogging system."""

    def __init__(self, user_id, username):
        """Initialize a User with a unique ID and username."""
        self.user_id = user_id
        self.username = username


class Post:
    """Class representing a Blog Post."""

    def __init__(self, title, content, author):
        """Initialize a Post with title, content, and author information."""
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.now()
        self.updated_at = None

    def update_content(self, new_content):
        """Update the content of the post and set the updated timestamp."""
        self.content = new_content
        self.updated_at = datetime.now()

    def __str__(self):
        """String representation of the Post."""
        formatted_updated_at = str(self.updated_at) if self.updated_at else "Not updated"
        return f"Post Title: {self.title}\nContent: {self.content}\nAuthor: {self.author.username}\nCreated At: {self.created_at}\nUpdated At: {formatted_updated_at}"


class Blog:
    """Class representing a Blog."""

    def __init__(self):
        """Initialize a Blog with an empty list of posts."""
        self.posts = []

    def add_post(self, post):
        """Add a post to the blog."""
        self.posts.append(post)

    def delete_post_by_title(self, title):
        """Delete a post by its title."""
        # Use list comprehension to find posts with the given title
        posts_to_delete = [post for post in self.posts if post.title == title]

        if posts_to_delete:
            # Assuming only the first post with the title will be deleted
            post_to_delete = posts_to_delete[0]
            self.posts.remove(post_to_delete)
            return [post_to_delete]
        else:
            return []

    def view_all_posts(self):
        """Get all posts in the blog."""
        return self.posts


def log_activity(activity):
    """Decorator function to log an activity."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Log the activity with the current timestamp
            result = func(*args, **kwargs)
            print(f"[{datetime.now()}] Activity: {activity}")
            return result

        return wrapper

    return decorator


def get_user_by_username(username, my_blog):
    """Get a user by their username."""
    return next((user for user in my_blog.view_all_posts() if user.username == username), None)


@log_activity("Added a post")
def add_post(my_blog):
    """Function to interactively add a post."""
    title = input("Enter post title: ")
    content = input("Enter post content: ")
    author_username = input("Enter author username: ")

    author = get_user_by_username(author_username, my_blog)
    if not author:
        # If the author doesn't exist, create a new User instance
        author = User(user_id=len(my_blog.view_all_posts()) + 1, username=author_username)

    new_post = Post(title=title, content=content, author=author)
    my_blog.add_post(new_post)
    print(f"Post '{title}' added successfully!")


@log_activity("Deleted a post")
def delete_post(my_blog):
    """Function to interactively delete a post."""
    title_to_delete = input("Enter the title of the post to delete: ")

    posts_to_delete = my_blog.delete_post_by_title(title_to_delete)

    if posts_to_delete:
        print("Post(s) deleted successfully!")
        for post in posts_to_delete:
            print(post)
    else:
        print("No matching posts found.")


@log_activity("Viewed all posts")
def display_posts(my_blog):
    """Function to display all posts."""
    all_posts = my_blog.view_all_posts()

    if all_posts:
        print("All Posts:")
        for post in all_posts:
            print(post)
    else:
        print("No posts available.")


def main():
    """Main function to execute the blog management tool."""
    parser = argparse.ArgumentParser(description="Simple blog management tool.")
    parser.add_argument("commands", nargs='*', choices=["add", "delete", "display", "exit"],
                        help="Commands to perform consecutively")

    args = parser.parse_args()

    my_blog = Blog()

    while not args.commands or "exit" not in args.commands:
        command = input("\nAvailable commands: add, delete, display, exit\nEnter command: ")

        if command == "add":
            add_post(my_blog)
        elif command == "delete":
            delete_post(my_blog)
        elif command == "display":
            display_posts(my_blog)
        elif command == "exit":
            break
        else:
            print(f"Invalid command '{command}'. Try again.")


if __name__ == "__main__":
    main()
