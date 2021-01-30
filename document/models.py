from django.db import models
from django.utils.translation import gettext_lazy as _
from config import constants


class Status(models.Model):
    title = models.CharField(verbose_name=_('Status name'), max_length=255, null=True, unique=True)
    description = models.TextField(verbose_name=_('Description'), max_length=1000, null=True, blank=True)
    color = models.CharField(verbose_name=_('Color'), max_length=10, null=True, blank=True)
    is_detail = models.BooleanField(verbose_name=_('Is detail'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    def __str__(self):
        return str(self.title)


class DocumentType(models.Model):
    document_type_name = models.CharField(verbose_name=_('Document type'), max_length=255, null=True)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    class Meta:
        db_table = 'document_document_type'

    def __str__(self):
        return f'Doc type name: {self.document_type_name}'


# Create your models here.
class Document(models.Model):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True)
    original_name = models.CharField(verbose_name=_('Original name'), max_length=255, null=True, unique=True)
    description = models.TextField(verbose_name=_('Description'), max_length=2000, null=True, blank=True)
    file_path = models.FileField(verbose_name=_('File path'), upload_to='files/%Y/%m/%d/', null=True, blank=True)
    mime_type = models.CharField(verbose_name=_('Mime type'), max_length=50, null=True)
    is_processed = models.BooleanField(verbose_name=_('Is processed'), default=False)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    def __str__(self):
        return f'{self.original_name}'


class Attribute(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True)
    attribute_name = models.CharField(verbose_name=_('Attribute name'), max_length=255, null=True, blank=True)
    is_required = models.BooleanField(verbose_name=_('Is required'), default=False)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    def __str__(self):
        return f'Тип документа: {self.document_type.document_type_name}; Имя атрибута: {self.attribute_name}'


class Ocr(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    ocr_text = models.TextField(verbose_name=_('OCR text'), max_length=1000, blank=True, null=True)
    user_text = models.TextField(verbose_name=_('User text'), max_length=1000, blank=True, null=True)
    status = models.SmallIntegerField(verbose_name=_('Status'), blank=True, null=True, default=2)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    def __str__(self):
        return f'DocID: {self.document.id}; OcrText: {self.ocr_text}'


class Nlp(models.Model):
    """
    status = 0 - not recognized word ids or text
    status = 1 - recognized word ids
    status = 2 - recognized only text (for ocr_text)
    status = 3 - operator add attribute with word ids
    status = 4 - new attribute
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True)
    position = models.IntegerField(verbose_name=_('Position'), null=True, default=None)
    ocr_word_ids = models.JSONField(verbose_name=_('OCR word IDs'), null=True, default=None, blank=True)
    status = models.SmallIntegerField(verbose_name=_("Status"), choices=constants.STATUS_RECOGNITION_CHOICES, default=0)
    ocr_text = models.TextField(verbose_name=_("Ocr text"), max_length=2000, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    def __str__(self):
        return f'NlpID: {self.id}; Document: {self.document.id}; Attribute: {self.attribute.attribute_name} '