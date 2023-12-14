# from datetime import datetime
# import time
# import logging
#
# logging.basicConfig(level=logging.INFO)
#
#
# def log_activity(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         logging.info(f"{func.__name__} took {elapsed_time:.5f} seconds to execute.")
#         logging.info("Log: This is a log message.")
#         return result
#
#     return wrapper
# class User:
#     def __init__(self, user_id, username):
#         self.user_id = user_id
#         self.username = username
#
#     def __str__(self):
#         return f"User ID: {self.user_id}, Username: {self.username}"
#
#
#
# class Post:
#     def __init__(self, title, content, author):
#         self.title = title
#         self.content = content
#         self.author = author
#         self.created_at = datetime.now()
#         self.updated_at = None
#
#     @log_activity
#     def update_content(self, new_content):
#         self.content = new_content
#         self.updated_at = datetime.now()
#
#     def __str__(self):
#         formatted_updated_at = str(self.updated_at) if self.updated_at else "Not updated"
#         return f"Post Title: {self.title}\nContent: {self.content}\nAuthor: {self.author.username}\nCreated At: {self.created_at}\nUpdated At: {formatted_updated_at}\n"
#     # def __str__(self):
#     #     formatted_updated_at = str(self.updated_at) if self.updated_at else "Not updated"
#     #     return f"Post Title: {self.title}\nContent: {self.content}\nAuthor: {self.author.username}\nCreated At: {self.created_at}\nUpdated At: {formatted_updated_at}"
#
#
# class Blog:
#     def __init__(self):
#         self.posts = []
#         self.delete_post = []
#
#     @log_activity
#     def add_post(self, posts, current_user=None):
#         self.posts.extend(posts)
#
#     @log_activity
#     def delete_post_by_title(self, title):
#         posts_to_delete = [post for post in self.posts if post.title == title]
#
#         if posts_to_delete:
#             for post in posts_to_delete:
#                 post.updated_at = None  # Set updated_at to None to mark the post as deleted
#                 self.delete_post.append(post)
#                 self.posts.remove(post)
#
#             return posts_to_delete
#         else:
#             return []
#
#     @log_activity
#     def delete_post_by_author(self, author_username):
#         lowercase_author_username = author_username.lower()
#         posts_to_delete = [post for post in self.posts if post.author.username.lower() == lowercase_author_username]
#
#         for post in posts_to_delete:
#             post.updated_at = None  # Set updated_at to None to mark the post as deleted
#
#         self.posts = [post for post in self.posts if post not in posts_to_delete]
#         return posts_to_delete
#
#     @log_activity
#     def search_post_by_title(self, title):
#         return [post for post in self.posts if post.title == title]
#
#     @log_activity
#     def search_post_by_author(self, author_username):
#         lowercase_author_username = author_username.lower()
#         return [post for post in self.posts if post.author.username.lower() == lowercase_author_username]
#
#     @log_activity
#     def search(self, filter_function):
#         return [post for post in self.posts if filter_function(post)]
#
#     @log_activity
#     def filter_posts_by_author(self, author):
#         return self.search(lambda post: post.author.username.lower() == author.username.lower())
#
#     @log_activity
#     def filter_posts_by_title(self, keyword):
#         return self.search(lambda post: keyword.lower() in post.title.lower())
#
#     @log_activity
#     def view_user_posts_by_title(self, author_username, title):
#         lowercase_author_username = author_username.lower()
#         matching_posts = [post for post in self.posts
#                           if post.author.username.lower() == lowercase_author_username
#                           and post.title == title]
#
#         return matching_posts
#
#     @log_activity
#     def filter_posts_by_username_and_title(self, author_username, title):
#         lowercase_author_username = author_username.lower()
#         return [post for post in self.posts
#                 if post.author.username.lower() == lowercase_author_username
#                 and title.lower() in post.title.lower()]
#
#     @log_activity
#     def view_user_posts_by_author(self, author_username):
#         lowercase_author_username = author_username.lower()
#         return [post for post in self.posts if post.author.username.lower() == lowercase_author_username]
#
#     @log_activity
#     def update_post_content(self, title, new_content):
#         matching_posts = [post for post in self.posts if post.title == title]
#
#         if matching_posts:
#             post_to_update = matching_posts[0]
#             post_to_update.update_content(new_content)
#             return post_to_update
#         else:
#             return None
#
#     def get_posts_generator(self):
#         # Generator function to yield posts
#         for post in self.delete_post:
#             yield post
#
#
# @log_activity
# def print_all_posts(blog):
#     print("All Posts:")
#     for post in blog.posts:
#         print(post)
#
#
# if __name__ == "__main__":
#     my_blog = Blog()
#
#     while True:
#         print("\nOptions:")
#         print("1.Add Post")
#         print("2.Delete Post by Title")
#         print("3.Delete Post by Author")
#         print("4.Search Post by Title")
#         print("5.Search Post by Author")
#         print("6.Update Post Content")
#         print("7.Filter Posts by Username and Title")
#         print("8.Filter Posts by Author")
#         print("9.View User Posts by Author")
#         print("10.View User Posts by Title")
#         print("11.Print All Posts")
#         print("12.Print Updated Posts")
#         print("13.Print Deleted Posts")
#         print("14.Print Deleted Posts(yield)")
#         print("15.Exit")
#
#         choice = input("Enter your choice: ")
#
#         if choice == "1":
#             num_posts = int(input("Enter the number of posts to add: "))
#             posts = []
#             for _ in range(num_posts):
#                 title = input("Enter post title: ")
#                 content = input("Enter post content: ")
#                 author_username = input("Enter author username: ")
#
#                 # Create a new User instance
#                 author = User(user_id=len(my_blog.posts) + 1, username=author_username)
#
#                 new_post = Post(title=title, content=content, author=author)
#                 posts.append(new_post)
#
#             my_blog.add_post(posts)
#             print(f"{num_posts} post(s) added successfully!")
#
#
#         elif choice == "2":
#             title_to_delete = input("Enter the title of the post to delete: ")
#             posts_to_delete = my_blog.delete_post_by_title(title_to_delete)
#
#             if posts_to_delete:
#                 print("Post(s) deleted successfully!")
#                 for post in posts_to_delete:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#         elif choice == "3":
#             author_to_delete = input("Enter the username of the author to delete posts: ")
#             posts_to_delete = my_blog.delete_post_by_author(author_to_delete)
#
#             if posts_to_delete:
#                 print("Post(s) deleted successfully!")
#                 for post in posts_to_delete:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#         elif choice == "4":
#             title_to_search = input("Enter the title of the post to search: ")
#             matching_posts = my_blog.search_post_by_title(title_to_search)
#
#             if matching_posts:
#                 print("\nMatching Posts:")
#                 for post in matching_posts:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#         elif choice == "5":
#             author_to_search = input("Enter the username of the author: ")
#             matching_posts = my_blog.search_post_by_author(author_to_search)
#
#             if matching_posts:
#                 print("\nMatching Posts:")
#                 for post in matching_posts:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#         elif choice == "6":
#             title_to_update = input("Enter the title of the post to update: ")
#             new_content = input("Enter the new content for the post: ")
#             updated_post = my_blog.update_post_content(title_to_update, new_content)
#             if updated_post is not None:
#                 print("Post content updated successfully!")
#                 print(updated_post)
#             else:
#                 print("No matching posts found for update.")
#         elif choice == "7":
#             author_to_filter = input("Enter the username to filter by: ")
#             title_to_filter = input("Enter the title to filter by: ")
#             filtered_posts = my_blog.filter_posts_by_username_and_title(author_to_filter, title_to_filter)
#
#             if filtered_posts:
#                 print("\nFiltered Posts:")
#                 for post in filtered_posts:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#         elif choice == "8":
#             author_to_filter = input("Enter the username to filter by: ")
#             # Create a User instance for the specified author
#             author_instance = User(0, author_to_filter)
#             filtered_posts = my_blog.filter_posts_by_author(author_instance)
#
#             if filtered_posts:
#                 print("\nFiltered Posts:")
#                 for post in filtered_posts:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#
#         elif choice == "9":
#             author_to_view = input("Enter the username of the author: ")
#             matching_posts = my_blog.view_user_posts_by_author(author_to_view)
#
#             if matching_posts:
#                 print("\nMatching Posts:")
#                 for post in matching_posts:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#         elif choice == "10":
#             author_to_view = input("Enter the username of the author: ")
#             title_to_view = input("Enter the title of the post: ")
#             matching_posts = my_blog.view_user_posts_by_title(author_to_view, title_to_view)
#
#             if matching_posts:
#                 print("\nMatching Posts:")
#                 for post in matching_posts:
#                     print(post)
#             else:
#                 print("No matching posts found.")
#
#         elif choice == "11":
#             print_all_posts(my_blog)
#
#         elif choice == "12":
#             updated_posts = [post for post in my_blog.posts if post.updated_at is not None]
#
#             if updated_posts:
#                 print("\nUpdated Posts:")
#                 for post in updated_posts:
#                     print(post)
#             else:
#                 print("No updated posts found.")
#
#         elif choice == "13":
#             deleted_posts = [post for post in my_blog.delete_post if post.updated_at is None]
#
#             if deleted_posts:
#                 print("\nDeleted Posts:")
#                 for post in my_blog.delete_post:
#                     print(post)
#                     if post:
#                         deleted_posts = my_blog.posts.append(post)
#                     else:
#                         print("No deleted")
#             else:
#                 print("No deleted posts found.")
#
#         elif choice == '14':
#             print("\nPosts:")
#             for post in my_blog.get_posts_generator():
#                 print(post)
#
#         elif choice == "15":
#             print("Exiting the program. Goodbye!")
#             break
#
#         else:
#             print("Invalid choice. Please enter a valid option.")
