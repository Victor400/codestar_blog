from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for adding/editing comments."""

    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your comment here...",
                    "rows": 4,
                }
            ),
        }
        labels = {
            "body": "",
        }

    def clean_body(self):
        """Validate the comment body."""
        body = self.cleaned_data.get("body", "").strip()

        if not body:
            raise forms.ValidationError("Comment cannot be empty.")

        if len(body) < 5:
            raise forms.ValidationError("comment, at least 5 characters long.")

        if len(body) > 500:
            raise forms.ValidationError("Comment not exceed 500 characters.")

        return body
