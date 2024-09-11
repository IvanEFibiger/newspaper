from django.contrib import admin
from .models import User, Article, Category, Comment, Tag
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "Villalonga News Admin"
admin.site.site_title = "Panel de administración del Periódico"
admin.site.index_title = _("Bienvenido al panel de administración")

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('category', 'published_date', 'is_featured', 'is_important')
    search_fields = ('title', 'body', 'author__username')
    ordering = ('-published_date',)
    readonly_fields = ('published_date', 'updated_date')
    
    
    fieldsets = (
        (None, {
            'fields': ('title', 'lead', 'body', 'media', 'media_footer')
        }),
        ('Autor y Categoría', {
            'fields': ('author', 'category')
        }),
        ('Estado', {
            'fields': ('is_featured', 'is_important')
        }),
        ('Fechas', {
            'fields': ('published_date', 'updated_date'),
            'classes': ('collapse',),  
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            user = request.user
            kwargs["queryset"] = User.objects.filter(id=user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'content', 'created_date')
    list_filter = ('article', 'user', 'created_date')
    search_fields = ('user__username', 'article__title', 'content')
    readonly_fields = ('created_date',)
    
admin.site.register(User)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)