from django import forms

class SetPasswordForm(forms.Form):
    """ Form to set a new password with validation """
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        min_length=6,  # Minimum password length
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data