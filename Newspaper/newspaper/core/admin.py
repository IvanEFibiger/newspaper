from django.contrib import admin
from .models import User, Article, Category, Comment, Tag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            user = request.user
            kwargs["queryset"] = User.objects.filter(id=user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
admin.site.register(User)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Tag)