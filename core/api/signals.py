from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from core.models import Task, Team, Notification, Comment


@receiver(m2m_changed, sender=Task.assigned_users.through)
def create_notifications_on_assignment(sender, instance, action, pk_set, **kwargs):
    message = f"@{instance.created_by} have assigned task to you."
    if action == "post_add":
        for user_id in pk_set:
            Notification.objects.create(
                task=instance,
                user_id=user_id,
                message=message
            )

@receiver(m2m_changed, sender=Team.members.through)
def create_notifications_on_team_adding(sender, instance, action, pk_set, **kwargs):
    message = f"You have been added to the {sender.team.name} team."
    if action == "post_add":
        for user_id in pk_set:
            Notification.objects.create(
                task=instance,
                user_id=user_id,
                message=message
            )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    message = f"@{instance.user}: {instance.message}"
    if created and instance.task:
        for user in instance.task.assigned_users.all():
            Notification.objects.create(
                task=instance.task,
                user=user,
                message=message
            )
