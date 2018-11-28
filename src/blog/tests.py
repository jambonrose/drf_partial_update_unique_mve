"""Tests demonstrate behavior change with unique constraint"""
from django.test import TestCase

from .models import Post, UniquePost
from .serializers import PostSerializer, UniquePostSerializer


class SerializersTests(TestCase):
    """Test partial update behavior of Serializers"""

    def _build_serializer_with_partial_changes(self, Model, Serializer):
        """Utility: instantiate a partially-updated Serializer"""
        post = Model.objects.create(title="first", slug="slug")
        return Serializer(instance=post, data={"title": "second"}, partial=True)

    def test_post_partial(self):
        """Update PostSerializer partially with only the title"""
        s_post = self._build_serializer_with_partial_changes(Post, PostSerializer)
        self.assertTrue(s_post.is_valid(), msg=s_post.errors)
        s_post.save()
        post = Post.objects.get(slug="slug")
        self.assertEqual("second", post.title)

    # Included for convenience: fails!
    # def test_post_partial(self):
    #     """Update UniquePostSerializer partially with only the title"""
    #     s_post = self._build_serializer_with_partial_changes(
    #         UniquePost, UniquePostSerializer
    #     )
    #     self.assertTrue(s_post.is_valid(), msg=s_post.errors)
    #     s_post.save()
    #     post = Post.objects.get(slug="slug")
    #     self.assertEqual("second", post.title)

    def test_unique_post_partial(self):
        """Show failure of partially updating UniquePostSerializer

        If we were to use the following assertion (as above), we would fail
        with the errors printed after.

            self.assertTrue(s_post.is_valid(), msg=s_post.errors)

            AssertionError: False is not true : {
                'slug': [
                    ErrorDetail(
                        string='This field is required.',
                        code='required'
                    ),
                ],
                'pub_date': [
                    ErrorDetail(
                        string='This field is required.',
                        code='required'
                    )
                ],
            }
        """
        s_post = self._build_serializer_with_partial_changes(
            UniquePost, UniquePostSerializer
        )
        self.assertFalse(s_post.is_valid())
        self.assertIn("slug", s_post.errors)
        self.assertIn("pub_date", s_post.errors)
        self.assertEqual(s_post.errors["slug"][0].code, "required")
        self.assertEqual(s_post.errors["pub_date"][0].code, "required")

    def test_unique_post_partial_extra_fields(self):
        """Show inclusion of slug and pub_date enable partial update"""
        post = UniquePost.objects.create(title="first", slug="slug")
        s_post = UniquePostSerializer(
            instance=post,
            data={"title": "second", "slug": post.slug, "pub_date": post.pub_date},
            partial=True,
        )
        self.assertTrue(s_post.is_valid(), msg=s_post.errors)
        s_post.save()
        post.refresh_from_db()
        self.assertEqual("second", post.title)
