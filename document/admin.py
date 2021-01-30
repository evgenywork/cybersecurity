from django.contrib import admin
from .models import *


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "is_detail")


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "document_type_name", "is_active", "created_at")


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "document_type", "attribute_name", "is_required", "is_active")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "original_name", "status", "is_processed", "is_active")


@admin.register(Nlp)
class NlpAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "attribute", "status", "is_active")


@admin.register(Ocr)
class OcrAdmin(admin.ModelAdmin):
    list_display = ("id", "ocr_text", "status", "is_active")


@admin.register(NlpResult)
class NlpResultAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "is_active")


