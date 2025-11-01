from django.contrib import admin

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'title')
    readonly_fields = ('created_at',)
