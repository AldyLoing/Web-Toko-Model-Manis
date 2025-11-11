from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, ContactMessage

# Contact Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Lengkap',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor WhatsApp (Opsional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Pesan Anda',
                'rows': 5,
                'required': True
            }),
        }

class FormPendaftaran(UserCreationForm):
    email = forms.EmailField(required=True)
    nomor_hape = forms.CharField(max_length=15, required=True)

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nomor_hape', 'address', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super(FormPendaftaran, self).save(commit=False)
        user.nomor_hape = self.cleaned_data['nomor_hape']
        user.nama_bank = None  # ⬅️ Tambahkan baris ini untuk menghindari error
        if commit:
            user.save()
        return user

    

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nomor_hape', 'address', 'role', 'password1', 'password2']

    def clean_role(self):
        user = self.instance
        if not user.is_superuser and self.cleaned_data['role'] == CustomUser.ADMIN_TRX:
            raise forms.ValidationError("Hanya superadmin yang bisa membuat Admin TRC!")
        return self.cleaned_data['role']


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'nama_bank', 'email', 'nomor_hape',
            'address', 'titik', 'role', 'profile_picture', 'password1', 'password2'
        ]
        labels = {
            "username": "Nama Pengguna",
            "nama_bank": "Nama Bank",
            "email": "Email",
            "nomor_hape": "Nomor Telepon",
            "address": "Alamat",
            "titik": "Titik Maps",
            "role": "Peran",
            "profile_picture": "Foto Profil",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "nama_bank": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "nomor_hape": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    role = forms.ChoiceField(
        choices=[
            (CustomUser.ADMIN_UNIT, 'Admin Bank Sampah Unit'),
            (CustomUser.MEMBER, 'Nasabah / Member')
        ],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_id = self.instance.id  # Ambil ID user yang sedang diedit

        if CustomUser.objects.exclude(id=user_id).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_id = self.instance.id  # Ambil ID user yang sedang diedit

        if CustomUser.objects.exclude(id=user_id).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["profile_picture", "username", "nama_bank", "email", "nomor_hape", "address", "titik"]
        labels = {
            "profile_picture": "Foto Profil",
            "username": "Nama Pengguna",
            "nama_bank": "Nama Bank",
            "email": "Email",
            "nomor_hape": "Nomor Telepon",
            "address": "Alamat",
            "titik": "Titik Lokasi",  # Menambahkan label untuk titik lokasi
        }
        widgets = {
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "nama_bank": forms.TextInput(attrs={"class": "form-control", "pattern": "\d{16}", "title": "Masukkan 16 digit angka"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "nomor_hape": forms.TextInput(attrs={"class": "form-control", "pattern": "\d+", "title": "Masukkan hanya angka"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "titik": forms.TextInput(attrs={"class": "form-control", "placeholder": "Latitude, Longitude", "readonly": "readonly"}),  # Menambahkan widget untuk titik
        }

        
class WasteTransactionForm(forms.ModelForm):
    class Meta:
        model = WasteTransaction
        fields = ['user', 'category', 'weight_kg']
        labels = {
            'user': 'Nama Pengguna',
            'category': 'Kategori Sampah',
            'weight_kg': 'Berat (kg)',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # Kalau yang login admin_unit, hanya tampilkan member dari bank yang sama
        if current_user and current_user.role == 'admin_unit':
            self.fields['user'].queryset = CustomUser.objects.filter(
                role='member',
                nama_bank=current_user.nama_bank
            )
            

class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan judul slide'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan deskripsi slide',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class MitraForm(forms.ModelForm):
    class Meta:
        model = Mitra
        fields = ['nama', 'website', 'logo']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
        
class InformasiLinkForm(forms.ModelForm):
    class Meta:
        model = InformasiLink
        fields = ['judul', 'url']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul link'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan URL'}),
        }