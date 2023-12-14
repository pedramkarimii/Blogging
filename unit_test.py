import unittest
from unittest.mock import patch

from OOP_Blogging import *


class TestBlog(unittest.TestCase):
    def setUp(self):
        """Set up a new Blog instance for each test."""
        self.blog = Blog()

    @patch('builtins.input', side_effect=['Test Title', 'Test Content', 'test_user'])
    def test_add_post(self, mock_input):
        """Test adding a post to the blog"""
        # Mock user input for title, content, and author username
        self.blog.add_post([Post(input(), input(), User(1, input()))])
        # Ensure the number of posts in the blog is 1 after adding a post
        self.assertEqual(len(self.blog.posts), 1)

    def test_delete_post_by_title(self):
        """Test deleting a post by title"""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # Delete the post by title
        self.blog.delete_post_by_title("Test Title")
        # Ensure the post is not in the 'posts' list but is in the 'delete_post' list
        self.assertNotIn(post, self.blog.posts)
        self.assertIn(post, self.blog.delete_post)

    def test_delete_post_by_author(self):
        """Test deleting a post by author."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # Delete the post by author
        self.blog.delete_post_by_author("test_user")
        # Ensure the post is not in the 'posts' list but is in the 'delete_post' list
        self.assertNotIn(post, self.blog.posts)
        self.assertIn(post, self.blog.delete_post)

    def test_search_post_by_title(self):
        """Test searching for a post by title."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # Search for the post by title
        result = self.blog.search_post_by_title("Test Title")
        # Ensure the post is in the search result
        self.assertIn(post, result)

    def test_search_post_by_author(self):
        """Test searching for a post by author."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # Search for the post by author
        result = self.blog.search_post_by_author("test_user")
        # Ensure the post is in the search result
        self.assertIn(post, result)

    def test_filter_posts_by_title(self):
        """Test filtering posts by title."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # Filter posts by title keyword
        result = self.blog.filter_posts_by_title("Test")
        # Ensure the post is in the filtered result
        self.assertIn(post, result)

    def test_filter_posts_by_author(self):
        """Test filtering posts by author."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # Filter posts by author
        result = self.blog.filter_posts_by_author("test_user")
        # Ensure the post is in the filtered result
        self.assertIn(post, result)

    def test_view_user_posts_by_title(self):
        """Test viewing user posts by title."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # View user posts by title
        result = self.blog.view_user_posts_by_title("test_user", "Test Title")
        # Ensure the post is in the viewed result
        self.assertIn(post, result)

    def test_view_user_posts_by_author(self):
        """Test viewing user posts by author."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # View user posts by author
        result = self.blog.view_user_posts_by_author("test_user")
        # Ensure the post is in the viewed result
        self.assertIn(post, result)

    def test_update_post_content(self):
        """Test updating post content."""
        # Create a post and add it to the blog
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.add_post([post])
        # Update the post content
        updated_post = self.blog.update_post_content("Test Title", "New Content")
        # Ensure the content of the post is updated
        self.assertEqual(updated_post.content, "New Content")

    def test_get_posts_generator(self):
        """Test getting posts generator."""
        # Create a post and add it to the 'delete_post' list
        post = Post("Test Title", "Test Content", User(1, "test_user"))
        self.blog.delete_post = [post]
        # Get posts using the generator
        result = list(self.blog.get_posts_generator())
        # Ensure the post is in the result
        self.assertIn(post, result)


if __name__ == '__main__':
    unittest.main()
