import asyncio
from tortoise import Tortoise, run_async, fields
from tortoise.models import Model

class Author(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    books: fields.ReverseRelation["Book"]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        
class Book(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    author: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField(
        "models.Author", related_name="books"
    )
    publication_date = fields.DateField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

async def main():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["__main__"]},
    )
    await Tortoise.generate_schemas()

    print("--- Creating Authors ---")
    author1 = await Author.create(name="Jane Austen")
    author2 = await Author.create(name="George Orwell")
    print(f"Created author: {author1}")
    print(f"Created author: {author2}")

    print("\n--- Creating Books ---")
    book1 = await Book.create(title="Pride and Prejudice", author=author1, publication_date="1813-01-28")
    book2 = await Book.create(title="Emma", author=author1, publication_date="1815-12-23")
    book3 = await Book.create(title="Nineteen Eighty-Four", author=author2, publication_date="1949-06-08")
    print(f"Created book: {book1}")
    print(f"Created book: {book2}")
    print(f"Created book: {book3}")

    print("\n--- Reading Authors ---")
    authors = await Author.all()
    for author in authors:
        print(f"Found author: {author}")

    print("\n--- Reading Books ---")
    books = await Book.all().prefetch_related("author")
    for book in books:
        print(f"Found book: {book} by {book.author.name}")

    print("\n--- Reading Books by a Specific Author ---")
    austen_books = await Book.filter(author=author1).all()
    print(f"Books by {author1.name}: {[book.title for book in austen_books]}")

    print("\n--- Updating an Author ---")
    await Author.filter(id=author2.id).update(name="Eric Arthur Blair (George Orwell)")
    updated_author2 = await Author.get(id=author2.id)
    print(f"Updated author: {updated_author2}")

    print("\n--- Updating a Book ---")
    await Book.filter(id=book1.id).update(publication_date="1813-01-29")
    updated_book1 = await Book.get(id=book1.id)
    print(f"Updated book: {updated_book1}")

    print("\n--- Deleting a Book ---")
    deleted_count = await Book.filter(id=book2.id).delete()
    print(f"Deleted {deleted_count} book(s)")
    remaining_books = await Book.all()
    print(f"Remaining books: {[book.title for book in remaining_books]}")

    print("\n--- Deleting an Author (will also delete associated books due to ForeignKey) ---")
    deleted_author_count = await Author.filter(id=author1.id).delete()
    print(f"Deleted {deleted_author_count} author(s)")
    remaining_authors = await Author.all()
    remaining_books_after_author_delete = await Book.all()
    print(f"Remaining authors: {[author.name for author in remaining_authors]}")
    print(f"Remaining books after author deletion: {[book.title for book in remaining_books_after_author_delete]}")

if __name__ == "__main__":
    run_async(main())
