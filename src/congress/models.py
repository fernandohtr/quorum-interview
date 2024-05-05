from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Legislator(models.Model):
    class PoliticalPartyType(models.TextChoices):
        """
        https://bestdiplomats.org/political-parties-in-the-us/
        """

        DEMOCRATIC = "D"
        REPUBLICAN = "R"
        LIBERTARIAN = "L"
        GREEN = "G"
        CONSTITUTION = "C"
        REFORM = "Re"
        SOCIALIST = "S"
        LIBERTY_UNION = "LU"
        PROGESSIVE = "P"
        AMERICAN_INDEPENDENT = "AI"
        KNOW_NOTHING = "KN"
        FREE_SOIL = "FS"
        POPULIST = "Po"
        PROGRESSIVE_LABOR = "PL"
        INDEPENDENT_AMERICAN = "IA"

    class StateType(models.TextChoices):
        ALABAMA = "AL"
        ALASKA = "AK"
        ARIZONA = "AZ"
        ARKANSAS = "AR"
        CALIFORNIA = "CA"
        COLORADO = "CO"
        CONNECTICUT = "CT"
        DELAWARE = "DE"
        FLORIDA = "FL"
        GEORGIA = "GA"
        HAWAII = "HI"
        IDAHO = "ID"
        ILLINOIS = "IL"
        INDIANA = "IN"
        IOWA = "IA"
        KANSAS = "KS"
        KENTUCKY = "KY"
        LOUISIANA = "LA"
        MAINE = "ME"
        MARYLAND = "MD"
        MASSACHUSETTS = "MA"
        MICHIGAN = "MI"
        MINNESOTA = "MN"
        MISSISSIPPI = "MS"
        MISSOURI = "MO"
        MONTANA = "MT"
        NEBRASKA = "NE"
        NEVADA = "NV"
        NEW_HAMPSHIRE = "NH"
        NEW_JERSEY = "NJ"
        NEW_MEXICO = "NM"
        NEW_YORK = "NY"
        NORTH_CAROLINA = "NC"
        NORTH_DAKOTA = "ND"
        OHIO = "OH"
        OKLAHOMA = "OK"
        OREGON = "OR"
        PENNSYLVANIA = "PA"
        RHODE_ISLAND = "RI"
        SOUTH_CAROLINA = "SC"
        SOUTH_DAKOTA = "SD"
        TENNESSEE = "TN"
        TEXAS = "TX"
        UTAH = "UT"
        VERMONT = "VT"
        VIRGINIA = "VA"
        WASHINGTON = "WA"
        WEST_VIRGINIA = "WV"
        WISCONSIN = "WI"
        WYOMING = "WY"

    class CongressHouse(models.IntegerChoices):
        REPRESENTATIVE = 1
        SENATOR = 2

    name = models.CharField(max_length=250)
    political_party = models.CharField(choices=PoliticalPartyType, max_length=3, blank=True, null=True)
    state = models.CharField(choices=StateType, max_length=2, blank=True, null=True)
    district = models.SmallIntegerField(blank=True, null=True)
    congress_house = models.SmallIntegerField(choices=CongressHouse, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Legislator)
def create_legislator_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.name} {instance.political_party} {instance.state} {instance.district}")


class Bill(models.Model):
    class OriginType(models.TextChoices):
        HOUSE_RESOLUTION = "H.R."
        SENATOR = "S."

    number = models.CharField(max_length=8, blank=True, null=True)
    title = models.CharField(max_length=250)
    origin = models.CharField(choices=OriginType, max_length=4, blank=True, null=True)
    sponsor = models.ForeignKey(Legislator, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Bill)
def create_bill_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify({instance.number})


class Vote(models.Model):
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, blank=True, null=True)


class VoteResult(models.Model):
    class VoteType(models.IntegerChoices):
        SUPPORTES = 1
        OPPOSES = 2

    legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE, blank=True, null=True)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, blank=True, null=True)
    vote_type = models.IntegerField(choices=VoteType)
