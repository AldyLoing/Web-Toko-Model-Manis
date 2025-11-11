from django.core.management.base import BaseCommand
from django.utils.text import slugify
from posting.models import Category

class Command(BaseCommand):
    help = 'Generate slugs for categories that don\'t have them'

    def handle(self, *args, **options):
        categories_without_slug = Category.objects.filter(slug__isnull=True) | Category.objects.filter(slug='')
        
        for category in categories_without_slug:
            category.slug = slugify(category.name)
            category.save()
            self.stdout.write(
                self.style.SUCCESS(f'Generated slug "{category.slug}" for category "{category.name}"')
            )
        
        if not categories_without_slug:
            self.stdout.write(self.style.SUCCESS('All categories already have slugs!'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated slugs for {categories_without_slug.count()} categories')
            )