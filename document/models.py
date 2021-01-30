from django.contrib.postgres.fields import ArrayField
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
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, default=1)
    original_name = models.CharField(verbose_name=_('Original name'), max_length=255, null=True)
    description = models.TextField(verbose_name=_('Description'), max_length=2000, null=True, blank=True)
    file_path = models.FileField(verbose_name=_('File path'), upload_to='files/%Y/%m/%d/', null=True, blank=True)
    mime_type = models.CharField(verbose_name=_('Mime type'), max_length=50, null=True, blank=True)
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
    ocr_word_ids = ArrayField(models.IntegerField(), null=True, blank=True)
    status = models.SmallIntegerField(verbose_name=_("Status"), choices=constants.STATUS_RECOGNITION_CHOICES, default=0)
    ocr_text = models.TextField(verbose_name=_("Ocr text"), max_length=2000, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    def __str__(self):
        return f'NlpID: {self.id}; Document: {self.document.id}; Attribute: {self.attribute.attribute_name} '


class NlpResult(models.Model):
    """Таблица для синхронизации основных полей из nlp"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    cve = models.CharField(verbose_name=_('CVE'), max_length=255, null=True, blank=True, db_index=True)
    cwe = models.CharField(verbose_name=_('CWE'), max_length=255, null=True, blank=True, db_index=True)
    software = models.CharField(verbose_name=_('SOFTWARE'), max_length=255, null=True, blank=True, db_index=True)
    malware = models.CharField(verbose_name=_('MALWARE'), max_length=255, null=True, blank=True, db_index=True)
    course_of_action = models.CharField(verbose_name=_('COURSE_OF_ACTION'), max_length=255, null=True, blank=True, db_index=True)
    intrusion_set = models.CharField(verbose_name=_('INTRUSION_SET'), max_length=255, null=True, blank=True, db_index=True)
    threat_actor = models.CharField(verbose_name=_('THREAT_ACTOR'), max_length=255, null=True, blank=True, db_index=True)
    tool = models.CharField(verbose_name=_('TOOL'), max_length=255, null=True, blank=True, db_index=True)
    attack_pattern = models.CharField(verbose_name=_('ATTACK_PATTERN'), max_length=255, null=True, blank=True, db_index=True)
    industry = models.CharField(verbose_name=_('INDUSTRY'), max_length=255, null=True, blank=True, db_index=True)
    mitre_attack = models.CharField(verbose_name=_('MITRE_ATTACK'), max_length=255, null=True, blank=True, db_index=True)
    campaign = models.CharField(verbose_name=_('CAMPAIGN'), max_length=255, null=True, blank=True, db_index=True)
    org = models.CharField(verbose_name=_('ORG'), max_length=255, null=True, blank=True, db_index=True)
    country = models.CharField(verbose_name=_('COUNTRY'), max_length=255, null=True, blank=True, db_index=True)
    city = models.CharField(verbose_name=_('CITY'), max_length=255, null=True, blank=True, db_index=True)
    geolocation = models.CharField(verbose_name=_('GEOLOCATION'), max_length=255, null=True, blank=True, db_index=True)
    time_stamp = models.DateTimeField(verbose_name=_('TIMESTAMP'), null=True, blank=True, db_index=True)
    ioc = models.CharField(verbose_name=_('IOC'), max_length=255, null=True, blank=True, db_index=True)
    technique = models.CharField(verbose_name=_('TECHNIQUE'), max_length=255, null=True, blank=True, db_index=True)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated date'), auto_now=True, null=True)

    class Meta:
        db_table = 'document_nlp_result'

    def __str__(self):
        return f'NlpID: {self.id}; Document: {self.document.id} '
