from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=150, unique=True)
    profile_image = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    groups = models.ManyToManyField(Group, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_user_permissions')

    def __str__(self):
        return self.username


class Image(models.Model):
    image_url = models.URLField()

    def __str__(self):
        return self.image_url


class Match(models.Model):
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    match_status = models.CharField(max_length=50)  # e.g., 'Scheduled', 'Ongoing', 'Completed'
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    match_date = models.DateTimeField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.match_date}"


class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    team_logo = models.URLField()

    def __str__(self):
        return self.team_name


class League(models.Model):
    league_name = models.CharField(max_length=50, unique=True)
    league_logo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.league_name


class TeamLeagues(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team', 'league')

    def __str__(self):
        return f"{self.team.team_name} in {self.league.league_name}"


class Room(models.Model):
    room_id = models.CharField(max_length=50, unique=True)
    room_name = models.CharField(max_length=50)
    room_url = models.URLField()
    room_description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.room_name


class RoomUsers(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.room.room_name}"


class RoomRule(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    max_user_num = models.IntegerField(default=128)
    expiration_date = models.DateTimeField()
    score_winner_point = models.IntegerField()
    side_winner_point = models.IntegerField()
    score_winner_open = models.BooleanField()

    def __str__(self):
        return f"Rule for {self.room.room_name}"


class RoomLeagues(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room', 'league')

    def __str__(self):
        return f"{self.room.room_name} associated with {self.league.league_name}"
