"""Translator module for handling translation services."""

from .azure_translator import AzureTranslator
from .base import BaseTranslator

__all__ = ['AzureTranslator', 'BaseTranslator'] 